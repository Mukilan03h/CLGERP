from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'Admin'

class IsFacultyOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow faculty to create, update, or delete objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role != 'Faculty':
            return False
        if request.method == 'POST':
            subject_id = request.data.get('subject')
            if subject_id:
                from attendance.models import Subject
                subject = Subject.objects.get(id=subject_id)
                return subject in request.user.faculty.subjects.all()
        return True

class IsStudentOwner(permissions.BasePermission):
    """
    Custom permission to only allow student owners of an object to view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.student.user == request.user
