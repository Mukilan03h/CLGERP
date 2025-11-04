from rest_framework import permissions
from attendance.models import Subject

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsFacultyUser(permissions.BasePermission):
    """
    Allows access only to faculty users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Faculty'

class IsStudentUser(permissions.BasePermission):
    """
    Allows access only to student users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Student'

class IsStudentOwner(permissions.BasePermission):
    """
    Allows access only to the student who owns the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.student.user == request.user

class IsFacultyForSubject(permissions.BasePermission):
    """
    Allows access only to the faculty member who teaches the subject.
    """
    message = 'You do not have permission to perform this action for this subject.'

    def has_permission(self, request, view):
        # This check is for the 'create' action (POST)
        if request.method == 'POST':
            subject_id = request.data.get('subject')
            # If no subject is provided, deny permission
            if not subject_id:
                return False

            try:
                # Check if the faculty user is associated with the subject
                subject = Subject.objects.get(pk=subject_id)
                return request.user.faculty.subjects.filter(pk=subject.pk).exists()
            except (Subject.DoesNotExist, AttributeError):
                # Subject doesn't exist or user is not a faculty/has no profile
                return False

        # For other request methods (GET, PUT, etc.), let has_object_permission handle it
        return True

    def has_object_permission(self, request, view, obj):
        # This check is for 'retrieve', 'update', 'destroy' actions on a specific object
        try:
            return obj.subject in request.user.faculty.subjects.all()
        except AttributeError:
            # User is not a faculty or has no faculty profile
            return False
