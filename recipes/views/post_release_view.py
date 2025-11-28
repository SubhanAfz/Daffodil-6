from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed
from recipes.models.recipe import Recipe
from recipes.models.report import Report


@login_required
def post_release(request, id):
    """Release a post back to public view by users.

    Retrieves the appropriate post by ID and gives 404 if no post found. It gives error 403 if the user
    does not have permission to release posts. Then sets thepsot to public and deletes all it's reports."""
    post = get_object_or_404(Recipe, id=id)

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        post.set_public()
        post.set_reports(0)
        post.save()
        Report.objects.filter(recipe=post).delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return HttpResponseNotAllowed(["POST"])
