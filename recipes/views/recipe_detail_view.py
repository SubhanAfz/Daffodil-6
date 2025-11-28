from django.shortcuts import render, get_object_or_404
from django.db.models import F, Count, Exists, OuterRef
from recipes.models import Recipe, Like, Favourite


def recipe_detail_view(request, recipe_id):
    """
    Display the details of a specific recipe.

    This view retrieves a recipe by its ID and renders the recipe detail page.
    If the recipe does not exist, a 404 error is raised.
    """

    queryset = Recipe.objects.annotate(
        likes_count=Count("liked_by", distinct=True),
        favourites_count=Count("favourited_by", distinct=True),
    )

    if request.user.is_authenticated:
        queryset = queryset.annotate(
            is_liked=Exists(
                Like.objects.filter(recipe=OuterRef("pk"), user=request.user)
            ),
            is_favourited=Exists(
                Favourite.objects.filter(recipe=OuterRef("pk"), user=request.user)
            ),
        )

    recipe = get_object_or_404(queryset, id=recipe_id)

    # Increment the view count each time the recipe detail is accessed
    recipe.views = F("views") + 1
    recipe.save(update_fields=["views"])
    recipe.refresh_from_db()

    is_liked = getattr(recipe, "is_liked", False)
    is_favourited = getattr(recipe, "is_favourited", False)
    likes = recipe.likes_count
    favourites = recipe.favourites_count
    return render(
        request,
        "recipe_detail.html",
        {
            "recipe": recipe,
            "is_liked": is_liked,
            "is_favourited": is_favourited,
            "likes": likes,
            "favourites": favourites,
        },
    )
