from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import Favourite, Follow, Like, Recipe

User = get_user_model()


class SignalTests(TestCase):
    """Test suite for Django signals."""

    def setUp(self):
        """Set up common test data."""
        self.user1 = User.objects.create_user(
            username="user1", password="password123", email="user1@example.com"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="password123",
            email="user2@example.com",
        )
        self.recipe = Recipe.objects.create(
            author=self.user1, title="Test Recipe", content="Test instructions."
        )

    @patch("recipes.signals.create_notification")
    def test_create_like_notification_on_create(self, mock_create_notification):
        """Verify a notification is created when a recipe is liked."""
        Like.objects.create(user=self.user2, recipe=self.recipe)

        mock_create_notification.assert_called_once_with(
            recipient=self.user1,
            sender=self.user2,
            notification_type="like",
            link=f"/recipe/{self.recipe.id}/",
        )

    @patch("recipes.signals.create_notification")
    def test_no_like_notification_on_update(self, mock_create_notification):
        """Verify no notification is created when a Like instance is updated."""
        like = Like.objects.create(user=self.user2, recipe=self.recipe)
        mock_create_notification.reset_mock()  # Reset after initial creation

        like.save()  # Trigger a post_save signal on an existing object
        mock_create_notification.assert_not_called()

    @patch("recipes.signals.create_notification")
    def test_create_favourite_notification_on_create(
        self, mock_create_notification
    ):
        """Verify a notification is created when a recipe is favourited."""
        Favourite.objects.create(user=self.user2, recipe=self.recipe)

        mock_create_notification.assert_called_once_with(
            recipient=self.user1,
            sender=self.user2,
            notification_type="favourite",
            link=f"/recipe/{self.recipe.id}/",
        )

    @patch("recipes.signals.create_notification")
    def test_no_favourite_notification_on_update(self, mock_create_notification):
        """Verify no notification is created when a Favourite instance is updated."""
        favourite = Favourite.objects.create(user=self.user2, recipe=self.recipe)
        mock_create_notification.reset_mock()

        favourite.save()
        mock_create_notification.assert_not_called()

    @patch("recipes.signals.create_notification")
    def test_create_follow_notification_on_create(self, mock_create_notification):
        """Verify a notification is created when a user is followed."""
        Follow.objects.create(user=self.user1, follower=self.user2)

        mock_create_notification.assert_called_once_with(
            recipient=self.user1,
            sender=self.user2,
            notification_type="follow",
            link=f"/users/{self.user2.username}/",
        )

    @patch("recipes.signals.create_notification")
    def test_no_follow_notification_on_update(self, mock_create_notification):
        """Verify no notification is created when a Follow instance is updated."""
        follow = Follow.objects.create(user=self.user1, follower=self.user2)
        mock_create_notification.reset_mock()

        follow.save()
        mock_create_notification.assert_not_called()