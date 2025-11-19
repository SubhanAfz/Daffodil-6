import django.db.models as models

from recipes.models.user import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField()
    is_reported = models.BooleanField()
    num_reports = models.IntegerField()

    def report_info_str(self):
        if not self.is_reported:
            return f'This recipe has not been reported.'
        else:
            return f'"{self.title}" by {self.author.username} has been reported {self.num_reports} times.'

            
        
