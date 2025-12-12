from recipes.models import Notification
from recipify.settings import DEBUG


def create_notification(recipient, sender, notification_type="default", link=""):
    """
    Create a notification
    notification_type: 'like', 'favourite', 'follow', or 'default'
    """
    is_notification_created = Notification.objects.get_or_create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        link=link,
    )

    if is_notification_created:
        print(f"Notification created: {notification_type} from {sender} to {recipient}")
