from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Like


class LikeListViewTest(TestCase):
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
        self.url = reverse("like_list")

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_like_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "likes.html")

    def test_empty_like_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="no-likes-text"')

    def test_like_list_with_likes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="no-likes-text"')
        Like.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="no-likes-text"')

    def test_post_gives_405(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")
