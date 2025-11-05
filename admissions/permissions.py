from rest_framework import permissions

class IsAdmissionsStaff(permissions.BasePermission):
    """
    Custom permission to only allow admissions staff to approve or reject applications.
    """
    def has_permission(self, request, view):
        return request.user.role in ['Admin', 'AdmissionOfficer']
