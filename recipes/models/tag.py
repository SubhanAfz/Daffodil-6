from django.db import models

from recipes.models import Recipe


# e.g. chinese, italian, spicy etc
class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    recipes = models.ManyToManyField(Recipe, related_name="tags")

    def __str__(self):
        return self.name
