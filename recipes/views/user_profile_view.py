from django.shortcuts import render, get_object_or_404
from recipes.models.user import User
from recipes.models.recipe import Recipe


def user_profile(request, username):
    """
    Show all recipes for a given username.
    Accepts username with or without a leading '@'.
    """
    profile_user = User.objects.filter(username=username).first()
    if not profile_user:
        alt = f"@{username}"
        profile_user = get_object_or_404(User, username=alt)
    recipes = Recipe.objects.filter(author=profile_user).order_by('-created_at')
    return render(request, "user_profile.html", {
        "profile_user": profile_user,
        "recipes": recipes,
    })