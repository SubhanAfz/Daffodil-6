from django.forms import ValidationError
from django.test import TestCase
from recipes.models.recipe import Recipe


class RecipeModelTestCase(TestCase):
    """Unit tests for recipe model."""

    fixtures = [
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/reports.json",
    ]

    def setUp(self):
        self.recipe = Recipe.objects.get(id=6)

    def test_report_info_str_reported(self):
        """Test report_info_str method for a reported recipe"""
        self.recipe.is_reported = True
        self.recipe.num_reports = 3
        self.recipe.save()
        expected = f'"{self.recipe.title}" by {self.recipe.author.username} has been reported {self.recipe.num_reports} times.'
        actual = self.recipe.report_info_str()
        self.assertEqual(expected, actual)

    def test_report_info_str_not_reported(self):
        """Test report_info_str method for a non-reported recipe"""
        self.recipe.is_reported = False
        self.recipe.num_reports = 0
        self.recipe.save()
        expected = f'This recipe "{self.recipe.title}" has not been reported.'
        actual = self.recipe.report_info_str()
        self.assertEqual(expected, actual)

    def test_valid_recipe(self):
        self._assert_recipe_is_valid()

    def test_title_must_be_less_than_200_characters(self):
        """Test validity of title with 201 characters"""

        self.recipe.title = "a" * 201
        self._assert_recipe_is_invalid()

        """Test validity of title with 200 characters"""
        self.recipe.title = "a" * 200
        self._assert_recipe_is_valid()

    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
