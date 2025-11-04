from .models import ActivityLog

class AuditTrailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.method not in ['GET', 'HEAD', 'OPTIONS']:
            ActivityLog.objects.create(
                user=request.user,
                action_type=self.get_action_type(request.method),
                description=f"Accessed {request.path}",
                ip_address=self.get_client_ip(request)
            )

        return response

    def get_action_type(self, method):
        if method == 'POST':
            return 'Create'
        elif method == 'PUT' or method == 'PATCH':
            return 'Update'
        elif method == 'DELETE':
            return 'Delete'
        return 'Read'

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
