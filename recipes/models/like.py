from django.db import models
from django.conf import settings
from .recipe import Recipe


class Like(models.Model):
    """Model representing a user's like on a recipe."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="liked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user} likes {self.recipe.title}"
