from django.shortcuts import get_object_or_404, redirect, render
from recipes.models.recipe import Recipe
from recipes.models.report import Report


def post_delete(request, id):
    """ Deletes a post from the database.
    
    Takes the post id identifies if the user making the request has permission to delete posts/recipes. 
    Error 403 is given if the user does not have permission."""
    post = get_object_or_404(Recipe, id=id)

    if not request.user.is_superuser:
        return render(request, '403_error.html')

    if request.method == "POST":
        Report.objects.filter(recipe=post).delete()
        post.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return render(request, '405_error.html')
    
