from rest_framework import permissions

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

class IsFacultyOwner(permissions.BasePermission):
    """
    Allows access only to the faculty member who owns the object.
    """
    message = 'You can only manage your own timetable.'

    def has_permission(self, request, view):
        # This check is for the 'create' action (POST)
        if request.method == 'POST':
            faculty_id = request.data.get('faculty')
            # If no faculty is provided, deny permission
            if not faculty_id:
                return False

            try:
                # Check if the faculty user is the same as the one being assigned
                return request.user.faculty.id == int(faculty_id)
            except (AttributeError, ValueError):
                # User is not a faculty/has no profile or invalid faculty_id
                return False

        # For other request methods (GET, PUT, etc.), let has_object_permission handle it
        return True

    def has_object_permission(self, request, view, obj):
        # This check is for 'retrieve', 'update', 'destroy' actions on a specific object
        try:
            return obj.faculty.user == request.user
        except AttributeError:
            # User is not a faculty or has no faculty profile
            return False
