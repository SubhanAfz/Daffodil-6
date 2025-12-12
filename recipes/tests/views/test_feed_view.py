"""Tests of the feed view."""

from django.test import TestCase
from django.urls import reverse

from recipes.models import Follow, Like, Recipe, User
from recipes.tests.helpers import RECIPE_FIXTURES


class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = RECIPE_FIXTURES

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse("feed")

    def test_feed_url(self):
        """Test that the feed URL is correct."""
        self.assertEqual(self.url, "/feed/")

    def test_unauthenticated_user_redirected(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/log_in/?next={self.url}")

    def test_authenticated_user_can_access_feed(self):
        """Test that authenticated users can access the feed."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feed.html")

    def test_popular_chefs_query(self):
        """Test that popular chefs are retrieved and ordered by follower count."""
        MAX_NUMBER_POPULAR_CHEFS = 10
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")
        user3 = User.objects.get(username="@petrapickles")
        user4 = User.objects.get(username="@peterpickles")

        # Make user2 popular with 3 followers
        Follow.objects.create(user=user2, follower=self.user)
        Follow.objects.create(user=user2, follower=user3)
        Follow.objects.create(user=user2, follower=user4)

        Follow.objects.create(user=user3, follower=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        popular_chefs = response.context["popular_chefs"]
        self.assertLessEqual(len(popular_chefs), MAX_NUMBER_POPULAR_CHEFS)

        self.assertEqual(popular_chefs[0], user2)

    def test_popular_chefs_limited_to_ten(self):
        """Test that only top 10 popular chefs are returned."""
        self.client.force_login(self.user)

        for i in range(11):
            User.objects.create(
                username=f"@user{i}",
                email=f"user{i}@example.com",
                first_name=f"User{i}",
                last_name="Test",
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        popular_chefs = response.context["popular_chefs"]
        self.assertEqual(len(popular_chefs), 10)

    def test_trending_recipes_query(self):
        """Test that trending recipes are retrieved and ordered by like count."""
        MAX_NUMBER_TRENDING = 10
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")
        user3 = User.objects.get(username="@petrapickles")

        recipe1 = Recipe.objects.get(pk=1)
        recipe2 = Recipe.objects.get(pk=2)

        Like.objects.create(user=self.user, recipe=recipe1)
        Like.objects.create(user=user2, recipe=recipe1)
        Like.objects.create(user=user3, recipe=recipe1)

        Like.objects.create(user=self.user, recipe=recipe2)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        trending_recipes = response.context["trending_recipes"]
        self.assertLessEqual(len(trending_recipes), MAX_NUMBER_TRENDING)

        self.assertEqual(trending_recipes[0], recipe1)

    def test_trending_recipes_excludes_hidden(self):
        """Test that hidden recipes are excluded from trending."""
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")

        hidden_recipe = Recipe.objects.get(pk=4)
        self.assertTrue(hidden_recipe.is_hidden)

        Like.objects.create(user=self.user, recipe=hidden_recipe)
        Like.objects.create(user=user2, recipe=hidden_recipe)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        trending_recipes = response.context["trending_recipes"]

        self.assertNotIn(hidden_recipe, trending_recipes)

    def test_trending_recipes_limited_to_ten(self):
        """Test that only top 10 trending recipes are returned."""
        self.client.force_login(self.user)

        for i in range(11):
            Recipe.objects.create(
                title=f"Recipe {i}",
                description=f"Description {i}",
                content=f"Content {i}",
                author=self.user,
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        trending_recipes = response.context["trending_recipes"]
        self.assertEqual(len(trending_recipes), 10)

    def test_explore_recipes_based_on_follows(self):
        """Test that explore shows recipes from followed users."""
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")

        Follow.objects.create(user=user2, follower=self.user)

        user2_recipes = Recipe.objects.filter(author=user2, is_hidden=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        # User2's recipes should be in explore
        for recipe in user2_recipes:
            self.assertIn(recipe, explore_recipes)

    def test_explore_recipes_based_on_likes(self):
        """Test that explore shows recipes from authors of liked recipes."""
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.get(pk=1)

        Like.objects.create(user=self.user, recipe=recipe1)

        author = recipe1.author
        author_recipes = Recipe.objects.filter(author=author, is_hidden=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        for recipe in author_recipes:
            if recipe.author != self.user:
                self.assertIn(recipe, explore_recipes)

    def test_explore_recipes_excludes_current_user(self):
        """Test that the current user's own recipes are excluded from explore."""
        self.client.force_login(self.user)

        user_recipe = Recipe.objects.create(
            title="My Recipe",
            description="My Description",
            content="My Content",
            author=self.user,
        )

        user2 = User.objects.get(username="@janedoe")
        Follow.objects.create(user=user2, follower=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        self.assertNotIn(user_recipe, explore_recipes)

    def test_explore_recipes_excludes_hidden(self):
        """Test that hidden recipes are excluded from explore."""
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")

        Follow.objects.create(user=user2, follower=self.user)

        hidden_recipes = Recipe.objects.filter(author=user2, is_hidden=True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        for recipe in hidden_recipes:
            self.assertNotIn(recipe, explore_recipes)

    def test_explore_recipes_limited_to_fifty(self):
        """Test that explore recipes are limited to 50."""
        self.client.force_login(self.user)

        followed_user = User.objects.get(username="@janedoe")

        Follow.objects.create(user=followed_user, follower=self.user)

        for i in range(51):
            Recipe.objects.create(
                title=f"Recipe {i}",
                description=f"Description {i}",
                content=f"Content {i}",
                author=followed_user,
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]
        self.assertEqual(len(explore_recipes), 50)

    def test_fallback_when_no_follows_or_likes(self):
        """Test that random recipes are shown when user has no follows or likes."""
        self.client.force_login(self.user)

        Follow.objects.filter(follower=self.user).delete()
        Like.objects.filter(user=self.user).delete()

        user2 = User.objects.get(username="@janedoe")
        Recipe.objects.create(
            title="Random Recipe 1",
            description="Description 1",
            content="Content 1",
            author=user2,
        )
        Recipe.objects.create(
            title="Random Recipe 2",
            description="Description 2",
            content="Content 2",
            author=user2,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        # Should have some recipes (fallback random recipes)
        self.assertGreater(len(explore_recipes), 0)

    def test_fallback_excludes_current_user_recipes(self):
        """Test that fallback random recipes exclude current user's recipes."""
        self.client.force_login(self.user)

        Follow.objects.filter(follower=self.user).delete()
        Like.objects.filter(user=self.user).delete()

        user_recipe = Recipe.objects.create(
            title="My Recipe",
            description="My Description",
            content="My Content",
            author=self.user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        self.assertNotIn(user_recipe, explore_recipes)

    def test_fallback_excludes_hidden_recipes(self):
        """Test that fallback random recipes exclude hidden recipes."""
        self.client.force_login(self.user)

        Follow.objects.filter(follower=self.user).delete()
        Like.objects.filter(user=self.user).delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        for recipe in explore_recipes:
            self.assertFalse(recipe.is_hidden)

    def test_fallback_limited_to_fifty(self):
        """Test that fallback recipes are limited to 50."""
        self.client.force_login(self.user)

        Follow.objects.filter(follower=self.user).delete()
        Like.objects.filter(user=self.user).delete()

        user2 = User.objects.get(username="@janedoe")

        for i in range(51):
            Recipe.objects.create(
                title=f"Recipe {i}",
                description=f"Description {i}",
                content=f"Content {i}",
                author=user2,
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]
        self.assertEqual(len(explore_recipes), 50)

    def test_context_contains_all_required_keys(self):
        """Test that the context contains all required keys."""
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertIn("popular_chefs", response.context)
        self.assertIn("trending_recipes", response.context)
        self.assertIn("explore_recipes", response.context)
        self.assertIn("recipes", response.context)

    def test_recipes_context_equals_explore_recipes(self):
        """Test that 'recipes' context is the same as 'explore_recipes'."""
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        recipes = list(response.context["recipes"])
        explore_recipes = list(response.context["explore_recipes"])

        self.assertEqual(recipes, explore_recipes)

    def test_explore_ordered_by_created_at_descending(self):
        """Test that explore recipes are ordered by created_at descending."""
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")

        Follow.objects.create(user=user2, follower=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = response.context["explore_recipes"]

        if len(explore_recipes) > 1:
            for i in range(len(explore_recipes) - 1):
                self.assertGreaterEqual(
                    explore_recipes[i].created_at, explore_recipes[i + 1].created_at
                )

    def test_post_request_gives_405(self):
        """Test that POST requests return 405 Method Not Allowed."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")

    def test_explore_no_duplicates_from_follow_and_like(self):
        """Test that recipes don't appear twice if author is both followed and liked."""
        self.client.force_login(self.user)

        user2 = User.objects.get(username="@janedoe")
        recipe2 = Recipe.objects.get(pk=2)

        Follow.objects.create(user=user2, follower=self.user)

        Like.objects.create(user=self.user, recipe=recipe2)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        explore_recipes = list(response.context["explore_recipes"])

        recipe_ids = [recipe.id for recipe in explore_recipes]
        self.assertEqual(len(recipe_ids), len(set(recipe_ids)))
