from django.db import models
from django.conf import settings

class Follow(models.Model):
    """Model representing a user following another user."""

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )
    by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    notification_type = models.CharField(max_length=20, choices=[
        ('like', 'Like'),
        ('favourite', 'Favourite'),
        ('follow', 'Follow'),
    ])
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_notification_message(self):
        """
        Generate a notification message based on the type of notification.
        """
        match self.notification_type:
            case 'like':
                return f"{self.by_user} liked your recipe."
            case 'favourite':
                return f"{self.by_user} favourited your recipe."
            case 'follow':
                return f"{self.by_user} started following you."
            case _:
                return "You have a new notification."
