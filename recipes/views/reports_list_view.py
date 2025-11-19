from recipes.models.recipe import Recipe
from recipes.models.report import Report


def get_reports_list(request):
    reports_asc = Report.objects.all().order_by('created_at')
    reports_desc = Report.objects.all().order_by('-created_at')
    reported_recipes = Recipe.objects.all().order_by('num_reports')

    context = {
        'num_reports' : Report.objects.count(),
        'ascending_order_reports' : reports_asc,
        'descending_order_reports' : reports_desc,
        'num_reports_recipes' : reported_recipes,
    }