from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from recipes.models import Notification


@never_cache
@login_required
def get_user_notifications(request):
    """Get all user notifications for likes, favourites, and follows.

    Retrieves all notifications on the user's profile and displays them in the notifications page.
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
def mark_all_unread_notifications_as_read(request):
    """Mark all notifications as read for the logged-in user."""

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    user_notifications = Notification.objects.filter(
        recipient=request.user, is_read=False
    )
    user_notifications.update(is_read=True)

    return redirect("notifications")


@login_required
def notification_view(request, pk):
    """
    Mark the notification as read (if it belongs to the current user)
    and redirect to the notification link (or ?next=...), falling back to the
    notifications page.
    """
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if not notif.is_read:
        notif.is_read = True
        notif.save(update_fields=["is_read"])

    # prefer explicit next query param, then notification.link
    next_url = request.GET.get("next") or (notif.link or "")
    # allow internal links or same-host absolute URLs
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}
    ):
        return redirect(next_url)

    return redirect(reverse("notifications"))
