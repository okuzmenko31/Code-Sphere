from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object
    or admins to edit it. Assumes the model instance
    has an `creator` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or (request.user.is_authenticated
                                                          and request.user.is_admin):
            return True
        return obj.creator == request.user
