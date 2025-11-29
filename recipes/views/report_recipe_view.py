from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotAllowed, HttpRequest
from recipes.models import Recipe, Report


@login_required
def report_recipe(request: HttpRequest, recipe_id):
    """
    Report a specific recipe for review.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    recipe = get_object_or_404(Recipe, id=recipe_id)
    report_text = request.POST.get("report_text", "").strip()
    if report_text == "":
        report_text = "No reason provided."
    Report.objects.update_or_create(
        reporter=request.user,
        recipe=recipe,
        defaults={'reason': report_text}
    )
    return redirect("recipe_detail", recipe_id=recipe.id)
