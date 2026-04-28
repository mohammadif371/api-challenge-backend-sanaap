from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Full access - admin only"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsEditor(BasePermission):
    """Upload and update - no delete"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_editor() or request.user.is_admin()
        )


class IsViewer(BasePermission):
    """Read only - viewer role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_viewer() or request.user.is_editor() or request.user.is_admin()
        )