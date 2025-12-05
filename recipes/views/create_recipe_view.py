from django.shortcuts import render, redirect
from django.db import DatabaseError, IntegrityError, transaction
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


@login_required
def create_recipe(request: HttpRequest):
    """Create a recipe.

    Checks to make sure a post request is being made (if not, then a default form is made).
    If the form is valid, it will set the user as the author of the form and attempt to save it.
    If saving fails, the user is given an error.


    """
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe: Recipe = form.save(commit=False)
            recipe.author = request.user
            try:
                with transaction.atomic():
                    recipe.save()
                    tags_input = form.cleaned_data.get("tags_input", "")
                    if tags_input:
                        tag_names = [
                            name.strip() for name in tags_input.split(",") if name.strip()
                        ]
                        for tag_name in tag_names:
                            lower_tag_name = tag_name.lower()
                            tag, _ = Tag.objects.get_or_create(name=lower_tag_name)
                            tag.recipes.add(recipe)
                return redirect("recipe_detail", recipe_id=recipe.pk)
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
    else:
        form = RecipeForm()

    return render(request, "create_recipe.html", {"form": form})
