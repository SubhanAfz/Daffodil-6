from django.db import models
from django.utils import timezone

from recipes.models.user import User


class Recipe(models.Model):
    """Model representing a recipe with content, author, and moderation fields."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    is_reported = models.BooleanField(default=False)
    num_reports = models.IntegerField(default=0)
    is_hidden = models.BooleanField(default=False)
    date_hidden = models.DateTimeField(null=True, default=None)
    thumbnail = models.ImageField(
        upload_to="thumbnails/", null=True, blank=True, default=None
    )

    def report_info_str(self):
        """Return a string describing the recipe's report status."""
        if not self.is_reported:
            return f'This recipe "{self.title}" has not been reported.'
        else:
            return f'"{self.title}" by {self.author.username} has been reported {self.num_reports} times.'

    def set_hidden(self):
        """Mark the recipe as hidden and record the timestamp."""
        self.is_hidden = True
        self.date_hidden = timezone.now()

    def set_public(self):
        """Mark the recipe as public and clear the hidden timestamp."""
        self.is_hidden = False
        self.date_hidden = None

    def set_reports(self, num):
        """Set the number of reports and update the is_reported flag."""
        self.num_reports = num
        self.is_reported = num > 0
