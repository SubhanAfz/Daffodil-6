"""Tests of the dashboard view."""

from django.test import TestCase
from django.urls import reverse
from recipes.models.recipe import Recipe
from recipes.models.user import User


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
        Recipe.objects.create(
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

        Recipe.objects.create(
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
