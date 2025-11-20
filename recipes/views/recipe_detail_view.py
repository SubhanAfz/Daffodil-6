from django.shortcuts import render, get_object_or_404
from django.db.models import F
from recipes.models import Recipe

def recipe_detail(request, recipe_id):
    """
    Display the details of a specific recipe.

    This view retrieves a recipe by its ID and renders the recipe detail page.
    If the recipe does not exist, a 404 error is raised.
    """

    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Increment the view count each time the recipe detail is accessed
    recipe.views = F('views') +1
    recipe.save(update_fields=['views'])
    
    return render(request, 'recipe_detail.html', {'recipe': recipe})
    