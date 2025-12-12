from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from recipes.models import Notification, User


class NotificationModelTestCase(TestCase):
    """Unit tests for the Notification model."""

    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        """Set up test data for notification tests."""
        self.recipient = User.objects.get(username="@johndoe")
        self.sender = User.objects.get(username="@janedoe")

    def test_valid_notification_creation(self):
        """Test that a notification can be created successfully."""
        notif = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type="follow",
            link=f"/users/{self.sender.username}/",
        )
        self.assertIsInstance(notif, Notification)
        self.assertEqual(notif.recipient, self.recipient)
        self.assertEqual(notif.sender, self.sender)
        self.assertEqual(notif.notification_type, "follow")
        self.assertEqual(notif.link, f"/users/{self.sender.username}/")

    def test_is_read_defaults_to_false(self):
        """Test that the 'is_read' field defaults to False."""
        notif = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type="like",
        )
        self.assertFalse(notif.is_read)

    def test_created_at_is_auto_set(self):
        """Test that the 'created_at' field is set automatically."""
        notif = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type="favourite",
        )
        self.assertIsNotNone(notif.created_at)
        self.assertLess(notif.created_at, timezone.now())

    def test_link_can_be_null(self):
        """Test that the 'link' field can be null."""
        notif = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type="default",
            link=None,
        )
        self.assertIsNone(notif.link)

    def test_unique_notification_constraint(self):
        """Test the unique constraint on recipient, sender, type, and link."""
        Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type="like",
            link="/recipe/1/",
        )
        with self.assertRaises(IntegrityError):
            Notification.objects.create(
                recipient=self.recipient,
                sender=self.sender,
                notification_type="like",
                link="/recipe/1/",
            )

    def test_ordering_is_by_created_at_descending(self):
        """Test that notifications are ordered by 'created_at' in descending order."""
        notif1 = Notification.objects.create(
            recipient=self.recipient, sender=self.sender, notification_type="like"
        )
        notif2 = Notification.objects.create(
            recipient=self.recipient, sender=self.sender, notification_type="follow"
        )
        notifications = Notification.objects.filter(recipient=self.recipient)
        self.assertEqual(list(notifications), [notif2, notif1])

    def test_cascade_delete_on_recipient(self):
        """Test that deleting a recipient user deletes their notifications."""
        notif = Notification.objects.create(
            recipient=self.recipient, sender=self.sender, notification_type="like"
        )
        notif_id = notif.id
        self.recipient.delete()
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notif_id)

    def test_cascade_delete_on_sender(self):
        """Test that deleting a sender user deletes their sent notifications."""
        notif = Notification.objects.create(
            recipient=self.recipient, sender=self.sender, notification_type="like"
        )
        notif_id = notif.id
        self.sender.delete()
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notif_id)

    def test_str_representation(self):
        """Test the string representation of the notification."""
        notif = Notification.objects.create(
            recipient=self.recipient, sender=self.sender, notification_type="follow"
        )
        expected_str = f"Notification for {self.recipient.username} from {self.sender.username} (follow)"
        self.assertEqual(str(notif), expected_str)
