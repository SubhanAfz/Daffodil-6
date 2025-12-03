from django.test import TestCase
from recipes.forms import RecipeForm
from django.contrib.auth import get_user_model

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

    def test_valid_form(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
