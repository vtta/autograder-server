import os

from django.conf import settings

import autograder.shared.global_constants as gc


def check_user_provided_filename(filename):
    """
    Verifies whether the given filename is valid according to the
    following requirements:
        - Filenames must be non-empty and non-null
        - Filenames must only contain the characters specified in
          autograder.shared.global_constants.PROJECT_FILENAME_WHITELIST_REGEX
        - Filenames cannot be the string ".."
        - Filenames cannot start with '.'

    If the given filename does not meet these requirements, ValueError
    is raised. These restrictions are placed on filenames for security
    purposes.
    """
    if not filename:
        raise ValueError("Filenames must be non-empty and non-null")

    if filename.startswith('.'):
        raise ValueError("Filenames cannot start with '.'")

    if filename == "..":
        raise ValueError("'..' is not a valid filename")

    if not gc.PROJECT_FILENAME_WHITELIST_REGEX.fullmatch(filename):
        raise ValueError(
            "Invalid filename: {0} \n"
            "Filenames must contain only alphanumeric characters, hyphen, "
            "underscore, and period.".format(filename))


# -----------------------------------------------------------------------------

def check_shell_style_file_pattern(pattern):
    """
    Verified whether the given file pattern is valid according to the
    following requirements:
        - Patterns must be non-empty and non-null
        - Filenames myst only contain characters specified in
          autograder.shared.global_constants.PROJECT_FILE_PATTERN_WHITELIST_REGEX

    If the given pattern does not meet these requirements, ValueError
    is raised. These restrictions are placed on file patterns for security
    purposes.
    """
    if not pattern:
        raise ValueError("File patterns must be non-empty and non-null")

    if not gc.PROJECT_FILE_PATTERN_WHITELIST_REGEX.fullmatch(pattern):
        raise ValueError(
            "Invalid file pattern: {0} \n"
            "Shell-style patterns must only contain "
            "alphanumeric characters, hyphen, underscore, "
            "period, * ? [ ] and !".format(pattern))


# -----------------------------------------------------------------------------

def get_course_root_dir(course):
    """
    Computes the absolute path of the root directory for the given course.
    For example: {MEDIA_ROOT}/courses/eecs280

    NOTE: DO NOT COMPUTE COURSE ROOT DIRECTORIES MANUALLY.
          ALWAYS DO SO BY USING THIS FUNCTION.
          This will allow for the filesystem layout to be easily
          modified if necessary.
    """
    return os.path.join(settings.MEDIA_ROOT, 'courses', course.name)


# -----------------------------------------------------------------------------

def get_semester_root_dir(semester):
    """
    Computes the absolute path of the root directory for the given semester.
    For example: {MEDIA_ROOT}/courses/eecs280/fall2015

    NOTE: DO NOT COMPUTE SEMESTER ROOT DIRECTORIES MANUALLY.
          ALWAYS DO SO BY USING THIS FUNCTION.
          This will allow for the filesystem layout to be easily
          modified if necessary.
    """
    return os.path.join(get_course_root_dir(semester.course), semester.name)


# -----------------------------------------------------------------------------

def get_project_root_dir(project):
    """
    Computes the absolute path of the root directory for the given project.
    For example: {MEDIA_ROOT}/courses/eecs280/fall2015/project3

    NOTE: DO NOT COMPUTE PROJECT ROOT DIRECTORIES MANUALLY.
          ALWAYS DO SO BY USING THIS FUNCTION.
          This will allow for the filesystem layout to be easily
          modified if necessary.
    """
    return os.path.join(
        get_semester_root_dir(project.semester), project.name)


# -----------------------------------------------------------------------------

def get_project_files_dir(project):
    """
    Computes the absolute path of the directory where uploaded files
    should be stored for the given project.
    For example: {MEDIA_ROOT}/courses/eecs280/fall2015/project3/project_files

    NOTE: DO NOT COMPUTE THIS PATH MANUALLY.
          ALWAYS DO SO BY USING THIS FUNCTION.
          This will allow for the filesystem layout to be easily
          modified if necessary.
    """
    return os.path.join(
        get_project_root_dir(project), gc.PROJECT_FILES_DIRNAME)


# -----------------------------------------------------------------------------

def get_project_submissions_by_student_dir(project):
    """
    Computes the absolute path of the directory where student submissions
    should be stored for the given project.
    For example:
        {MEDIA_ROOT}/courses/eecs280/fall2015/project3/submissions_by_student
    """
    return os.path.join(
        get_project_root_dir(project), gc.PROJECT_SUBMISSIONS_DIRNAME)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class ChangeDirectory(object):
    """
    Enables moving into and out of a given directory using "with" statements.
    """
    def __init__(self, new_dir):
        self._original_dir = os.getcwd()
        self._new_dir = new_dir

    def __enter__(self):
        os.chdir(self._new_dir)

    def __exit__(self, *args):
        os.chdir(self._original_dir)