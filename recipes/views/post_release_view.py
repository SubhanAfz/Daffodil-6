from django.shortcuts import get_object_or_404, redirect, render
from recipes.models.recipe import Recipe
from recipes.models.report import Report


def post_release(request, id):
    post = get_object_or_404(Recipe, id=id)

    if request.method == "POST":

        post.set_public()
        post.save()
        Report.objects.filter(recipe=post).delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return render(request, '405_error.html')
    
