# ruff: noqa: F401
# note to contributor: remove this comment above when it is completed (all the imports are used)
from django.contrib import admin
from recipes.models import User, Recipe, Like, Favourite, Tag, Follow, Report, Notification

# Register your models here.
admin.site.register(Recipe)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Favourite)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Report)
admin.site.register(Notification)
