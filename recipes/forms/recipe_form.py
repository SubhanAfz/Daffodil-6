from django import forms
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    """Recipe form.

    Describes fields that the user can effect and declares that the widgets of "description" and "content" can
    be resized both vertically and horizontally.

    """

    class Meta:
        model = Recipe
        fields = ["title", "description", "ingredients", "content", "thumbnail"]

        widgets = {
            "description": forms.Textarea(attrs={"style": "form-control", "rows": 3}),
            "ingredients": forms.Textarea(attrs={"style": "form-control", "rows": 6}),
            "content": forms.Textarea(attrs={"style": "form-control", "rows": 8}),
        }
