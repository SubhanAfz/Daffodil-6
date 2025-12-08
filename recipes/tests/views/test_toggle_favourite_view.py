from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Favourite
from recipes.tests.helpers import STANDARD_FIXTURES, CommonTestMixin


class ToggleFavouriteViewTest(TestCase, CommonTestMixin):
    fixtures = STANDARD_FIXTURES

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.recipe = Recipe.objects.get(pk=1)
        self.url = reverse("toggle_favourite", args=[self.recipe.pk])

    def test_unauthenticated_access(self):
        self.assert_unauthenticated_redirect(self.url)

    def test_get_toggle_favourite_renders_405_error(self):
        self.assert_405_on_get(self.url)

    def test_toggle_favourite_removes_favourite_when_already_favourited(self):
        Favourite.objects.create(user=self.user, recipe=self.recipe)
        favourite_exists = Favourite.objects.filter(
            user=self.user, recipe=self.recipe
        ).exists()
        self.assertTrue(favourite_exists)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        favourite_exists = Favourite.objects.filter(
            user=self.user, recipe=self.recipe
        ).exists()
        self.assertFalse(favourite_exists)

    def test_toggle_favourite_adds_favourite_when_not_favourited(self):
        favourite_exists = Favourite.objects.filter(
            user=self.user, recipe=self.recipe
        ).exists()
        self.assertFalse(favourite_exists)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("recipe_detail", args=[self.recipe.pk]))
        favourite_exists = Favourite.objects.filter(
            user=self.user, recipe=self.recipe
        ).exists()
        self.assertTrue(favourite_exists)
