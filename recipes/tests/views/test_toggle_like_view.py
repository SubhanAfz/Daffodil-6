from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Like


class ToggleLikeViewTest(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.recipe = Recipe.objects.get(pk=1)
        self.url = reverse("toggle_like", args=[self.recipe.pk])

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_toggle_like_removes_like_when_already_liked(self):
        Like.objects.create(user=self.user, recipe=self.recipe)
        like_exists = Like.objects.filter(
            user=self.user, recipe=self.recipe
        ).exists()
        self.assertTrue(like_exists)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        like_exists = Like.objects.filter(
            user=self.user, recipe=self.recipe
        ).exists()
        self.assertFalse(like_exists)

    def test_toggle_like_adds_like_when_not_liked(self):
        like_exists = Like.objects.filter(user=self.user, recipe=self.recipe).exists()
        self.assertFalse(like_exists)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        like_exists = Like.objects.filter(user=self.user, recipe=self.recipe).exists()
        self.assertTrue(like_exists)
