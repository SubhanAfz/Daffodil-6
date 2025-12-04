from django.shortcuts import render, redirect
from django.urls import reverse
from recipes.models.user import User
from recipes.models.recipe import Recipe
from django.http import Http404


def user_profile(request, username: str):
    """
    Show all recipes for a given username.
    Accepts username with or without a leading '@'.
    """
    profile_user = User.objects.filter(username=username).first()
    if not profile_user:
        if username.startswith("@"):
            raise Http404("User does not exist")
        else:
            alt = f"@{username}"
            # redirect usernames without '@' to the correct profile
            return redirect(reverse("user_profile", args=[alt]))
    recipes = Recipe.objects.filter(author=profile_user).order_by("-created_at")
    return render(
        request,
        "user_profile.html",
        {
            "profile_user": profile_user,
            "recipes": recipes,
        },
    )
