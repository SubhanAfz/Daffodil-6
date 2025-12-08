from django.test import TestCase
from django.db import IntegrityError
from recipes.models import Like, Recipe, User
from recipes.tests.helpers import STANDARD_FIXTURES


class LikeModelTest(TestCase):
    """Unit tests for Like model."""

    fixtures = STANDARD_FIXTURES

    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)
        self.user = User.objects.get(username="@johndoe")

    def test_create_like(self):
        """Test creating a Like instance."""
        like = Like.objects.create(user=self.user, recipe=self.recipe)
        self.assertIsInstance(like, Like)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.recipe, self.recipe)

    def test_unique_like_constraint(self):
        """Test that a user cannot like the same recipe more than once."""
        Like.objects.create(user=self.user, recipe=self.recipe)
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, recipe=self.recipe)

    def test_cascade_delete_on_user(self):
        """Test that deleting a user deletes their likes."""
        like = Like.objects.create(user=self.user, recipe=self.recipe)
        self.user.delete()
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())

    def test_cascade_delete_on_recipe(self):
        """Test that deleting a recipe deletes its likes."""
        like = Like.objects.create(user=self.user, recipe=self.recipe)
        self.recipe.delete()
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())
