from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from recipes.models import Notification

@login_required
def get_user_notifications(request):
    """Get user notifications for likes on their recipes.

    Retrieves all likes on the user's recipes and displays them in the notifications page.
    """

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    user_notifications = Notification.objects.filter(recipient=request.user)

    context = {
        "notifications": user_notifications,
    }

    return render(request, "notifications.html", context)

@login_required
def mark_notifications_as_read(request):
    """Mark all notifications as read for the logged-in user."""

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    user_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    user_notifications.update(is_read=True)

    return render(request, "notifications.html", user_notifications)