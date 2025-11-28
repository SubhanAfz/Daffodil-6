from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Favourite


class FavouriteListViewTest(TestCase):
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
        self.url = reverse("favourite_list")

    def test_favourite_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourites.html")
        
    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_empty_favourite_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="no-favourites-text"')

    def test_favourite_list_with_favourites(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="no-favourites-text"')
        Favourite.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="no-favourites-text"')
