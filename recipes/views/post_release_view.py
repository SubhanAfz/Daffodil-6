from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from recipes.models.recipe import Recipe
from recipes.models.report import Report


@login_required
def post_release(request, id):
    """Release a post back to public view by users.

    Retrieves the appropriate post by ID and gives 404 if no post found. It gives error 403 if the user
    does not have permission to release posts. Then sets thepsot to public and deletes all it's reports."""
    post = get_object_or_404(Recipe, id=id)

    if not request.user.is_superuser:
        return render(request, "403_error.html")

    if request.method == "POST":
        post.set_public()
        post.set_reports(0)
        post.save()
        Report.objects.filter(recipe=post).delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))

    return render(request, "405_error.html")
