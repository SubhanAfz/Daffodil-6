"""Tests of the user profile view."""

from django.test import TestCase, override_settings
from django.urls import reverse
from recipes.models import User, Recipe, Followers


class UserProfileViewTestCase(TestCase):
    """Tests of the user profile view."""

    fixtures = ["recipes/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("user_profile", kwargs={"username": "@johndoe"})

    def test_user_profile_url(self):
        self.assertEqual(self.url, "/users/@johndoe/")

    def test_get_user_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile.html")

    def test_get_user_profile_redirects_when_using_username_without_at_symbol(self):
        url = reverse("user_profile", kwargs={"username": "johndoe"})
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, self.url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, "user_profile.html")

    def test_get_user_profile_not_found(self):
        url = reverse("user_profile", kwargs={"username": "@nonexistentuser"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=False)
    def test_user_profile_not_found_template(self):
        url = reverse("user_profile", kwargs={"username": "@nonexistentuser"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404_error.html")

    def test_user_profile_showing_users_recipes(self):
        user = User.objects.get(username="@johndoe")
        Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            content="Test Content",
            author=user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Recipe")

    def test_user_profile_not_showing_other_users_recipes(self):
        user2 = User.objects.create(username="@janedoe")

        Recipe.objects.create(
            title="User2 Recipe",
            description="Test Description",
            content="Test Content",
            author=user2,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "User2 Recipe")

    def test_user_profile_no_recipes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes found.")

    def test_user_profile_shows_followers_count(self):
        """Test that the user profile displays the correct followers count."""
        profile_user = User.objects.get(username="@johndoe")

        # Create users to follow the profile user
        user2 = User.objects.create(username="@janedoe", email="jane@example.com")
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")

        # Create follow relationships
        Followers.objects.create(user=profile_user, follower=user2)
        Followers.objects.create(user=profile_user, follower=user3)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that followers count is 2
        self.assertEqual(response.context["followers"], 2)
        self.assertContains(response, '<span class="d-block fw-bold h4 mb-0">2</span>')

    def test_user_profile_shows_following_count(self):
        """Test that the user profile displays the correct following count."""
        profile_user = User.objects.get(username="@johndoe")

        # Create users for the profile user to follow
        user2 = User.objects.create(username="@janedoe", email="jane@example.com")
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")
        user4 = User.objects.create(username="@sarahjones", email="sarah@example.com")

        # Create follow relationships
        Followers.objects.create(user=user2, follower=profile_user)
        Followers.objects.create(user=user3, follower=profile_user)
        Followers.objects.create(user=user4, follower=profile_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that following count is 3
        self.assertEqual(response.context["following"], 3)
        self.assertContains(response, '<span class="d-block fw-bold h4 mb-0">3</span>')

    def test_follow_button_not_shown_when_not_authenticated(self):
        """Test that the follow button is not shown for unauthenticated users."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that the follow button is not present
        self.assertNotContains(response, 'id="follow-button"')

    def test_follow_button_not_shown_when_viewing_own_profile(self):
        """Test that the follow button is not shown when viewing your own profile."""
        user = User.objects.get(username="@johndoe")
        self.client.force_login(user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that the follow button is not present
        self.assertNotContains(response, 'id="follow-button"')

    def test_follow_button_shown_when_authenticated_viewing_other_profile(self):
        """Test that the follow button is shown when authenticated user views another user's profile."""
        # Create and login as a different user
        other_user = User.objects.create(username="@janedoe", email="jane@example.com")
        self.client.force_login(other_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that the follow button is present
        self.assertContains(response, 'id="follow-button"')
        self.assertContains(response, "Follow")

    def test_follow_button_shows_following_when_already_following(self):
        """Test that the follow button shows 'Following' when user is already following."""
        profile_user = User.objects.get(username="@johndoe")
        other_user = User.objects.create(username="@janedoe", email="jane@example.com")
        self.client.force_login(other_user)

        # Create follow relationship
        Followers.objects.create(user=profile_user, follower=other_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that button shows "Following"
        self.assertContains(response, "Following")
        self.assertContains(response, "btn-dark")

    def test_follow_button_shows_follow_when_not_following(self):
        """Test that the follow button shows 'Follow' when user is not following."""
        other_user = User.objects.create(username="@janedoe", email="jane@example.com")
        self.client.force_login(other_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that button shows "Follow"
        self.assertContains(response, 'id="follow-button"')
        self.assertContains(response, "btn-outline-dark")
        # Verify the button contains "Follow" but not "Following"
        self.assertRegex(
            response.content.decode(), r"<button[^>]*>\s*Follow\s*</button>"
        )
