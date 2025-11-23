from django.shortcuts import render
from recipes.models.recipe import Recipe
from recipes.models.report import Report

def get_moderation_queue(request):
    """Get post and report information for mod queue page.
    
    Gets the order tag of the page, if there isn't one then it takes the default of 'asc'.
     It then makes the appropriate list based on the order and puts it in the context.  """

    order = request.GET.get('order', 'asc')

    num_unresolved_posts = 0
    if order == "desc":
        list = Recipe.objects.all().filter(is_hidden=True, is_reported=True).order_by('-date_hidden')
        num_unresolved_posts = len(list)
    elif order == "reports":
        list = Recipe.objects.all().filter(is_hidden=True, is_reported=True).order_by('-num_reports')
        num_unresolved_posts = len(list)
    else:
        list = Recipe.objects.all().filter(is_hidden=True, is_reported=True).order_by('-date_hidden')
        num_unresolved_posts = len(list)

    context = {
        'num_posts' : num_unresolved_posts,
        'list' : list,
        'order' : order,
    }

    return render(request, 'hidden_dashboard.html', context)