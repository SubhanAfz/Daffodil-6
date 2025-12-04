from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from recipes.models import Recipe


@login_required
def feed(request):
    """
    Display a feed of recipes from other users.

    This view renders a feed page showing random recipes from other users.
    It ensures that only logged-in users can access the page.
    """
    current_user = request.user

    # Get random recipes not authored by the current user and not hidden
    recipes = (
        Recipe.objects.exclude(author=current_user)
        .filter(is_hidden=False)
        .order_by("?")[:50]
    )

    return render(
        request,
        "feed.html",
        {
            "recipes": recipes,
        },
    )
