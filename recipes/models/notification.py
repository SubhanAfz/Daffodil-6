from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Model representing a notification for a user."""

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
        null=False,
        max_length=20,
        choices=[
            ("like", "liked your recipe"),
            ("favourite", "favourited your recipe"),
            ("follow", "started following you"),
            ("default", "You have a new notification"),
        ],
    )
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipient", "sender", "notification_type", "link"],
                name="unique_notification",
            )
        ]

    def __str__(self):
        return f"Notification for {self.recipient.username} from {self.sender.username} ({self.notification_type})"
