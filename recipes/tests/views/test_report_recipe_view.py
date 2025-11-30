from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Report


class ReportRecipeViewTest(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.recipe = Recipe.objects.get(pk=1)
        self.url = reverse("report_recipe", args=[self.recipe.pk])

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_report_recipe_renders_405_error(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")

    def test_create_report(self):
        report_exists = Report.objects.filter(
            reporter=self.user, recipe=self.recipe
        ).exists()
        self.assertFalse(report_exists)
        response = self.client.post(self.url, {"report_text": "Inappropriate content"})
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        report_exists = Report.objects.filter(
            reporter=self.user, recipe=self.recipe
        ).exists()
        self.assertTrue(report_exists)

    def test_report_recipe_with_empty_reason(self):
        report_exists = Report.objects.filter(
            reporter=self.user, recipe=self.recipe
        ).exists()
        self.assertFalse(report_exists)
        response = self.client.post(self.url, {"report_text": ""})
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        report = Report.objects.get(reporter=self.user, recipe=self.recipe)
        self.assertEqual(report.reason, "No reason provided.")

    def test_report_recipe_overwrites_reason_when_already_reported(self):
        Report.objects.create(
            reporter=self.user, recipe=self.recipe, reason="Original reason"
        )
        report_exists = Report.objects.filter(
            reporter=self.user, recipe=self.recipe
        ).exists()
        self.assertTrue(report_exists)
        new_reason = "Updated reason for reporting"
        response = self.client.post(self.url, {"report_text": new_reason})
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        report = Report.objects.get(reporter=self.user, recipe=self.recipe)
        self.assertEqual(report.reason, new_reason)
