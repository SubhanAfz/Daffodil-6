from django.shortcuts import render


def error_405_view(request, exception=None):
    """
    Custom 405 Method Not Allowed error handler.
    """
    return render(request, "405_error.html", status=405)
