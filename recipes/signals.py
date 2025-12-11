from recipes.models import Like, Favourite, Follow
from recipes.helpers import create_notification
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Like)
def create_like_notification(instance, created, **kwargs):
    """Create a notification when a recipe is liked."""
    if created:
        create_notification(
            recipient=instance.recipe.author,
            sender=instance.user,
            notification_type="like",
            link=f"/recipe/{instance.recipe.id}/",
        )


@receiver(post_save, sender=Favourite)
def create_favourite_notification(instance, created, **kwargs):
    """Create a notification when a recipe is favourited."""
    if created:
        create_notification(
            recipient=instance.recipe.author,
            sender=instance.user,
            notification_type="favourite",
            link=f"/recipe/{instance.recipe.id}/",
        )


@receiver(post_save, sender=Follow)
def create_follow_notification(instance, created, **kwargs):
    """Create a notification when a user is followed."""
    if created:
        create_notification(
            recipient=instance.followed,
            sender=instance.follower,
            notification_type="follow",
            link=f"/users/{instance.follower.username}/",
        )
