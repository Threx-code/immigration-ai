from rest_framework import permissions


class IsReviewer(permissions.BasePermission):
    """
    Custom permission to only allow reviewers to access the view.
    Reviewer must have role='reviewer' AND be staff or superuser.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated, has reviewer role, and is staff or superuser
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'reviewer' and
            (request.user.is_staff or request.user.is_superuser)
        )

