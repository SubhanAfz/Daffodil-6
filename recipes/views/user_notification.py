from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
        "read_notifications": user_notifications.filter(is_read=True),
        "unread_notifications": user_notifications.filter(is_read=False),
    }

    return render(request, "notifications.html", context)



@login_required
def mark_notifications_as_read(request):
    """Mark all notifications as read for the logged-in user."""

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    user_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    user_notifications.update(is_read=True)

    return redirect("user_notifications")
