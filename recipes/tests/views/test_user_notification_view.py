from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import Notification
from recipes.models import User
from recipes.tests.helpers import reverse_with_next


class GetUserNotificationsTests(TestCase):
    """Tests for get_user_notifications view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="@testuser", email="testuser@example.com", password="Password123"
        )
        self.url = reverse("notifications")

    def test_redirect_when_not_logged_in(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        redirect_url = reverse_with_next("log_in", self.url)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )

    def test_get_method_returns_200(self):
        """Test GET request returns success."""
        self.client.login(username="@testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notifications.html")

    def test_post_method_not_allowed(self):
        """Test POST method returns 405."""
        self.client.login(username="@testuser", password="Password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_context_contains_read_and_unread_notifications(self):
        """Test context contains read and unread notifications."""
        self.client.login(username="@testuser", password="Password123")

        sender = User.objects.create_user(
            username="@sender", email="sender@example.com", password="Password123"
        )

        # Create read and unread notifications
        Notification.objects.create(
            recipient=self.user,
            sender=sender,
            notification_type="like",
            is_read=True,
        )
        Notification.objects.create(
            recipient=self.user,
            sender=sender,
            notification_type="follow",
            is_read=False,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["read_notifications"]), 1)
        self.assertEqual(len(response.context["unread_notifications"]), 1)

    def test_only_shows_user_own_notifications(self):
        """Test that users only see their own notifications."""
        other_user = User.objects.create_user(
            username="@otheruser", email="otheruser@example.com", password="Password123"
        )

        # Create notifications for both users
        Notification.objects.create(
            recipient=self.user,
            sender=other_user,
            notification_type="like",
        )
        Notification.objects.create(
            recipient=other_user, sender=self.user, notification_type="like"
        )

        self.client.login(username="@testuser", password="Password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        total_notifications = len(response.context["read_notifications"]) + len(
            response.context["unread_notifications"]
        )
        self.assertEqual(total_notifications, 1)

class MarkAllUnreadNotificationsAsReadTests(TestCase):
    """Tests for mark_all_unread_notifications_as_read view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="@testuser", email="testuser@example.com", password="Password123"
        )
        self.url = reverse("mark_notifications_as_read")

    def test_redirect_when_not_logged_in(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url)
        redirect_url = reverse_with_next("log_in", self.url)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )

    def test_get_method_not_allowed(self):
        """Test GET method returns 405."""
        self.client.login(username="@testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_marks_all_unread_as_read(self):
        """Test that all unread notifications are marked as read."""
        self.client.login(username="@testuser", password="Password123")

        sender = User.objects.create_user(
            username="@sender", email="sender@example.com", password="Password123"
        )

        # Create unread notifications
        notif1 = Notification.objects.create(
            recipient=self.user, sender=sender, notification_type="like", is_read=False
        )
        notif2 = Notification.objects.create(
            recipient=self.user,
            sender=sender,
            notification_type="follow",
            is_read=False,
        )

        response = self.client.post(self.url, follow=True)

        # Refresh from database
        notif1.refresh_from_db()
        notif2.refresh_from_db()

        self.assertTrue(notif1.is_read)
        self.assertTrue(notif2.is_read)
        self.assertRedirects(
            response, reverse("notifications"), status_code=302, target_status_code=200
        )

    def test_does_not_affect_already_read(self):
        """Test that already read notifications remain read."""
        self.client.login(username="@testuser", password="Password123")

        sender = User.objects.create_user(
            username="@sender", email="sender@example.com", password="Password123"
        )

        # Create read notification
        notif = Notification.objects.create(
            recipient=self.user, sender=sender, notification_type="like", is_read=True
        )

        self.client.post(self.url)
        notif.refresh_from_db()

        self.assertTrue(notif.is_read)

    def test_only_affects_user_notifications(self):
        """Test that only current user's notifications are marked as read."""
        other_user = User.objects.create_user(
            username="@otheruser", email="otheruser@example.com", password="Password123"
        )

        # Create notification for other user
        other_notif = Notification.objects.create(
            recipient=other_user,
            sender=self.user,
            notification_type="like",
            is_read=False,
        )

        self.client.login(username="@testuser", password="Password123")
        self.client.post(self.url)

        other_notif.refresh_from_db()
        self.assertFalse(other_notif.is_read)

    def test_redirects_to_notifications_page(self):
        """Test that view redirects to notifications page."""
        self.client.login(username="@testuser", password="Password123")
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse("notifications"))


class NotificationViewTests(TestCase):
    """Tests for notification_view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="@testuser", email="testuser@example.com", password="Password123"
        )
        self.sender = User.objects.create_user(
            username="@sender", email="sender@example.com", password="Password123"
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            sender=self.sender,
            notification_type="like",
            is_read=False,
            link="/some-page/",
        )

    def test_redirect_when_not_logged_in(self):
        """Test that unauthenticated users are redirected to login."""
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})
        response = self.client.get(url)
        redirect_url = reverse_with_next("log_in", url)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )

    def test_404_for_nonexistent_notification(self):
        """Test 404 is returned for non-existent notification."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_404_for_other_user_notification(self):
        """Test that users cannot access other users' notifications."""
        other_user = User.objects.create_user(
            username="@otheruser", email="otheruser@example.com", password="Password123"
        )
        other_notif = Notification.objects.create(
            recipient=other_user, sender=self.sender, notification_type="like"
        )

        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": other_notif.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_marks_notification_as_read(self):
        """Test that unread notification is marked as read."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        self.client.get(url)
        self.notification.refresh_from_db()

        self.assertTrue(self.notification.is_read)

    def test_redirects_correctly_for_already_read_notification(self):
        """Test that an already read notification still redirects correctly."""
        self.notification.is_read = True
        self.notification.save()

        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.notification.link)

    def test_redirects_to_notification_link(self):
        """Test redirect to notification link when present."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/some-page/")

    def test_redirects_to_next_param(self):
        """Test redirect to next query parameter when provided."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        response = self.client.get(url + "?next=/custom-page/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/custom-page/")

    def test_next_param_takes_precedence_over_link(self):
        """Test that next parameter takes precedence over notification link."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        response = self.client.get(url + "?next=/priority-page/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/priority-page/")

    def test_redirects_to_notifications_when_no_link(self):
        """Test redirect to notifications page when no link provided."""
        notif = Notification.objects.create(
            recipient=self.user, sender=self.sender, notification_type="like", link=""
        )

        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": notif.pk})

        response = self.client.get(url)
        self.assertRedirects(response, reverse("notifications"))

    def test_redirects_to_notifications_when_link_is_none(self):
        """Test redirect to notifications page when link is None."""
        notif = Notification.objects.create(
            recipient=self.user, sender=self.sender, notification_type="like", link=None
        )

        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": notif.pk})

        response = self.client.get(url)
        self.assertRedirects(response, reverse("notifications"))

    def test_rejects_external_next_url(self):
        """Test that external URLs in next parameter are rejected."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        response = self.client.get(url + "?next=https://evil.com/phishing")
        self.assertRedirects(response, reverse("notifications"))

    def test_allows_same_host_absolute_url(self):
        """Test that same-host absolute URLs are allowed."""
        self.client.login(username="@testuser", password="Password123")
        url = reverse("notification_view", kwargs={"pk": self.notification.pk})

        # Get the current host
        response = self.client.get(url + "?next=http://testserver/safe-page/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "http://testserver/safe-page/")

    def test_get_user_notifications_has_cache_control_headers(self):
        """Test that notifications list has cache control headers."""
        self.client.login(username="@testuser", password="Password123")
        response = self.client.get(reverse("notifications"))

        # Check for never_cache headers
        self.assertIn("no-cache", response.get("Cache-Control", "").lower())
