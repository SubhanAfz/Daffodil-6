from django import forms
from recipes.models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    """Recipe form.

    Describes fields that the user can effect and declares that the widgets of "description" and "content" can
    be resized both vertically and horizontally.

    """

    tags_input = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"style": "form-control", "rows": 2, "placeholder": "for example: dessert, chocolate, easy"}),
        label="Tags",
        help_text="Enter tags separated by commas."
    )

    class Meta:
        model = Recipe
        fields = ["title", "description", "ingredients", "content", "thumbnail"]

        widgets = {
            "description": forms.Textarea(attrs={"style": "form-control", "rows": 3}),
            "ingredients": forms.Textarea(attrs={"style": "form-control", "rows": 6}),
            "content": forms.Textarea(attrs={"style": "form-control", "rows": 8}),
        }

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        
        if commit:
            recipe.tags.clear()
            
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    tag.recipes.add(recipe)
        
        return recipe
