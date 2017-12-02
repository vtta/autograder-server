import fnmatch
import os
import shlex
import tempfile
import traceback

import time
from io import FileIO
from typing import Union

from autograder_sandbox import AutograderSandbox
from autograder_sandbox import SANDBOX_USERNAME
from autograder_sandbox.autograder_sandbox import CompletedCommand
from django.conf import settings
from django.db import transaction

import autograder.core.models as ag_models
import autograder.core.utils as core_ut
from autograder.core import constants


class MaxRetriesExceeded(Exception):
    pass


def retry(max_num_retries,
          retry_delay_start=0,
          retry_delay_end=0,
          retry_delay_step=None):
    """
    Returns a decorator that applies a synchronous retry loop to the
    decorated function.

    :param max_num_retries: The maximum number of times the decorated
        function can be retried before raising an exception. This
        parameter must be greater than zero.

    :param retry_delay_start: The delay time, in seconds, before retrying
        the function for the first time.

    :param retry_delay_end: The delay time, in seconds, before retrying
        the function for the last time.

    :param retry_delay_step: The number of seconds to increase the retry
        delay for each consecutive retry. If None, defaults to
        (retry_delay_end - retry_delay_start) / max_num_retries
    """
    if retry_delay_step is None:
        retry_delay_step = (retry_delay_end - retry_delay_start) / max_num_retries

    def decorator(func):
        def func_with_retry(*args, **kwargs):
            num_retries_remaining = max_num_retries
            retry_delay = retry_delay_start
            latest_exception = None
            while num_retries_remaining >= 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # TODO: handle certain database errors differently
                    print('Error in', func.__name__)
                    traceback.print_exc()
                    print('Will try again in', retry_delay, 'seconds')
                    num_retries_remaining -= 1
                    time.sleep(retry_delay)
                    retry_delay += retry_delay_step
                    latest_exception = traceback.format_exc()

            raise MaxRetriesExceeded(latest_exception)

        return func_with_retry

    return decorator


# Specialization of the "retry" decorator to be used for synchronous
# tasks that should always succeed unless there is a database issue.
retry_should_recover = retry(max_num_retries=60,
                             retry_delay_start=1, retry_delay_end=60)
# Specialization of the "retry" to be used for grading non-deferred
# autograder test cases.
retry_ag_test_cmd = retry(max_num_retries=settings.AG_TEST_MAX_RETRIES,
                          retry_delay_start=settings.AG_TEST_MIN_RETRY_DELAY,
                          retry_delay_end=settings.AG_TEST_MAX_RETRY_DELAY)


@retry_should_recover
def mark_submission_as_error(submission_pk, error_msg):
    with transaction.atomic():
        ag_models.Submission.objects.select_for_update().filter(
            pk=submission_pk
        ).update(status=ag_models.Submission.GradingStatus.error, error_msg=error_msg)


def add_files_to_sandbox(sandbox: AutograderSandbox,
                         suite: Union[ag_models.AGTestSuite, ag_models.StudentTestSuite],
                         submission: ag_models.Submission):
    student_files_to_add = []
    for student_file in suite.student_files_needed.all():
        matching_files = fnmatch.filter(submission.submitted_filenames,
                                        student_file.pattern)
        student_files_to_add += [
            os.path.join(core_ut.get_submission_dir(submission), filename)
            for filename in matching_files]

    if student_files_to_add:
        sandbox.add_files(*student_files_to_add)

    project_files_to_add = [file_.abspath for file_ in suite.project_files_needed.all()]
    if project_files_to_add:
        owner_and_read_only = {
            'owner': 'root' if suite.read_only_project_files else SANDBOX_USERNAME,
            'read_only': suite.read_only_project_files
        }
        sandbox.add_files(*project_files_to_add, **owner_and_read_only)


def run_ag_command(cmd: ag_models.AGCommand,
                   sandbox: AutograderSandbox,
                   ag_test_suite_result: ag_models.AGTestSuiteResult=None,
                   cmd_str_override: str=None) -> CompletedCommand:
    with FileCloser() as file_closer:
        stdin = get_stdin_file(cmd, ag_test_suite_result)
        file_closer.register_file(stdin)

        cmd_str = cmd_str_override if cmd_str_override is not None else cmd.cmd
        return run_command_from_args(cmd=cmd_str,
                                     sandbox=sandbox,
                                     max_num_processes=cmd.process_spawn_limit,
                                     max_stack_size=cmd.stack_size_limit,
                                     max_virtual_memory=cmd.virtual_memory_limit,
                                     timeout=cmd.time_limit,
                                     stdin=stdin)


def run_command_from_args(cmd: str,
                          sandbox: AutograderSandbox,
                          max_num_processes: int,
                          max_stack_size: int,
                          max_virtual_memory: int,
                          timeout: int,
                          stdin=None) -> CompletedCommand:
    run_result = sandbox.run_command(shlex.split(cmd),
                                     stdin=stdin,
                                     as_root=False,
                                     max_num_processes=max_num_processes,
                                     max_stack_size=max_stack_size,
                                     max_virtual_memory=max_virtual_memory,
                                     timeout=timeout,
                                     truncate_stdout=constants.MAX_OUTPUT_LENGTH,
                                     truncate_stderr=constants.MAX_OUTPUT_LENGTH)
    return run_result


def get_stdin_file(cmd: ag_models.AGCommand,
                   ag_test_suite_result: ag_models.AGTestSuiteResult=None) -> FileIO:
    if cmd.stdin_source == ag_models.StdinSource.text:
        stdin = tempfile.NamedTemporaryFile()
        stdin.write(cmd.stdin_text.encode())
        stdin.flush()
        stdin.seek(0)
        return stdin
    elif cmd.stdin_source == ag_models.StdinSource.project_file:
        return cmd.stdin_project_file.open('rb')
    elif cmd.stdin_source == ag_models.StdinSource.setup_stdout:
        if ag_test_suite_result is None:
            raise Exception('Expected ag test suite result, but got None.')

        return ag_test_suite_result.open_setup_stdout('rb')
    elif cmd.stdin_source == ag_models.StdinSource.setup_stderr:
        if ag_test_suite_result is None:
            raise Exception('Expected ag test suite result, but got None.')

        return ag_test_suite_result.open_setup_stderr('rb')
    else:
        return None


class FileCloser:
    def __init__(self):
        self._files_to_close = []  # type: List[FileIO]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for file_ in self._files_to_close:
            file_.close()

    def register_file(self, file_: FileIO):
        if file_ is None:
            return
        self._files_to_close.append(file_)