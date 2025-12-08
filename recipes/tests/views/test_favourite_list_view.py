from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Favourite
from recipes.tests.helpers import STANDARD_FIXTURES, CommonTestMixin


class FavouriteListViewTest(TestCase, CommonTestMixin):
    fixtures = STANDARD_FIXTURES

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.recipe = Recipe.objects.get(pk=1)
        self.url = reverse("favourite_list")

    def test_favourite_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourites.html")

    def test_unauthenticated_access(self):
        self.assert_unauthenticated_redirect(self.url)

    def test_empty_favourite_list(self):
        self.assert_no_recipes_text(self.client.get(self.url))

    def test_favourite_list_with_favourites(self):
        self.assert_no_recipes_text(self.client.get(self.url))
        Favourite.objects.create(user=self.user, recipe=self.recipe)
        self.assert_has_recipes(self.client.get(self.url))

    def test_post_gives_405(self):
        self.assert_405_on_post(self.url)
