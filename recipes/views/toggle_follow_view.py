from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404
from recipes.models import User, Follow


@login_required
def toggle_follow(request, user_id):
    """Handle following a user."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        # cannot follow oneself
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))

    follow, created = Follow.objects.get_or_create(
        follower=request.user, user=user_to_follow
    )

    if not created:
        # If the follow relationship already existed, delete it (unfollow)
        follow.delete()

    # Redirect back to the previous page
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))
