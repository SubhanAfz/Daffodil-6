from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from recipes.models import Recipe


@login_required
def favourite_list(request):
    """
    Display the list of recipes favourited by the current user.
    """
    current_user = request.user
    recipes = Recipe.objects.filter(favourited_by__user=current_user)
    return render(request, "favourites.html", {"recipes": recipes})
