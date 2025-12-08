from django.shortcuts import render
from django.db.models import Q, Count
from recipes.models import Recipe, Tag

MAX_KEYWORD_LENGTH = 100
MAX_TAGS_LENGTH = 200
MAX_INGREDIENTS_LENGTH = 100


def search_view(request):
    """
    Search recipes based on keywords, tags, ingredients, and sort by various criteria.

    Query parameters:
    - q: General keyword search (searches title and description)
    - tags: Comma-separated tag names
    - ingredients: Search in ingredients field
    - sort: Sorting option (most_liked, most_viewed, newest, oldest)
    """
    keyword = _process_url_variable(request, "q", MAX_KEYWORD_LENGTH)
    tags_query = _process_url_variable(request, "tags", MAX_TAGS_LENGTH)
    ingredients_query = _process_url_variable(
        request, "ingredients", MAX_INGREDIENTS_LENGTH
    )

    sort_by = request.GET.get("sort", "newest")

    recipes = Recipe.objects.filter(is_hidden=False)
    # Apply keyword filter
    recipes = _filter(recipes, keyword)
    # Apply tags filter
    tag_names = _process_tags(tags_query)
    if tag_names:
        recipes = recipes.filter(tags__name__in=tag_names).distinct()

    if ingredients_query:
        recipes = recipes.filter(ingredients__icontains=ingredients_query)

    recipes = recipes.annotate(
        likes_count=Count("liked_by", distinct=True),
        favourites_count=Count("favourited_by", distinct=True),
    )

    # Apply sorting, with newest as default
    recipes = _apply_sorting(recipes, sort_by)

    return render(
        request,
        "search.html",
        {
            "recipes": recipes,
            "all_tags": Tag.objects.all().order_by("name"),
            "search_params": {
                "keyword": keyword,
                "tags": tags_query,
                "ingredients": ingredients_query,
                "sort_by": sort_by,
            },
            "result_count": recipes.count(),
        },
    )


def _filter(recipes, keyword):
    """
    Function which applies keyword filtering to the recipes queryset.
    """
    if keyword:
        return recipes.filter(
            Q(title__icontains=keyword)
            | Q(description__icontains=keyword)
            | Q(content__icontains=keyword)
        )
    return recipes


def _apply_sorting(recipes, sort_by):
    """
    Function which sorts the recipes queryset based on the sort_by parameter.
    """
    if sort_by == "most_liked":
        return recipes.order_by("-likes_count", "-created_at")
    elif sort_by == "most_viewed":
        return recipes.order_by("-views", "-created_at")
    elif sort_by == "oldest":
        return recipes.order_by("created_at")
    else:
        return recipes.order_by("-created_at")


def _process_tags(tags_query):
    """
    Function which processes a string of tags into a list of cleaned tag names.
    """
    if not tags_query:
        return []
    return [tag.strip().lower() for tag in tags_query.split(",") if tag.strip()]


def _process_url_variable(req, var_name, max_length):
    """
    Function which processes a URL variable by:
        - trimming whitespace
        - enforcing a maximum length
    """
    value = req.GET.get(var_name, "").strip()
    if len(value) > max_length:
        value = value[:max_length]
    return value
