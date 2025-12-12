from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Django app configuration for the recipes app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self):  # noqa
        from . import signals  # noqa
