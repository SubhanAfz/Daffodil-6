from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from recipes.models import Recipe, Like


@login_required
def toggle_like(request, recipe_id):
    """
    Toggle the like status for a specific recipe by the current user.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)

    if not created:
        # If the like already existed, delete it (unlike)
        like.delete()

    return redirect("recipe_detail", recipe_id=recipe.id)

