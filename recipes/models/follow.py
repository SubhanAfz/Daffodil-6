from django.db import models
from django.conf import settings


class Follow(models.Model):
    """Model representing a user following another user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers_of"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "follower")

    def __str__(self):
        return f"{self.follower} follows {self.user}"
