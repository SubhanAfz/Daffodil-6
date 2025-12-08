from django.shortcuts import render, redirect
from django.db import DatabaseError, IntegrityError, transaction
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


@login_required
def create_recipe(request: HttpRequest):
    """
    Create a new recipe.
    Checks to make sure a post request is being made.
        (if not, then a default form is made)
    If the form is valid:
        It will set the user as the author of the form and attempt to save it.
    If saving fails, the user is given an error.
    """
    if request.method != "POST":
        form = RecipeForm()
        return render(request, "create_recipe.html", {"form": form})

    form = RecipeForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, "create_recipe.html", {"form": form})

    recipe: Recipe = form.save(commit=False)
    recipe.author = request.user
    try:
        return _save_recipe_with_tags(recipe, form)
    except IntegrityError:
        form.add_error(
            None,
            "A database integrity error occurred. Please ensure all fields are valid.",
        )
    except DatabaseError:
        form.add_error(
            None,
            "An error occurred when posting your recipe. Please try again later.",
        )
    return render(request, "create_recipe.html", {"form": form})


def _save_recipe_with_tags(recipe: Recipe, form: RecipeForm):
    """
    Helper function to save a recipe and associate tags with it.
    Uses a transaction to ensure both operations succeed or fail together.
    """
    with transaction.atomic():
        recipe.save()
        tags_input = form.cleaned_data.get("tags_input", "")
        _add_tags_to_recipe(recipe, tags_input)
    return redirect("recipe_detail", recipe_id=recipe.pk)


def _add_tags_to_recipe(recipe: Recipe, tags_input: str):
    """
    Helper function to add tags to a recipe.
    Splits the input string and adds each tag to the recipe.
    Creates new Tag objects if they do not already exist.
    """
    if not tags_input:
        return
    tag_names = [name.strip() for name in tags_input.split(",") if name.strip()]
    for tag_name in tag_names:
        lower_tag_name = tag_name.lower()
        tag, _ = Tag.objects.get_or_create(name=lower_tag_name)
        tag.recipes.add(recipe)
