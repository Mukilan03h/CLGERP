from rest_framework.permissions import BasePermission

class IsAccountantOrAdmin(BasePermission):
    """
    Custom permission to only allow accountants or admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'Admin' or request.user.role == 'Accountant')
