"""Tests of the home view."""

from django.test import TestCase, override_settings
from django.urls import reverse
from recipes.models.recipe import Recipe
from recipes.models.user import User


class UserProfileViewTestCase(TestCase):
    """Tests of the user profile view."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("user_profile", kwargs={"username": "@johndoe"})

    def test_user_profile_url(self):
        self.assertEqual(self.url, "/users/@johndoe/")

    def test_get_user_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile.html")

    def test_get_user_profile_redirects_when_using_username_without_at_symbol(self):
        url = reverse("user_profile", kwargs={"username": "johndoe"})
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, self.url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, "user_profile.html")

    def test_get_user_profile_not_found(self):
        url = reverse("user_profile", kwargs={"username": "@nonexistentuser"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=False)
    def test_user_profile_not_found_template(self):
        url = reverse("user_profile", kwargs={"username": "@nonexistentuser"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404_error.html")

    def test_user_profile_showing_users_recipes(self):
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

    def test_user_profile_not_showing_other_users_recipes(self):
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
