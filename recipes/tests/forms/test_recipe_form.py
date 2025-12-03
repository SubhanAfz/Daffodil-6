from django.test import TestCase
from recipes.forms import RecipeForm
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()


class RecipeFormTest(TestCase):
    """Tests for the recipe form."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    def setUp(self):
        user = User.objects.get(username="@johndoe")

        self.form_input = {
            "title": "Test title",
            "description": "Test desc",
            "content": "Test content",
            "author": user,
        }

    def test_form_has_necessary_fields(self):
        form = RecipeForm(data=self.form_input)
        self.assertIn("title", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("content", form.fields)
        self.assertIn("thumbnail", form.fields)

    def test_valid_form(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input["title"] = ""
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_rejects_blank_content(self):
        self.form_input["content"] = ""
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_form_accepts_blank_description(self):
        self.form_input["description"] = ""
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_title_exceeding_max_length(self):
        self.form_input["title"] = "x" * 201
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_accepts_title_at_max_length(self):
        self.form_input["title"] = "x" * 200
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_valid_image_file(self):
        fixtures_dir = os.path.join(os.path.dirname(__file__), "..", "fixtures")
        image_path = os.path.join(fixtures_dir, "burger.png")

        with open(image_path, "rb") as img_file:
            thumbnail = SimpleUploadedFile(
                name="burger.png",
                content=img_file.read(),
                content_type="image/png",
            )
            form = RecipeForm(data=self.form_input, files={"thumbnail": thumbnail})
            self.assertTrue(form.is_valid())

    def test_form_rejects_non_image_file(self):
        # Create a fake text file pretending to be an image
        fake_image = SimpleUploadedFile(
            name="test.txt", content=b"This is not an image", content_type="text/plain"
        )
        form = RecipeForm(data=self.form_input, files={"thumbnail": fake_image})
        self.assertFalse(form.is_valid())
        self.assertIn("thumbnail", form.errors)

    def test_form_rejects_invalid_image_file(self):
        # Create a file with image extension but invalid content
        invalid_image = SimpleUploadedFile(
            name="invalid.jpg",
            content=b"Not a valid image content",
            content_type="image/jpeg",
        )
        form = RecipeForm(data=self.form_input, files={"thumbnail": invalid_image})
        self.assertFalse(form.is_valid())
        self.assertIn("thumbnail", form.errors)
