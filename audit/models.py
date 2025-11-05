from django.db import models
from auth_app.models import User

class ActivityLog(models.Model):
    """
    Represents a log of a user's activity in the system.
    """
    ACTION_CHOICES = [
        ('Create', 'Create'),
        ('Read', 'Read'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
        ('Login', 'Login'),
        ('Logout', 'Logout'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action_type} at {self.timestamp}"
