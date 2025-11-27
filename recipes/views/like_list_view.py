from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from recipes.models import Recipe


@login_required
def like_list(request):
    """
    Display the list of recipes liked by the current user.
    """
    current_user = request.user
    recipes = Recipe.objects.filter(liked_by__user=current_user)
    return render(request, "likes.html", {"recipes": recipes})

