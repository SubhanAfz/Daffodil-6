from django.shortcuts import render
from recipes.models.recipe import Recipe
from recipes.models.report import Report


def get_reports_list(request):
    order = request.GET.get('order')

    if order == "desc":
        list = Report.objects.all().order_by('report_time')
    elif order == "posts":
        list = Recipe.objects.all().order_by('-num_reports')
    else:
        list = list = Report.objects.all().order_by('-report_time')
    

    context = {
        'num_reports' : Report.objects.count(),
        'list' : list,
    }

    return render(request, 'reported_dashboard.html', context)