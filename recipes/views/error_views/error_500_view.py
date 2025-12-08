from django.shortcuts import render


def error_500_view(request):
    """
    Custom 500 Internal Server Error handler.

    This view renders a user-friendly 500 error page.
    This happens when an unhandled exception occurs in the server.
    """
    return render(request, "500_error.html", status=500)
