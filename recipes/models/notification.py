from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


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
        null=False,
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
        constraints = [
            models.ordering.OrderingConstraint(
                fields=["-created_at"], name="ordering_by_created_at"
            ),
            models.UniqueConstraint(
                fields=["recipient", "sender", "notification_type", "link"],
                name="unique_notification",
            ),
        ]

    def clean(self):
        """Model-level validation: prevent self-notifications."""
        if self.recipient_id and self.sender_id and self.recipient_id == self.sender_id:
            raise ValidationError("Recipient and sender must be different users.")

    def save(self, *args, **kwargs):
        # run model validation before saving (raises ValidationError on failure)
        self.full_clean()
        super().save(*args, **kwargs)
