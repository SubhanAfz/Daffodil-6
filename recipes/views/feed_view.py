from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from recipes.models import Recipe, User


@login_required
def feed(request):
    """
    This view renders a feed page showing:
    - Popular chefs (users with most followers)
    - Trending recipes (recipes with most likes)
    - Explore (recipes tailored to the user's following and likes)
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    current_user = request.user

    popular_chefs = User.objects.annotate(num_followers=Count("followers")).order_by(
        "-num_followers"
    )[:10]

    trending_recipes = (
        Recipe.objects.filter(is_hidden=False)
        .annotate(num_likes=Count("liked_by"))
        .order_by("-num_likes")[:10]
    )
    followed_users = User.objects.filter(followers__follower=current_user)
    liked_authors = User.objects.filter(recipe__liked_by__user=current_user)

    explore_recipes = (
        Recipe.objects.filter(
            Q(author__in=followed_users) | Q(author__in=liked_authors)
        )
        .exclude(author=current_user)
        .filter(is_hidden=False)
        .distinct()
        .order_by("-created_at")[:50]
    )

    # fallback: just show random recipes if the user doesn't follow anyone and hasn't liked anything
    if not explore_recipes:
        explore_recipes = (
            Recipe.objects.exclude(author=current_user)
            .filter(is_hidden=False)
            .order_by("?")[:50]
        )

    return render(
        request,
        "feed.html",
        {
            "popular_chefs": popular_chefs,
            "trending_recipes": trending_recipes,
            "explore_recipes": explore_recipes,
            "recipes": explore_recipes,
        },
    )
