from django.shortcuts import render
from django.db.models import Q, Count
from recipes.models import Recipe, Tag


def search_view(request):
    """
    Search recipes based on keywords, tags, ingredients, and sort by various criteria.

    Query parameters:
    - q: General keyword search (searches title and description)
    - tags: Comma-separated tag names
    - ingredients: Search in ingredients field
    - sort: Sorting option (most_liked, most_viewed, newest, oldest)
    """

    MAX_KEYWORD_LENGTH = 100
    MAX_TAGS_LENGTH = 200
    MAX_INGREDIENTS_LENGTH = 100

    keyword = request.GET.get("q", "").strip()
    if len(keyword) > MAX_KEYWORD_LENGTH:
        keyword = keyword[:MAX_KEYWORD_LENGTH]
    tags_query = request.GET.get("tags", "").strip()
    if len(tags_query) > MAX_TAGS_LENGTH:
        tags_query = tags_query[:MAX_TAGS_LENGTH]
    ingredients_query = request.GET.get("ingredients", "").strip()
    if len(ingredients_query) > MAX_INGREDIENTS_LENGTH:
        ingredients_query = ingredients_query[:MAX_INGREDIENTS_LENGTH]
    sort_by = request.GET.get("sort", "newest")

    recipes = Recipe.objects.filter(is_hidden=False)

    if keyword:
        recipes = recipes.filter(
            Q(title__icontains=keyword)
            | Q(description__icontains=keyword)
            | Q(content__icontains=keyword)
        )

    # Apply tags filter
    if tags_query:
        tag_names = [
            tag.strip().lower() for tag in tags_query.split(",") if tag.strip()
        ]
        if tag_names:
            recipes = recipes.filter(tags__name__in=tag_names).distinct()

    if ingredients_query:
        recipes = recipes.filter(ingredients__icontains=ingredients_query)

    recipes = recipes.annotate(
        likes_count=Count("liked_by", distinct=True),
        favourites_count=Count("favourited_by", distinct=True),
    )

    # Apply sorting, with newest as default
    if sort_by == "most_liked":
        recipes = recipes.order_by("-likes_count", "-created_at")
    elif sort_by == "most_viewed":
        recipes = recipes.order_by("-views", "-created_at")
    elif sort_by == "oldest":
        recipes = recipes.order_by("created_at")
    else:
        recipes = recipes.order_by("-created_at")

    all_tags = Tag.objects.all().order_by("name")

    context = {
        "recipes": recipes,
        "all_tags": all_tags,
        "search_params": {
            "keyword": keyword,
            "tags": tags_query,
            "ingredients": ingredients_query,
            "sort_by": sort_by,
        },
        "result_count": recipes.count(),
    }

    return render(request, "search.html", context)
