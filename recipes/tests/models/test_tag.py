"""Unit tests for the Tag model."""

from django.test import TestCase
from recipes.models import Tag, Recipe, User


class TagModelTestCase(TestCase):
    """Unit tests for the Tag model."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    def setUp(self):
        """Set up test data for tag tests."""
        self.user = User.objects.get(username="@johndoe")

        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            content="Test content",
            author=self.user,
        )

        self.tag = Tag.objects.create(name="italian")

    def test_tag_creation(self):
        """Test that a tag can be created."""
        self.assertEqual(self.tag.name, "italian")
        self.assertIsInstance(self.tag, Tag)

    def test_tag_str_representation(self):
        """Test the string representation of a tag."""
        self.assertEqual(str(self.tag), "italian")

    def test_add_recipe_to_tag(self):
        """Test adding a recipe to a tag."""
        self.tag.recipes.add(self.recipe)
        self.assertIn(self.recipe, self.tag.recipes.all())
        self.assertEqual(self.tag.recipes.count(), 1)

    def test_add_multiple_recipes_to_tag(self):
        """Test adding multiple recipes to a tag."""
        recipe2 = Recipe.objects.create(
            title="Second Recipe",
            description="Another test recipe",
            ingredients="More ingredients",
            content="More content",
            author=self.user,
        )
        self.tag.recipes.add(self.recipe, recipe2)
        self.assertEqual(self.tag.recipes.count(), 2)
        self.assertIn(self.recipe, self.tag.recipes.all())
        self.assertIn(recipe2, self.tag.recipes.all())

    def test_recipe_has_tags_via_related_name(self):
        """Test accessing tags from a recipe using the related_name."""
        self.tag.recipes.add(self.recipe)
        self.assertIn(self.tag, self.recipe.tags.all())
        self.assertEqual(self.recipe.tags.count(), 1)

    def test_multiple_tags_on_recipe(self):
        """Test adding multiple tags to a single recipe."""
        tag2 = Tag.objects.create(name="spicy")
        tag3 = Tag.objects.create(name="vegetarian")

        tag2.recipes.add(self.recipe)
        tag3.recipes.add(self.recipe)
        self.tag.recipes.add(self.recipe)

        self.assertEqual(self.recipe.tags.count(), 3)
        self.assertIn(self.tag, self.recipe.tags.all())
        self.assertIn(tag2, self.recipe.tags.all())
        self.assertIn(tag3, self.recipe.tags.all())

    def test_remove_recipe_from_tag(self):
        """Test removing a recipe from a tag."""
        self.tag.recipes.add(self.recipe)
        self.assertEqual(self.tag.recipes.count(), 1)

        self.tag.recipes.remove(self.recipe)
        self.assertEqual(self.tag.recipes.count(), 0)
        self.assertNotIn(self.recipe, self.tag.recipes.all())

    def test_clear_all_recipes_from_tag(self):
        """Test clearing all recipes from a tag."""
        recipe2 = Recipe.objects.create(
            title="Second Recipe",
            description="Another test recipe",
            ingredients="More ingredients",
            content="More content",
            author=self.user,
        )

        self.tag.recipes.add(self.recipe, recipe2)
        self.assertEqual(self.tag.recipes.count(), 2)

        self.tag.recipes.clear()
        self.assertEqual(self.tag.recipes.count(), 0)

    def test_get_or_create_tag(self):
        """Test get_or_create functionality for tags."""
        tag, created = Tag.objects.get_or_create(name="italian")
        self.assertFalse(created)
        self.assertEqual(tag, self.tag)

        new_tag, created = Tag.objects.get_or_create(name="chinese")
        self.assertTrue(created)
        self.assertEqual(new_tag.name, "chinese")

    def test_tag_name_max_length(self):
        """Test that tag name respects max_length."""
        long_name = "a" * 200
        tag = Tag.objects.create(name=long_name)
        self.assertEqual(len(tag.name), 200)

    def test_delete_tag_keeps_recipe(self):
        """Test that deleting a tag doesn't delete the recipe."""
        self.tag.recipes.add(self.recipe)
        tag_id = self.tag.id
        recipe_id = self.recipe.id

        self.tag.delete()

        self.assertFalse(Tag.objects.filter(id=tag_id).exists())
        self.assertTrue(Recipe.objects.filter(id=recipe_id).exists())

    def test_unique_recipes_in_tag(self):
        """Test that a recipe cannot be added multiple times to the same tag."""
        self.tag.recipes.add(self.recipe)
        self.tag.recipes.add(self.recipe)  # Attempt to add again

        self.assertEqual(self.tag.recipes.count(), 1)
