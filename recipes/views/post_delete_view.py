from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed
from recipes.models.recipe import Recipe
from recipes.models.report import Report


@login_required
def post_delete(request, id):
    """Deletes a post using the ID from the database.
    It identifies if the user making the request has permission to delete posts/recipes.
    """
    post = get_object_or_404(Recipe, id=id)

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        Report.objects.filter(recipe=post).delete()
        post.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return HttpResponseNotAllowed(["POST"])
