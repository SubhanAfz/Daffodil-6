import django.db.models as models


# e.g. chinese, italian, spicy etc
class Tag(models.Model):
    name = models.CharField(max_length=200)
