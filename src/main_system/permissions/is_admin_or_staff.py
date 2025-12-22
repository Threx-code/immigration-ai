from rest_framework import permissions


class IsAdminOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow admin (superuser) or staff users to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is either superuser or staff
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_superuser or request.user.is_staff)
        )

