from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'Admin' role to access an endpoint.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'
