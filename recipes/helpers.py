from recipes.models import Notification


def create_notification(recipient, sender, notification_type="default", link=""):
    """
    Create a notification
    notification_type: 'like', 'favourite', 'follow', or 'default'
    """

    Notification.objects.get_or_create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        link=link,
    )
