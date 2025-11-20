from django.contrib import admin
from recipes.models import User
# Register your models here.
from recipes.models import Recipe
admin.site.register(Recipe)
admin.site.register(User)