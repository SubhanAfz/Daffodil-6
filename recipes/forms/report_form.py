from django import forms
from recipes.models import Report


class ReportForm(forms.ModelForm):
    """
    Form for reporting a recipe.
    Fields:
        reason (CharField): The reason why the user is reporting the recipe.
    """

    class Meta:
        model = Report
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Why are you reporting this recipe?",
                }
            )
        }
        labels = {"reason": "Why are you reporting this recipe?"}
