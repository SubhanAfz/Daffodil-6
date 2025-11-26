from django.shortcuts import render


def error_404_view(request, exception=None):
    """
    Custom 404 Not Found error handler.

    This view renders a user-friendly 404 error page when a user tries to
    access a resource that could not be found.
    """
    return render(request, "404_error.html", status=404)
