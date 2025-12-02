from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseNotAllowed

from recipes.models import Recipe


# login_required: https://docs.djangoproject.com/en/5.2/topics/auth/default/#the-login-required-decorator
@login_required
def like_list(request):
    """
    Display the list of recipes liked by the current user.
    """

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    current_user = request.user
    recipes = Recipe.objects.filter(liked_by__user=current_user)
    return render(request, "likes.html", {"recipes": recipes})
