from django.shortcuts import render
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from recipes.models.recipe import Recipe


@login_required
def get_moderation_queue(request: HttpRequest):
    """Get post and report information for mod queue page.

    Gets the order tag of the page.
    If there isn't an order tag then it takes the default of 'asc'.
    It then makes the appropriate list based on the order and puts it in the context.
    """

    if not request.user.is_staff:
        raise PermissionDenied

    order = request.GET.get("order", "asc")

    num_unresolved_posts = 0
    if order == "desc":
        list = (
            Recipe.objects.all()
            .filter(is_hidden=True, is_reported=True)
            .order_by("-date_hidden")
        )
        num_unresolved_posts = list.count()
    elif order == "reports":
        list = (
            Recipe.objects.all()
            .filter(is_hidden=True, is_reported=True)
            .order_by("-num_reports")
        )
        num_unresolved_posts = list.count()
    else:
        list = (
            Recipe.objects.all()
            .filter(is_hidden=True, is_reported=True)
            .order_by("date_hidden")
        )
        num_unresolved_posts = list.count()

    context = {
        "num_posts": num_unresolved_posts,
        "list": list,
        "order": order,
    }

    return render(request, "hidden_dashboard.html", context)
