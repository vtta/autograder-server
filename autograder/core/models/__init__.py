# Import all Model classes here.

from .ag_model_base import AutograderModel, PolymorphicAutograderModel

from .notification import Notification

from .course import Course
from .semester import Semester
from .project import Project
from .project.expected_student_file_pattern import ExpectedStudentFilePattern
from .project.required_student_file import RequiredStudentFile
from .project.uploaded_file import UploadedFile

from .submission_group import SubmissionGroup, SubmissionGroupInvitation
from .submission import Submission

# These next imports need to be in this order to get around
# circular dependency.
from .autograder_test_case_result import AutograderTestCaseResult
# Note: Even though we are importing the different types of test cases here,
# you should only access them through the factory function below
from .autograder_test_case.autograder_test_case_base import AutograderTestCaseBase
from .autograder_test_case.compiled_autograder_test_case import CompiledAutograderTestCase
from .autograder_test_case.compiled_and_run_autograder_test_case import CompiledAndRunAutograderTestCase
from .autograder_test_case.compilation_only_autograder_test_case import CompilationOnlyAutograderTestCase
from .autograder_test_case.interpreted_autograder_test_case import InterpretedAutograderTestCase

from .autograder_test_case.feedback_config import FeedbackConfig

from .autograder_test_case import AutograderTestCaseFactory
