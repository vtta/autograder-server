from rest_framework import viewsets, mixins, permissions

import autograder.rest_api.serializers as ag_serializers
import autograder.core.models as ag_models


class CoursePermissions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            return request.user.is_superuser

        return True

    def has_object_permission(self, request, view, course):
        if view.action == 'retrieve':
            return True

        return course.is_administrator(request.user)


class CourseViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ag_serializers.CourseSerializer
    permission_classes = (CoursePermissions,)

    def get_queryset(self):
        return ag_models.Course.objects.all()
