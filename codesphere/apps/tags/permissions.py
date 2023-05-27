from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Permission to only allow admins to edit, add or update tags.
    Users can only read the tags.
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        if request.method in permissions.SAFE_METHODS or is_admin:
            return True
        return False
