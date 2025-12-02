from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from recipes.models import Recipe


@login_required
def favourite_list(request):
    """
    Display the list of recipes favourited by the current user.
    """

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    current_user = request.user
    recipes = Recipe.objects.filter(favourited_by__user=current_user)
    return render(request, "favourites.html", {"recipes": recipes})
