from rest_framework import permissions


class IsEventCreator(permissions.BasePermission):
    """
    Custom permission to only allow creators of an event to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user