from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows safe methods for any authenticated user, but only admins for write methods.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsStudentOwnerOrAdmin(BasePermission):
    """
    Allows access only to the student who owns the application or an admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
        return obj.student.user == request.user
