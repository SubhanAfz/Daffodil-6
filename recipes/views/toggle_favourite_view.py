from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from recipes.models import Favourite, Recipe


@login_required
def toggle_favourite(request, recipe_id):
    """
    Toggle the favourite status for a specific recipe by the current user.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favourite, created = Favourite.objects.get_or_create(
        user=request.user, recipe=recipe
    )

    if not created:
        # If the favourite already existed, delete it (unfavourite)
        favourite.delete()

    return redirect("recipe_detail", recipe_id=recipe.id)
