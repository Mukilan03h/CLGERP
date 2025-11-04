from django.db import models
from auth_app.models import User

class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:20]}..."
