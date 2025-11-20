# ruff: noqa: F401
# note to contributor: remove this comment above when it is completed (all the imports are used)
from django.contrib import admin
from recipes.models import User
# Register your models here.
from recipes.models import Recipe
admin.site.register(Recipe)
admin.site.register(User)