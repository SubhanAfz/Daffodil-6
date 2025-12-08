"""Tests for the search view."""

from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Tag, Like
from recipes.tests.helpers import STANDARD_FIXTURES


class SearchViewTestCase(TestCase):
    """Tests for the search view."""

    fixtures = STANDARD_FIXTURES

    def setUp(self):
        """Set up test data for search tests."""
        self.url = reverse("search")

        self.user1 = User.objects.get(username="@johndoe")
        self.user2 = User.objects.get(username="@janedoe")

        self.tag_italian = Tag.objects.create(name="italian")
        self.tag_spicy = Tag.objects.create(name="spicy")
        self.tag_vegetarian = Tag.objects.create(name="vegetarian")

        self.recipe1 = Recipe.objects.get(pk=1)
        self.tag_italian.recipes.add(self.recipe1)

        self.recipe2 = Recipe.objects.get(pk=2)
        self.tag_spicy.recipes.add(self.recipe2)

        self.recipe3 = Recipe.objects.get(pk=3)
        self.tag_italian.recipes.add(self.recipe3)
        self.tag_vegetarian.recipes.add(self.recipe3)

        self.hidden_recipe = Recipe.objects.get(pk=4)
        self.hidden_recipe.is_hidden = True
        self.hidden_recipe.save()

        Like.objects.create(user=self.user1, recipe=self.recipe1)
        Like.objects.create(user=self.user2, recipe=self.recipe1)

    def test_search_url(self):
        """Test the search URL resolves correctly."""
        self.assertEqual(self.url, "/search/")

    def test_get_search_without_parameters(self):
        """Test GET request without any search parameters shows all non-hidden recipes."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(response.context["result_count"], 3)
        self.assertIn(self.recipe1, response.context["recipes"])
        self.assertIn(self.recipe2, response.context["recipes"])
        self.assertIn(self.recipe3, response.context["recipes"])
        self.assertNotIn(self.hidden_recipe, response.context["recipes"])

    def test_search_by_keyword_in_title(self):
        """Test searching by keyword in recipe title."""
        response = self.client.get(self.url, {"q": "Potatoes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 1)
        self.assertIn(self.recipe1, response.context["recipes"])
        self.assertNotIn(self.recipe2, response.context["recipes"])

    def test_search_by_keyword_in_description(self):
        """Test searching by keyword in recipe description."""
        response = self.client.get(self.url, {"q": "warming"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 1)
        self.assertIn(self.recipe2, response.context["recipes"])

    def test_search_by_keyword_case_insensitive(self):
        """Test that keyword search is case insensitive."""
        response = self.client.get(self.url, {"q": "CHOCOLATE"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 1)
        self.assertIn(self.recipe3, response.context["recipes"])

    def test_search_by_single_tag(self):
        """Test filtering by a single tag."""
        response = self.client.get(self.url, {"tags": "italian"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 2)
        self.assertIn(self.recipe1, response.context["recipes"])
        self.assertIn(self.recipe3, response.context["recipes"])
        self.assertNotIn(self.recipe2, response.context["recipes"])

    def test_search_by_multiple_tags(self):
        """Test filtering by multiple tags (OR logic)."""
        response = self.client.get(self.url, {"tags": "italian,spicy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 3)

    def test_search_by_ingredients(self):
        """Test searching by ingredients."""
        response = self.client.get(self.url, {"ingredients": "lentils"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 1)
        self.assertIn(self.recipe2, response.context["recipes"])

    def test_search_with_multiple_filters(self):
        """Test combining keyword, tags, and ingredients."""
        response = self.client.get(
            self.url, {"q": "chocolate", "tags": "vegetarian", "ingredients": "eggs"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 1)
        self.assertIn(self.recipe3, response.context["recipes"])

    def test_sort_by_newest(self):
        """Test sorting by newest (default)."""
        response = self.client.get(self.url, {"sort": "newest"})
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context["recipes"])

        self.assertEqual(recipes[0], self.recipe3)

    def test_sort_by_oldest(self):
        """Test sorting by oldest."""
        response = self.client.get(self.url, {"sort": "oldest"})
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context["recipes"])

        self.assertEqual(recipes[0], self.recipe1)

    def test_sort_by_most_viewed(self):
        """Test sorting by most viewed."""
        response = self.client.get(self.url, {"sort": "most_viewed"})
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context["recipes"])
        # recipe3 has 87 views, recipe2 has 42, recipe1 has 12
        self.assertEqual(recipes[0], self.recipe3)
        self.assertEqual(recipes[1], self.recipe2)
        self.assertEqual(recipes[2], self.recipe1)

    def test_sort_by_most_liked(self):
        """Test sorting by most liked."""
        response = self.client.get(self.url, {"sort": "most_liked"})
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context["recipes"])
        self.assertEqual(recipes[0], self.recipe1)

    def test_search_with_no_results(self):
        """Test search with no matching results."""
        response = self.client.get(self.url, {"q": "nonexistent recipe"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertEqual(len(response.context["recipes"]), 0)

    def test_hidden_recipes_not_shown(self):
        """Test that hidden recipes are filtered out."""
        response = self.client.get(self.url, {"q": "Hidden"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertNotIn(self.hidden_recipe, response.context["recipes"])

    def test_all_tags_in_context(self):
        """Test that all tags are included in context."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        all_tags = list(response.context["all_tags"])
        self.assertEqual(len(all_tags), 3)
        self.assertIn(self.tag_italian, all_tags)
        self.assertIn(self.tag_spicy, all_tags)
        self.assertIn(self.tag_vegetarian, all_tags)

    def test_search_params_in_context(self):
        """Test that search parameters are preserved in context."""
        response = self.client.get(
            self.url,
            {
                "q": "pasta",
                "tags": "italian",
                "ingredients": "eggs",
                "sort": "most_liked",
            },
        )
        self.assertEqual(response.status_code, 200)
        search_params = response.context["search_params"]
        self.assertEqual(search_params["keyword"], "pasta")
        self.assertEqual(search_params["tags"], "italian")
        self.assertEqual(search_params["ingredients"], "eggs")
        self.assertEqual(search_params["sort_by"], "most_liked")

    def test_empty_tag_query_ignored(self):
        """Test that empty tag query is ignored."""
        response = self.client.get(self.url, {"tags": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 3)

    def test_tag_query_with_spaces(self):
        """Test that tag names with spaces are handled correctly."""
        response = self.client.get(self.url, {"tags": " italian , spicy "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 3)

    def test_likes_count_annotated(self):
        """Test that likes count is properly annotated."""
        response = self.client.get(self.url)
        recipes = response.context["recipes"]
        recipe1_in_context = next(r for r in recipes if r.id == self.recipe1.id)
        self.assertEqual(recipe1_in_context.likes_count, 2)
