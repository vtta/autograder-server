from django.contrib.auth.models import User
from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema

from rest_framework import (
    viewsets, mixins, permissions, response, status)

import autograder.core.models as ag_models
import autograder.rest_api.serializers as ag_serializers
import autograder.rest_api.permissions as ag_permissions
from autograder.rest_api.views.ag_model_views import ListNestedModelViewSet, require_body_params

from .permissions import IsAdminOrReadOnlyStaff

from ..load_object_mixin import build_load_object_mixin


_add_staff_params = [
    Parameter(
        'new_staff',
        'body',
        type='List[string]',
        required=True,
        description='A list of usernames who should be granted staff '
                    'privileges for this course.'
    )
]


_remove_staff_params = [
    Parameter(
        'remove_staff',
        'body',
        type='List[string]',
        required=True,
        description='A list of usernames whose staff privileges '
                    'should be revoked for this course.'
    )
]


class CourseStaffViewSet(ListNestedModelViewSet):
    serializer_class = ag_serializers.UserSerializer
    permission_classes = (ag_permissions.is_admin_or_read_only_staff(),)

    model_manager = ag_models.Course.objects
    reverse_to_one_field_name = 'staff'

    @swagger_auto_schema(overrides={'request_body_parameters': _add_staff_params},
                         responses={'204': ''})
    @transaction.atomic()
    @method_decorator(require_body_params('new_staff'))
    def post(self, request, *args, **kwargs):
        course = self.get_object()
        self.add_staff(course, request.data['new_staff'])

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(overrides={'request_body_parameters': _remove_staff_params},
                         responses={'204': ''})
    @transaction.atomic()
    @method_decorator(require_body_params('remove_staff'))
    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        self.remove_staff(course, request.data['remove_staff'])

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def add_staff(self, course, usernames):
        staff_to_add = [
            User.objects.get_or_create(username=username)[0]
            for username in usernames]
        course.staff.add(*staff_to_add)

    def remove_staff(self, course, users_json):
        staff_to_remove = User.objects.filter(
            pk__in=[user['pk'] for user in users_json])
        course.staff.remove(*staff_to_remove)
