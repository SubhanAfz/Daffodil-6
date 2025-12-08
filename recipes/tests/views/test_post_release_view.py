from django.test import TestCase
from django.urls import reverse
from recipes.models.recipe import Recipe
from recipes.models.user import User
from recipes.tests.helpers import MODERATION_FIXTURES, CommonTestMixin


class PostReleaseViewTest(TestCase, CommonTestMixin):
    """Test the release post view."""

    fixtures = MODERATION_FIXTURES

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.moderator = User.objects.get(pk=5)
        self.superuser = User.objects.get(pk=6)

        self.recipe = Recipe.objects.get(pk=2)

        self.url = reverse("post_release", args=[self.recipe.pk])

    def test_non_super_gets_403(self):
        """Non-superusers get a 403 error page when attempting to release a recipe."""

        self.client.login(username="@janedoe", password="Password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "403_error.html")

    def test_get_gives_405(self):
        """Superusers get a 405 error page when using a get request on the URL."""

        self.client.login(username="@superuser", password="Password123")
        self.assert_405_on_get(self.url)

    def test_releases_recipe(self):
        """A superuser releasing a recipe leads to the recipe being not hidden"""

        self.client.login(username="@superuser", password="Password123")
        recipe = Recipe.objects.get(pk=self.recipe.pk)
        recipe.set_hidden()
        self.assertTrue(recipe.is_hidden)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        recipe.refresh_from_db()

        self.assertFalse(recipe.is_hidden)
