from django.test import TestCase
from django.db import IntegrityError
from recipes.models import Follow, User


class FollowModelTest(TestCase):
    """Unit tests for Follow model."""

    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user1 = User.objects.get(username="@johndoe")
        self.user2 = User.objects.get(username="@janedoe")

    def test_create_follower_relationship(self):
        """Test creating a Follow instance."""
        follow = Follow.objects.create(user=self.user1, follower=self.user2)
        self.assertIsInstance(follow, Follow)
        self.assertEqual(follow.user, self.user1)
        self.assertEqual(follow.follower, self.user2)

    def test_unique_follow_constraint(self):
        """Test that a user cannot follow the same user more than once."""
        Follow.objects.create(user=self.user1, follower=self.user2)
        with self.assertRaises(IntegrityError):
            Follow.objects.create(user=self.user1, follower=self.user2)

    def test_user_can_follow_multiple_users(self):
        """Test that a user can follow multiple users."""
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")

        Follow.objects.create(user=self.user1, follower=self.user2)
        Follow.objects.create(user=user3, follower=self.user2)

        following_count = self.user2.followers_of.count()
        self.assertEqual(following_count, 2)

    def test_user_can_have_multiple_followers(self):
        """Test that a user can have multiple followers."""
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")

        Follow.objects.create(user=self.user1, follower=self.user2)
        Follow.objects.create(user=self.user1, follower=user3)

        follower_count = self.user1.followers.count()
        self.assertEqual(follower_count, 2)

    def test_cascade_delete_on_user_being_followed(self):
        """Test that deleting a user deletes their follower relationships."""
        follow = Follow.objects.create(user=self.user1, follower=self.user2)
        self.user1.delete()
        self.assertFalse(Follow.objects.filter(pk=follow.pk).exists())

    def test_cascade_delete_on_follower(self):
        """Test that deleting a follower deletes their following relationships."""
        follow = Follow.objects.create(user=self.user1, follower=self.user2)
        self.user2.delete()
        self.assertFalse(Follow.objects.filter(pk=follow.pk).exists())

    def test_str_representation(self):
        """Test the string representation of a Follow instance."""
        follow = Follow.objects.create(user=self.user1, follower=self.user2)
        expected_str = f"{self.user2} follows {self.user1}"
        self.assertEqual(str(follow), expected_str)

    def test_created_at_auto_set(self):
        """Test that created_at is automatically set."""
        follow = Follow.objects.create(user=self.user1, follower=self.user2)
        self.assertIsNotNone(follow.created_at)

    def test_followers_related_name(self):
        """Test that the 'followers' related name works correctly."""
        Follow.objects.create(user=self.user1, follower=self.user2)

        # user1.followers should return followers of user1
        followers = self.user1.followers.all()
        self.assertEqual(followers.count(), 1)
        self.assertEqual(followers.first().follower, self.user2)

    def test_followers_of_related_name(self):
        """Test that the 'followers_of' related name works correctly."""
        Follow.objects.create(user=self.user1, follower=self.user2)

        # user2.followers_of should return who user2 is following
        following = self.user2.followers_of.all()
        self.assertEqual(following.count(), 1)
        self.assertEqual(following.first().user, self.user1)

    def test_get_follower_users(self):
        """Test getting the actual User objects who are followers."""
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")

        Follow.objects.create(user=self.user1, follower=self.user2)
        Follow.objects.create(user=self.user1, follower=user3)

        # Get actual follower User objects
        follower_users = User.objects.filter(followers_of__user=self.user1)
        self.assertEqual(follower_users.count(), 2)
        self.assertIn(self.user2, follower_users)
        self.assertIn(user3, follower_users)

    def test_get_following_users(self):
        """Test getting the actual User objects a user is following."""
        user3 = User.objects.create(username="@jimsmith", email="jim@example.com")

        Follow.objects.create(user=self.user1, follower=self.user2)
        Follow.objects.create(user=user3, follower=self.user2)

        # Get actual User objects that user2 is following
        following_users = User.objects.filter(followers__follower=self.user2)
        self.assertEqual(following_users.count(), 2)
        self.assertIn(self.user1, following_users)
        self.assertIn(user3, following_users)

    def test_check_if_user_follows_another(self):
        """Test checking if one user follows another."""
        Follow.objects.create(user=self.user1, follower=self.user2)

        # Check if user2 follows user1
        is_following = Follow.objects.filter(
            user=self.user1, follower=self.user2
        ).exists()
        self.assertTrue(is_following)

        # Check if user1 follows user2 (should be False)
        is_following_reverse = Follow.objects.filter(
            user=self.user2, follower=self.user1
        ).exists()
        self.assertFalse(is_following_reverse)

    def test_mutual_following(self):
        """Test that two users can follow each other."""
        # user2 follows user1
        Follow.objects.create(user=self.user1, follower=self.user2)
        # user1 follows user2
        Follow.objects.create(user=self.user2, follower=self.user1)

        # Both should have 1 follower and be following 1 person
        self.assertEqual(self.user1.followers.count(), 1)
        self.assertEqual(self.user1.followers_of.count(), 1)
        self.assertEqual(self.user2.followers.count(), 1)
        self.assertEqual(self.user2.followers_of.count(), 1)
