from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsStudentOwner(permissions.BasePermission):
    """
    Allows access only to the student who owns the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.student.user == request.user
