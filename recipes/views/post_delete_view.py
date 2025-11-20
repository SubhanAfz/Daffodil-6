from django.shortcuts import get_object_or_404, redirect, render
from recipes.models.recipe import Recipe


def post_delete(request, id):
    post = get_object_or_404(Recipe, id=id)

    if not request.user.is_staff:
        return render(request, '403_error.html')

    if request.method == "POST":
        post.set_hidden()
        post.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return render(request, '405_error.html')
    
