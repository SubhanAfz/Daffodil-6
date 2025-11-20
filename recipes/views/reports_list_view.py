from django.shortcuts import render
from recipes.models.recipe import Recipe
from recipes.models.report import Report


def get_reports_list(request):
    order = request.GET.get('order', 'asc')

    num_unresolved_reports = 0
    if order == "desc":
        list = Report.objects.all().exclude(recipe__is_hidden=True).order_by('report_time')
        num_unresolved_reports = len(list)
    elif order == "posts":
        list = Recipe.objects.all().filter(is_hidden=False, is_reported=True).order_by('-num_reports')
        num_unresolved_reports = len(Report.objects.all().exclude(recipe__is_hidden=True))
    else:
        list = Report.objects.all().exclude(recipe__is_hidden=True).order_by('-report_time')
        num_unresolved_reports = len(list)
    


    context = {
        'num_reports' : num_unresolved_reports,
        'list' : list,
        'order' : order,
    }

    return render(request, 'reported_dashboard.html', context)