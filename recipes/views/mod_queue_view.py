from django.shortcuts import render
from recipes.models.recipe import Recipe
from recipes.models.report import Report

def get_moderation_queue(request):
    order = request.GET.get('order', 'asc')

    num_unresolved_posts = 0
    if order == "desc":
        list = Recipe.objects.all().filter(is_hidden=True).order_by('-date_hidden')
        num_unresolved_posts = len(list)
    elif order == "reports":
        list = Recipe.objects.all().filter(is_hidden=True).order_by('-num_reports')
        num_unresolved_posts = len(list)
    else:
        list = Recipe.objects.all().filter(is_hidden=True).order_by('-date_hidden')
        num_unresolved_posts = len(list)

    context = {
        'num_posts' : num_unresolved_posts,
        'list' : list,
        'order' : order,
    }

    return render(request, 'hidden_dashboard.html', context)