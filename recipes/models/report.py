from django.db import models

from recipes.models.recipe import Recipe
from recipes.models.user import User


class Report(models.Model):
    """Model for one report of a post/recipe."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=1200)
    report_time = models.DateTimeField(auto_now_add=True)

    def report_str(self):
        """Return a string describing info of the report."""
        return f'"{self.recipe.title}" by {self.recipe.author.username}. This post has been reported a total of {self.recipe.num_reports} time(s). The reason given is: "{self.reason}"'
