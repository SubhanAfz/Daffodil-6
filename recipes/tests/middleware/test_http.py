from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from recipes.models import Recipe

User = get_user_model()


class HTTP405MiddlewareTest(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.user.is_staff = True
        self.user.save()
        self.recipe = Recipe.objects.first()
        self.url = reverse("post_hide", args=[self.recipe.id])

    def test_middleware_intercepts_405_and_renders_custom_template(self):
        """Test that the middleware intercepts HttpResponseNotAllowed and renders custom 405 template."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")
        self.assertIn(b"405 Error", response.content)

    def test_middleware_allows_correct_method(self):
        self.client.force_login(self.user)
        # Make a POST request to a POST endpoint - should work normally
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful hide
