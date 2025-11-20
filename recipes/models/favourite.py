from django.db import models
from django.conf import settings
from .recipe import Recipe

class Favourite(models.Model):
    """Model representing a user's favourite recipe."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favourited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} favourites {self.recipe}'
