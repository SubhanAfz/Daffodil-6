from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateRecipeViewTest(TestCase):
    """Tests for the create recipe in view."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.url = reverse("create_recipe")
        self.form_data = {"title": "Test", "description": "Test", "content": "Test"}
        self.invalid_form_data = {
            "title": "a" * 201,
            "description": "Test",
            "content": "Test",
        }

    def test_GET_gives_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_recipe.html")

    def test_POST_gives_200_OK(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_recipe.html")

    def test_create_recipe(self):
        num_recipes_before = Recipe.objects.count()
        self.client.post(self.url, data=self.form_data)
        num_recipes_after = Recipe.objects.count()

        self.assertEqual(num_recipes_before + 1, num_recipes_after)

    def test_invalid_data_doesnt_create_recipe(self):
        num_recipes_before = Recipe.objects.count()
        self.client.post(self.url, data=self.invalid_form_data)
        num_recipes_after = Recipe.objects.count()

        self.assertEqual(num_recipes_before, num_recipes_after)

    def test_redirect(self):
        response = self.client.post(self.url, data=self.form_data, follow=True)
        recipe = Recipe.objects.latest("pk")

        self.assertRedirects(
            response, reverse("recipe_detail", kwargs={"recipe_id": recipe.pk})
        )
