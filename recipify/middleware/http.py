from django.shortcuts import render
from django.http import HttpResponseNotAllowed


class HTTP405MethodNotAllowedMiddleware:
    """
    Middleware to handle HTTP 405 Method Not Allowed errors..
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseNotAllowed):
            return render(request, "405_error.html", status=405)
        return response
