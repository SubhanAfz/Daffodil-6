from django.test import TestCase
from django.urls import reverse
from recipes.models.recipe import Recipe
from recipes.models.user import User
from recipes.tests.helpers import MODERATION_FIXTURES, CommonTestMixin


class PostHideViewTest(TestCase, CommonTestMixin):
    """Test the hide post view."""

    fixtures = MODERATION_FIXTURES

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.moderator = User.objects.get(pk=5)
        self.superuser = User.objects.get(pk=6)

        self.recipe = Recipe.objects.get(pk=2)

        self.url = reverse("post_hide", args=[self.recipe.pk])

    def test_non_staff_gets_403(self):
        """Non-staff users get a 403 error page when attempting to hide a recipe."""

        self.client.login(username="@janedoe", password="Password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "403_error.html")

    def test_get_gives_405(self):
        """Staff get a 405 error page when using a get request on the URL."""

        self.client.login(username="@superuser", password="Password123")
        self.assert_405_on_get(self.url)

    def test_hides_recipe(self):
        """A staff user hiding a recipe leads to the recipe being hidden"""

        self.client.login(username="@superuser", password="Password123")

        recipe = Recipe.objects.get(pk=self.recipe.pk)
        self.assertFalse(recipe.is_hidden)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        recipe.refresh_from_db()
        self.assertTrue(recipe.is_hidden)
