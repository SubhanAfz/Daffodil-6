from django.test import TestCase
from recipes.models import User, Recipe, Favourite, Like, Tag
from django.urls import reverse
from recipes.tests.helpers import STANDARD_FIXTURES


class RecipeDetailViewTest(TestCase):
    fixtures = STANDARD_FIXTURES

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.recipe = Recipe.objects.get(pk=1)
        self.tag = Tag.objects.create(name="dessert")
        self.url = reverse("recipe_detail", args=[self.recipe.pk])

    def test_get_recipe_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_favourite_button_appears_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, 'id="favourite-button"')

    def test_like_button_appears_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, 'id="like-button"')

    def test_favourite_button_does_not_appear_for_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, 'id="favourite-button"')

    def test_like_button_does_not_appear_for_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, 'id="like-button"')

    def test_view_count_increments_on_access(self):
        initial_views = self.recipe.views
        self.client.get(self.url)

        self.recipe.refresh_from_db()

        self.assertEqual(self.recipe.views, initial_views + 1)

    def test_favourite_count(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        initial_favourites = response.context["favourites"]

        Favourite.objects.create(user=self.user, recipe=self.recipe)

        response = self.client.get(self.url)

        self.assertEqual(response.context["favourites"], initial_favourites + 1)

    def test_like_count(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        initial_likes = response.context["likes"]

        Like.objects.create(user=self.user, recipe=self.recipe)

        response = self.client.get(self.url)

        self.assertEqual(response.context["likes"], initial_likes + 1)

    def test_tags_showing(self):
        self.tag.recipes.add(self.recipe)
        response = self.client.get(self.url)
        tags = self.recipe.tags.all()
        for tag in tags:
            self.assertContains(response, tag.name)

    def test_tags_not_showing_when_none(self):
        response = self.client.get(self.url)
        tags = self.recipe.tags.all()
        self.assertEqual(tags.count(), 0)
        self.assertNotContains(response, self.tag.name)
