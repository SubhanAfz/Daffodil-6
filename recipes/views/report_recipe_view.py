from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotAllowed, HttpResponse
from recipes.models import Recipe, Report


@login_required
def report_recipe(request: HttpResponse, recipe_id):
    """
    Report a specific recipe for review.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    recipe = get_object_or_404(Recipe, id=recipe_id)
    report_text = request.POST.get("report_text", "").strip()
    if not report_text:
        return redirect("recipe_detail", recipe_id=recipe.id)
    try:
        report = Report.objects.get(reporter=request.user, recipe=recipe)
        report.reason = report_text
        report.save()
    except Report.DoesNotExist:
        Report.objects.create(reporter=request.user, recipe=recipe, reason=report_text)
    return redirect("recipe_detail", recipe_id=recipe.id)
