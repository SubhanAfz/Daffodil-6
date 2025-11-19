from django.contrib import admin

# Register your models here.
from recipes.models import Recipe
admin.site.register(Recipe)

from recipes.models import User
admin.site.register(User)