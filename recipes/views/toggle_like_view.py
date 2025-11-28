from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from recipes.models import Like, Recipe


@login_required
def toggle_like(request, recipe_id):
    """
    Toggle the like status for a specific recipe by the current user.
    """
    if request.method != "POST":
        return render(request, "405_error.html")

    recipe = get_object_or_404(Recipe, id=recipe_id)
    like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)

    if not created:
        like.delete()

    return redirect("recipe_detail", recipe_id=recipe.id)
