import django.db.models as models


# e.g. chicken, flour, tomato
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
