from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Model representing a user following another user."""

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_received",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_sent",
    )
    notification_type = models.CharField(
        max_length=20,
        choices=[
            ("like", "liked your recipe"),
            ("favourite", "favourited your recipe"),
            ("follow", "started following you"),
            ("default", "You have a new notification"),
        ],
    )
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
