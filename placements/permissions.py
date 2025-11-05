from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'Admin'

class IsStudentOwner(permissions.BasePermission):
    """
    Custom permission to only allow student owners of an object to view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.student.user == request.user
