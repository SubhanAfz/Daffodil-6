from django.test import TestCase, override_settings
from django.urls import reverse
from recipes.models import Recipe
from django.contrib.auth import get_user_model
from recipes.tests.helpers import reverse_with_next
from unittest.mock import patch
from django.db import DatabaseError
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
import tempfile
import os


MEDIA_ROOT = tempfile.mkdtemp()

User = get_user_model()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class CreateRecipeViewTest(TestCase):
    """Tests for the create recipe in view."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    @classmethod
    def tearDownClass(cls):
        """Remove temporary media directory after all tests in this class."""
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

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

    def test_POST_redirects_on_success(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        recipe = Recipe.objects.latest("pk")
        self.assertRedirects(
            response, reverse("recipe_detail", kwargs={"recipe_id": recipe.pk})
        )

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

    def test_get_create_recipe_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )

    def test_post_create_recipe_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.post(self.url, data=self.form_data)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )

    @patch("recipes.models.Recipe.save")
    def test_database_error_handling(self, mock_save):
        """Test that DatabaseError is caught and appropriate error message is shown."""
        mock_save.side_effect = DatabaseError("Database connection failed")
        num_recipes_before = Recipe.objects.count()

        response = self.client.post(self.url, data=self.form_data)

        num_recipes_after = Recipe.objects.count()
        self.assertEqual(num_recipes_before, num_recipes_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_recipe.html")

        form = response.context["form"]
        self.assertIn(
            "An error occurred when posting your recipe. Please try again later.",
            form.non_field_errors(),
        )

    def test_create_recipe_with_thumbnail(self):
        """Test that a recipe with thumbnail is created successfully."""
        # Load the test image file
        fixtures_dir = os.path.join(os.path.dirname(__file__), "..", "fixtures")
        image_path = os.path.join(fixtures_dir, "burger.png")

        with open(image_path, "rb") as img_file:
            thumbnail = SimpleUploadedFile(
                name="burger.png",
                content=img_file.read(),
                content_type="image/png",
            )

            num_recipes_before = Recipe.objects.count()

            post_data = self.form_data.copy()
            post_data["thumbnail"] = thumbnail

            self.client.post(self.url, data=post_data)

            num_recipes_after = Recipe.objects.count()
            self.assertEqual(num_recipes_before + 1, num_recipes_after)

            recipe = Recipe.objects.latest("pk")
            self.assertIsNotNone(recipe.thumbnail)
            self.assertIn("thumbnails/", recipe.thumbnail.name)
            
    def test_create_recipe_with_tags(self):
        """Test that a recipe with tags is created successfully."""
        num_recipes_before = Recipe.objects.count()

        post_data = self.form_data.copy()
        post_data["tags_input"] = "Vegan, Gluten-Free, Dessert"

        self.client.post(self.url, data=post_data)

        num_recipes_after = Recipe.objects.count()
        self.assertEqual(num_recipes_before + 1, num_recipes_after)

        recipe = Recipe.objects.latest("pk")
        tags = [tag.name for tag in recipe.tags.all()]
        self.assertIn("Vegan", tags)
        self.assertIn("Gluten-Free", tags)
        self.assertIn("Dessert", tags)

    def test_create_recipe_without_thumbnail(self):
        """Test that a recipe without thumbnail has has_thumbnail set to False."""
        num_recipes_before = Recipe.objects.count()

        self.client.post(self.url, data=self.form_data)

        num_recipes_after = Recipe.objects.count()
        self.assertEqual(num_recipes_before + 1, num_recipes_after)

        recipe = Recipe.objects.latest("pk")
        self.assertFalse(recipe.thumbnail)
