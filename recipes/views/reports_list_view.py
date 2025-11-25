from django.shortcuts import render
from recipes.models.recipe import Recipe
from recipes.models.report import Report


def get_reports_list(request):

    """Get post and report information for Reports page.
    
    Gets the order tag of the page, if there isn't one then it takes the default of 'asc'.
     It then makes the appropriate list based on the order and puts it in the context.  """
    
    order = request.GET.get('order', 'asc')

    num_unresolved_reports = 0
    if order == "desc":
        list = Report.objects.all().exclude(recipe__is_hidden=True).order_by('report_time')
        num_unresolved_reports = list.count()
    elif order == "posts":
        list = Recipe.objects.all().filter(is_hidden=False, is_reported=True).order_by('-num_reports')
        num_unresolved_reports = Report.objects.all().exclude(recipe__is_hidden=True).count()
    else:
        list = Report.objects.all().exclude(recipe__is_hidden=True).order_by('-report_time')
        num_unresolved_reports = list.count()
    


    context = {
        'num_reports' : num_unresolved_reports,
        'list' : list,
        'order' : order,
    }

    return render(request, 'reported_dashboard.html', context)