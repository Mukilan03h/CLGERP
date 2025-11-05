from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsOwnerOrAdmin(BasePermission):
    """
    Allows access only to the object owner or admin users.
    Assumes the model instance has a `faculty` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True

        # Check if the obj has a 'faculty' attribute
        if hasattr(obj, 'faculty'):
            return obj.faculty.user == request.user

        # Check if the obj is a Payslip and check its faculty owner
        if hasattr(obj, 'payslip') and hasattr(obj.payslip, 'faculty'):
            return obj.payslip.faculty.user == request.user

        return False
