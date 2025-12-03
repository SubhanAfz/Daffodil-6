from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotAllowed, HttpRequest
from recipes.models import Recipe, Report
from recipes.forms import ReportForm


@login_required
def report_recipe(request: HttpRequest, recipe_id):
    """
    Report a specific recipe for review.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = ReportForm(request.POST)

    if form.is_valid():
        Report.objects.update_or_create(
            reporter=request.user,
            recipe=recipe,
            defaults={"reason": form.cleaned_data["reason"]},
        )
    else:
        Report.objects.update_or_create(
            reporter=request.user,
            recipe=recipe,
            defaults={"reason": "No reason provided."},
        )

    return redirect("recipe_detail", recipe_id=recipe.id)
