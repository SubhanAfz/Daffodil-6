from django.shortcuts import render

def error_403_view(request, exception=None):
    """
    Custom 403 Forbidden error handler.

    This view renders a user-friendly 403 error page when a user tries to
    access a resource they are not authorized to view.
    """
    return render(request, "403_error.html", status=403)