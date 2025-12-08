from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Report
from recipes.tests.helpers import STANDARD_FIXTURES, CommonTestMixin


class ReportRecipeViewTest(TestCase, CommonTestMixin):
    fixtures = STANDARD_FIXTURES

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.recipe = Recipe.objects.get(pk=1)
        self.url = reverse("report_recipe", args=[self.recipe.pk])

    def test_unauthenticated_access(self):
        self.assert_unauthenticated_redirect(self.url)

    def test_report_recipe_renders_405_error(self):
        self.assert_405_on_get(self.url)

    def test_create_report(self):
        report_exists = Report.objects.filter(
            reporter=self.user, recipe=self.recipe
        ).exists()
        self.assertFalse(report_exists)
        response = self.client.post(self.url, {"reason": "Inappropriate content"})
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
        response = self.client.post(self.url, {"reason": ""})
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
        response = self.client.post(self.url, {"reason": new_reason})
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        report = Report.objects.get(reporter=self.user, recipe=self.recipe)
        self.assertEqual(report.reason, new_reason)
