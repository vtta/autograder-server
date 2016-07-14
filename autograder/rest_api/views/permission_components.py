from rest_framework import permissions


def is_admin_or_read_only_staff(request, course):
    is_admin = course.is_administrator(request.user)
    staff_and_read_only = (course.is_course_staff(request.user) and
                           request.method in permissions.SAFE_METHODS)
    return is_admin or staff_and_read_only


def user_can_view_project(user, project):
    if (project.course.is_administrator(user) or
            project.course.is_course_staff(user)):
        return True

    if not project.visible_to_students:
        return False

    if project.course.is_enrolled_student(user):
        return True

    return project.allow_submissions_from_non_enrolled_students


def user_can_view_group(user, group):
    if not user_can_view_project(user, group.project):
        return False

    if (group.project.course.is_administrator(user) or
            group.project.course.is_course_staff(user)):
        return True

    return group.members.filter(pk=user.pk).exists()