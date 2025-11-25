from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from recipes.models.recipe import Recipe


@login_required
def post_hide(request, id):
    """Hide a post from public view by users.

    Retrieves the post by relevant ID and gives 404 if there is no appropriate post. It then checks if the user
    making the request has permission to hide posts, and hides the post if the user does."""
    post = get_object_or_404(Recipe, id=id)

    if not request.user.is_staff:
        return render(request, "403_error.html")

    if request.method == "POST":
        post.set_hidden()
        post.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))

    return render(request, "405_error.html")
