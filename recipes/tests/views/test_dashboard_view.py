"""Tests of the dashboard view."""

from django.test import TestCase
from django.urls import reverse
from recipes.models import Follow, User
from recipes.tests.helpers import create_test_recipe


class DashboardViewTestCase(TestCase):
    """Tests of the dashboard view."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.url = reverse("dashboard")

    def test_user_dashboard_url(self):
        self.assertEqual(self.url, "/dashboard/")

    def test_get_dashboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_dashboard_showing_users_recipes(self):
        user = User.objects.get(username="@johndoe")
        create_test_recipe(
            title="Test Recipe",
            description="Test Description",
            content="Test Content",
            author=user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Recipe")

    def test_dashboard_not_showing_other_users_recipes(self):
        user2 = User.objects.create(username="@janedoe")

        create_test_recipe(
            title="User2 Recipe",
            description="Test Description",
            content="Test Content",
            author=user2,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "User2 Recipe")

    def test_dashboard_no_recipes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes found.")

    def test_dashboard_following_count(self):
        """Test that the dashboard displays the correct following count."""
        # Create additional users
        user2 = User.objects.create(username="@janedoe", email="jane@example.com")
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")
        user4 = User.objects.create(username="@sarahjones", email="sarah@example.com")

        # Make the current user follow user2 and user3
        Follow.objects.create(user=user2, follower=self.user)
        Follow.objects.create(user=user3, follower=self.user)

        # Make user4 follow the current user (should not affect following count)
        Follow.objects.create(user=self.user, follower=user4)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that the following count is 2
        self.assertEqual(response.context["following"], 2)

    def test_dashboard_followers_count(self):
        """Test that the dashboard displays the correct followers count."""
        # Create additional users
        user2 = User.objects.create(username="@janedoe", email="jane@example.com")
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")
        user4 = User.objects.create(username="@sarahjones", email="sarah@example.com")

        # Make user2 and user3 follow the current user
        Follow.objects.create(user=self.user, follower=user2)
        Follow.objects.create(user=self.user, follower=user3)

        # Make the current user follow user4 (should not affect followers count)
        Follow.objects.create(user=user4, follower=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that the followers count is 2
        self.assertEqual(response.context["followers"], 2)
