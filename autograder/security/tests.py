import os
import unittest
import subprocess
import uuid
import tempfile

from collections import OrderedDict

from .autograder_sandbox import AutograderSandbox


def kb_to_bytes(num_kb):
    return 1000 * num_kb


def mb_to_bytes(num_mb):
    return 1000 * kb_to_bytes(num_mb)


def gb_to_bytes(num_gb):
    return 1000 * mb_to_bytes(num_gb)


class AutograderSandboxInitTestCase(unittest.TestCase):
    def setUp(self):
        self.name = 'awexome_container'
        self.ip_whitelist = ['35.2.65.126']
        self.environment_variables = OrderedDict(
            {'spam': 'egg', 'sausage': 42})

    def test_default_init(self):
        sandbox = AutograderSandbox()
        self.assertIsNotNone(sandbox.name)
        self.assertCountEqual([], sandbox.ip_address_whitelist)
        self.assertIsNone(sandbox.environment_variables)

    def test_non_default_init(self):
        sandbox = AutograderSandbox(
            name=self.name,
            ip_address_whitelist=self.ip_whitelist,
            environment_variables=self.environment_variables
        )

        self.assertEqual(self.name,
                         sandbox.name)
        self.assertEqual(self.ip_whitelist,
                         sandbox.ip_address_whitelist)
        self.assertEqual(self.environment_variables,
                         sandbox.environment_variables)

    def test_context_manager(self):
        with AutograderSandbox(name=self.name) as sandbox:
            self.assertEqual(self.name, sandbox.name)
            # If the container was created successfully, we
            # should get an error if we try to create another
            # container with the same name.
            with self.assertRaises(subprocess.CalledProcessError):
                with AutograderSandbox(name=self.name):
                    pass

        # The container should have been deleted at this point,
        # so we should be able to create another with the same name.
        with AutograderSandbox(name=self.name):
            pass

    def test_sandbox_environment_variables_set(self):
        print_env_var_script = "echo ${}".format(
            ' $'.join(self.environment_variables))

        sandbox = AutograderSandbox(
            environment_variables=self.environment_variables)
        with sandbox, tempfile.NamedTemporaryFile('w+') as f:
            f.write(print_env_var_script)
            f.seek(0)
            sandbox.add_files(f.name)
            result = sandbox.run_command(['bash', os.path.basename(f.name)])
            expected_output = ' '.join(
                str(val) for val in self.environment_variables.values())
            expected_output += '\n'
            self.assertEqual(expected_output, result.stdout)


class AutograderSandboxBasicRunCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.sandbox = AutograderSandbox()

        self.root_cmd = ["touch", "/"]

    def test_run_legal_command_non_root(self):
        stdout_content = "hello world"
        with self.sandbox:
            cmd_result = self.sandbox.run_command(["echo", stdout_content])
            self.assertEqual(0, cmd_result.return_code)
            self.assertEqual(stdout_content + '\n', cmd_result.stdout)

    def test_run_illegal_command_non_root(self):
        with self.sandbox:
            cmd_result = self.sandbox.run_command(self.root_cmd)
            self.assertNotEqual(0, cmd_result.return_code)
            self.assertNotEqual("", cmd_result.stderr)

    def test_run_command_as_root(self):
        with self.sandbox:
            cmd_result = self.sandbox.run_command(self.root_cmd, as_root=True)
            self.assertEqual(0, cmd_result.return_code)
            self.assertEqual("", cmd_result.stderr)

    def test_run_command_raise_on_error(self):
        """
        Tests that an exception is thrown only when raise_on_failure is True
        and the command exits with nonzero status.
        """
        with self.sandbox:
            # No exception should be raised.
            cmd_result = self.sandbox.run_command(self.root_cmd,
                                                  as_root=True,
                                                  raise_on_failure=True)
            self.assertEqual(0, cmd_result.return_code)

            with self.assertRaises(subprocess.CalledProcessError):
                self.sandbox.run_command(self.root_cmd, raise_on_failure=True)


_STACK_USAGE_PROG_TMPL = """#include <iostream>

using namespace std;

int main()
{{
    char stacky[{num_bytes_on_stack}];
    cout << stacky << endl;
    return 0;
}}
"""


_HEAP_USAGE_PROG_TMPL = """#include <iostream>

using namespace std;

int main()
{{
    char* heapy = new char[{num_bytes_on_heap}];
    cout << heapy << endl;
    return 0;
}}
"""


_PROCESS_SPAWN_PROG_TMPL = """
import time
from multiprocessing import Pool

def f(x):
    print('function called')
    time.sleep(1)
    return x * x

if __name__ == '__main__':
    with Pool({num_processes}) as p:
        print(p.map(f, range({num_processes})))
"""


class AutograderSandboxResourceLimitTestCase(unittest.TestCase):
    def setUp(self):
        self.sandbox = AutograderSandbox()

        self.small_virtual_mem_limit = mb_to_bytes(100)
        self.large_virtual_mem_limit = gb_to_bytes(1)

    def test_run_command_timeout_exceeded(self):
        with self.sandbox:
            cmd_result = self.sandbox.run_command(["sleep", "10"], timeout=1)
            self.assertTrue(cmd_result.timed_out)

    def test_command_exceeds_process_limit(self):
        process_limit = 0
        prog = _PROCESS_SPAWN_PROG_TMPL.format(
            num_processes=process_limit + 2)
        with self.sandbox, tempfile.NamedTemporaryFile('w+') as f:
            f.write(prog)
            f.seek(0)
            self.sandbox.add_files(f.name)

            result = self.sandbox.run_command(
                ['python3', os.path.basename(f.name)],
                max_num_processes=process_limit)
            self.assertNotEqual(0, result.return_code)

    def test_command_doesnt_exceed_process_limit(self):
        process_limit = 10
        prog = _PROCESS_SPAWN_PROG_TMPL.format(
            num_processes=process_limit // 2)
        with self.sandbox, tempfile.NamedTemporaryFile('w+') as f:
            f.write(prog)
            f.seek(0)
            self.sandbox.add_files(f.name)

            result = self.sandbox.run_command(
                ['python3', os.path.basename(f.name)],
                max_num_processes=process_limit)
            self.assertEqual(0, result.return_code)

    def test_command_exceeds_stack_size_limit(self):
        stack_size_limit = mb_to_bytes(5)
        prog = _STACK_USAGE_PROG_TMPL.format(
            num_bytes_on_stack=stack_size_limit * 2)
        with self.sandbox, \
                tempfile.NamedTemporaryFile('w+', suffix='.cpp') as f:
            f.write(prog)
            f.seek(0)
            self.sandbox.add_files(f.name)

            exe_name = 'stacky'
            self.sandbox.run_command(
                ['g++', '-Wall', '-pedantic',
                 os.path.basename(f.name), '-o', exe_name])
            result = self.sandbox.run_command(
                ['./' + exe_name], max_stack_size=stack_size_limit)
            self.assertNotEqual(0, result.return_code)

    def test_command_doesnt_exceed_stack_size_limit(self):
        stack_size_limit = mb_to_bytes(30)
        prog = _STACK_USAGE_PROG_TMPL.format(
            num_bytes_on_stack=stack_size_limit // 2)
        with self.sandbox, \
                tempfile.NamedTemporaryFile('w+', suffix='.cpp') as f:
            f.write(prog)
            f.seek(0)
            self.sandbox.add_files(f.name)

            exe_name = 'stacky'
            self.sandbox.run_command(
                ['g++', '-Wall', '-pedantic',
                 os.path.basename(f.name), '-o', exe_name])
            result = self.sandbox.run_command(
                ['./' + exe_name], max_stack_size=stack_size_limit)
            self.assertEqual(0, result.return_code)

    def test_command_exceeds_virtual_mem_limit(self):
        virtual_mem_limit = mb_to_bytes(100)
        prog = _HEAP_USAGE_PROG_TMPL.format(
            num_bytes_on_heap=virtual_mem_limit * 2)
        with self.sandbox, \
                tempfile.NamedTemporaryFile('w+', suffix='.cpp') as f:
            f.write(prog)
            f.seek(0)
            self.sandbox.add_files(f.name)

            exe_name = 'heapy'
            self.sandbox.run_command(
                ['g++', '-Wall', '-pedantic',
                 os.path.basename(f.name), '-o', exe_name])
            result = self.sandbox.run_command(
                ['./' + exe_name],
                max_virtual_memory=virtual_mem_limit)

            self.assertNotEqual(0, result.return_code)

    def test_command_doesnt_exceed_virtual_mem_limit(self):
        virtual_mem_limit = mb_to_bytes(100)
        prog = _HEAP_USAGE_PROG_TMPL.format(
            num_bytes_on_heap=virtual_mem_limit // 2)
        with self.sandbox, \
                tempfile.NamedTemporaryFile('w+', suffix='.cpp') as f:
            f.write(prog)
            f.seek(0)
            self.sandbox.add_files(f.name)

            exe_name = 'heapy'
            self.sandbox.run_command(
                ['g++', '-Wall', '-pedantic',
                 os.path.basename(f.name), '-o', exe_name])
            result = self.sandbox.run_command(
                ['./' + exe_name],
                max_virtual_memory=virtual_mem_limit)

            self.assertEqual(0, result.return_code)

    def test_run_subsequent_commands_with_different_resource_limits(self):
        self.fail()

    def test_multiple_containers_dont_exceed_ulimits(self):
        """
        One quirk of docker containers is that if there are multiple users
        created in different containers but with the same UID, the resource
        usage of all those users will contribute to hitting the same ulimits.
        This test makes sure that the ulimits are set high enough that
        valid processes aren't randomly cut off.
        """
        self.fail()


_GOOGLE_IP_ADDR = "216.58.214.196"


class AutograderSandboxNetworkAccessTestCase(unittest.TestCase):
    def test_networking_disabled(self):
        with AutograderSandbox() as sandbox:
            result = sandbox.run_command(['ping', '-c', '5', _GOOGLE_IP_ADDR])
            self.assertNotEqual(0, result.return_code)

    def test_run_command_access_ip_address_whitelist(self):
        self.fail()


class AutograderSandboxCopyFilesTestCase(unittest.TestCase):
    def test_copy_files_into_sandbox(self):
        files = []
        try:
            for i in range(10):
                f = tempfile.NamedTemporaryFile(mode='w+')
                f.write('this is file {}'.format(i))
                f.seek(0)
                files.append(f)

            filenames = [file_.name for file_ in files]

            with AutograderSandbox() as sandbox:
                sandbox.add_files(*filenames)

                ls_result = sandbox.run_command(['ls'])
                actual_filenames = [
                    filename.strip() for filename in ls_result.stdout.split()]
                expected_filenames = [
                    os.path.basename(filename) for filename in filenames]
                self.assertCountEqual(expected_filenames, actual_filenames)

                for file_ in files:
                    file_.seek(0)
                    expected_content = file_.read()
                    actual_content = sandbox.run_command(
                        ['cat', os.path.basename(file_.name)]).stdout
                    self.assertEqual(expected_content, actual_content)
        finally:
            for file_ in files:
                file_.close()

    def test_copy_and_rename_file_into_sandbox(self):
        self.fail()
