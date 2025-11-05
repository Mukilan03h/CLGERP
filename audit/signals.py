from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import ActivityLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Log user login events.
    """
    ActivityLog.objects.create(
        user=user,
        action_type='Login',
        description=f"User {user.username} logged in.",
        ip_address=get_client_ip(request)
    )
