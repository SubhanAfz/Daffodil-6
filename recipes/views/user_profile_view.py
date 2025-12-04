from django.shortcuts import render, redirect
from django.urls import reverse
from recipes.models import User, Recipe, Follow
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

    # Filter recipes by author
    recipes = Recipe.objects.filter(author=profile_user).select_related("author")

    # Hide hidden recipes if viewing someone else's profile
    if request.user != profile_user:
        recipes = recipes.filter(is_hidden=False)

    recipes = recipes.order_by("-created_at")

    is_followed = False
    if request.user.is_authenticated:
        is_followed = Follow.objects.filter(
            follower=request.user, user=profile_user
        ).exists()

    # Get follower and following counts
    followers = profile_user.followers.count()
    following = profile_user.followers_of.count()

    return render(
        request,
        "user_profile.html",
        {
            "profile_user": profile_user,
            "recipes": recipes,
            "is_followed": is_followed,
            "followers": followers,
            "following": following,
        },
    )
