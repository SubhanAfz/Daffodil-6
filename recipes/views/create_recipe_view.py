from django.shortcuts import render, redirect
from django.db import DatabaseError
from recipes.forms import RecipeForm
from recipes.models import Recipe
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
                recipe.save()
                return redirect("recipe_detail", recipe_id=recipe.pk)
            except DatabaseError:
                form.add_error(
                    None,
                    "An error occurred when posting your recipe. Please try again later.",
                )
    else:
        form = RecipeForm()

    return render(request, "create_recipe.html", {"form": form})
