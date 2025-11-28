from django.test import TestCase
from django.urls import reverse
from recipes.models import User


class ErrorView405Test(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/reports.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.url = reverse("post_delete", args=[1])  # Example URL that only allows POST
        self.user = User.objects.get(username="@superuser")
        self.client.force_login(self.user)

    def test_405_error_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")
