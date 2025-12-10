from django.test import TestCase
from django.db import IntegrityError
from recipes.models import Favourite, Recipe, User
from recipes.tests.helpers import STANDARD_FIXTURES


class FavouriteModelTest(TestCase):
    """Unit tests for Favourite model."""

    fixtures = STANDARD_FIXTURES

    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)
        self.user = User.objects.get(username="@johndoe")

    def test_string_representation(self):
        """Test the string representation of a Favourite instance."""
        favourite = Favourite.objects.create(user=self.user, recipe=self.recipe)
        expected_str = f"{self.user.username} favourited {self.recipe.title}"
        self.assertEqual(str(favourite), expected_str)

    def test_create_favourite(self):
        """Test creating a Favourite instance."""
        favourite = Favourite.objects.create(user=self.user, recipe=self.recipe)
        self.assertIsInstance(favourite, Favourite)
        self.assertEqual(favourite.user, self.user)
        self.assertEqual(favourite.recipe, self.recipe)

    def test_unique_favourite_constraint(self):
        """Test that a user cannot favourite the same recipe more than once."""
        Favourite.objects.create(user=self.user, recipe=self.recipe)
        with self.assertRaises(IntegrityError):
            Favourite.objects.create(user=self.user, recipe=self.recipe)

    def test_cascade_delete_on_user(self):
        """Test that deleting a user deletes their favourites."""
        favourite = Favourite.objects.create(user=self.user, recipe=self.recipe)
        self.user.delete()
        self.assertFalse(Favourite.objects.filter(pk=favourite.pk).exists())

    def test_cascade_delete_on_recipe(self):
        """Test that deleting a recipe deletes its favourites."""
        favourite = Favourite.objects.create(user=self.user, recipe=self.recipe)
        self.recipe.delete()
        self.assertFalse(Favourite.objects.filter(pk=favourite.pk).exists())
