from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Followers


class ToggleFollowViewTest(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.other_user = User.objects.get(username="@janedoe")
        self.client.force_login(self.user)
        self.url = reverse("toggle_follow", args=[self.other_user.pk])

    def test_unauthenticated_access(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn("/log_in/", response.url)

    def test_toggle_follow_unfollows_when_already_following(self):
        """Test that following a user you already follow will unfollow them."""
        # Create the follow relationship first
        Followers.objects.create(user=self.other_user, follower=self.user)
        follow_exists = Followers.objects.filter(
            user=self.other_user, follower=self.user
        ).exists()
        self.assertTrue(follow_exists)

        # Toggle to unfollow
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect

        # Verify the follow relationship was removed
        follow_exists = Followers.objects.filter(
            user=self.other_user, follower=self.user
        ).exists()
        self.assertFalse(follow_exists)

    def test_toggle_follow_follows_when_not_following(self):
        """Test that following a user you don't follow will create the relationship."""
        # Verify no follow relationship exists
        follow_exists = Followers.objects.filter(
            user=self.other_user, follower=self.user
        ).exists()
        self.assertFalse(follow_exists)

        # Toggle to follow
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect

        # Verify the follow relationship was created
        follow_exists = Followers.objects.filter(
            user=self.other_user, follower=self.user
        ).exists()
        self.assertTrue(follow_exists)

    def test_cannot_follow_yourself(self):
        """Test that a user cannot follow themselves."""
        self_url = reverse("toggle_follow", args=[self.user.pk])
        response = self.client.post(self_url)
        self.assertEqual(response.status_code, 302)  # Redirect

        # Verify no self-follow relationship was created
        self_follow_exists = Followers.objects.filter(
            user=self.user, follower=self.user
        ).exists()
        self.assertFalse(self_follow_exists)

    def test_get_request_returns_405(self):
        """Test that GET requests are not allowed."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")

    def test_toggle_follow_with_nonexistent_user(self):
        """Test that following a non-existent user returns 404."""
        non_existent_url = reverse("toggle_follow", args=[99999])
        response = self.client.post(non_existent_url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_to_referer(self):
        """Test that the view redirects to the HTTP_REFERER."""
        referer_url = reverse("dashboard")
        response = self.client.post(self.url, HTTP_REFERER=referer_url)
        self.assertRedirects(response, referer_url, fetch_redirect_response=False)

    def test_redirect_to_dashboard_when_no_referer(self):
        """Test that the view redirects to dashboard when no HTTP_REFERER."""
        response = self.client.post(self.url)
        self.assertRedirects(
            response, reverse("dashboard"), fetch_redirect_response=False
        )

    def test_toggle_follow_updates_follower_count(self):
        """Test that following/unfollowing updates the follower count correctly."""
        # Initial follower count
        initial_count = self.other_user.followers.count()

        # Follow the user
        self.client.post(self.url)
        self.assertEqual(self.other_user.followers.count(), initial_count + 1)

        # Unfollow the user
        self.client.post(self.url)
        self.assertEqual(self.other_user.followers.count(), initial_count)

    def test_toggle_follow_updates_following_count(self):
        """Test that following/unfollowing updates the following count correctly."""
        # Initial following count
        initial_count = self.user.followers_of.count()

        # Follow the user
        self.client.post(self.url)
        self.assertEqual(self.user.followers_of.count(), initial_count + 1)

        # Unfollow the user
        self.client.post(self.url)
        self.assertEqual(self.user.followers_of.count(), initial_count)
