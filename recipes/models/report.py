import django.db.models as models

from recipes.models.recipe import Recipe
from recipes.models.user import User

class Report (models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User)
    reason = models.CharField(max_length=1200)
    report_time = models.DateTimeField()