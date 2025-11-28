from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from recipes.views.error_views import error_405_view

class HTTP405MethodNotAllowedMiddleware:
    """
    Middleware to handle HTTP 405 Method Not Allowed errors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseNotAllowed):
            return error_405_view(request)
        return response
