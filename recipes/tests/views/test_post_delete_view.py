from django.test import TestCase
from django.urls import reverse
from recipes.models.recipe import Recipe
from recipes.models.report import Report
from recipes.models.user import User


class PostDeleteViewTest(TestCase):
    """Test the delete post view."""

    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/reports.json",
        "recipes/tests/fixtures/staff_user.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.moderator = User.objects.get(pk=5)
        self.superuser = User.objects.get(pk=6)

        self.recipe = Recipe.objects.get(pk=2)

        self.url = reverse("post_delete", args=[self.recipe.pk])

    def test_non_super_gets_403(self):
        """Non-superusers get a 403 error page when attempting to delete a recipe."""

        self.client.login(username="@johndoe", password="Password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "403_error.html")

    def test_get_gives_405(self):
        """Superusers get a 405 error page when using a get request on the URL."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "405_error.html")

    def test_deletes_recipe_and_reports(self):
        """A superuser deleting a recipe leads to the recipe and associated reports being deleted."""

        self.client.login(username="@superuser", password="Password123")

        recipe_exists = Recipe.objects.filter(pk=self.recipe.pk).exists()
        reports_exist = Report.objects.filter(recipe=self.recipe).exists()
        self.assertTrue(recipe_exists)
        self.assertTrue(reports_exist)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        recipe_exists = Recipe.objects.filter(pk=self.recipe.pk).exists()
        reports_exist = Report.objects.filter(recipe=self.recipe).exists()
        self.assertFalse(recipe_exists)
        self.assertFalse(reports_exist)
