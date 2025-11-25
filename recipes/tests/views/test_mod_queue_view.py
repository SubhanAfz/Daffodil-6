from django.test import TestCase
from django.urls import reverse
from recipes.models.recipe import Recipe

class ModQueueViewTest(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/reports.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.url = reverse("mod_queue")

    def test_default_order(self):
        """Test the default order when requesting without order is asc."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url)

        self.assertEqual(response.context["order"], "asc")

    def test_order_asc(self):
        """Test the order of posts is correct when requesting order is asc."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url, {"order": "asc"})

        list = response.context["list"]

        hide_times = []
        for recipe in list:
            hide_times.append(recipe.date_hidden)

        self.assertEqual(hide_times, sorted(hide_times))

    def test_order_desc(self):
        """Test the order of posts is correct when requesting order is desc."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url, {"order": "desc"})

        list = response.context["list"]

        hide_times = []
        for recipe in list:
            hide_times.append(recipe.date_hidden)

        self.assertEqual(hide_times, sorted(hide_times,reverse=True))
            
    def test_order_reports(self):
        """Test list returned is posts in descending order of num_reports."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url, {"order": "reports"})

        list = response.context["list"]

        num_reports =[]
        for post in list:
            num_reports.append(post.num_reports)

        self.assertEqual(num_reports, sorted(num_reports, reverse=True))

    def test_returns_all_hidden_posts(self):
        """Test all 3 key words return a list containing all hidden posts. """

        self.client.login(username="@superuser", password="Password123")
        hidden_items_set = set(Recipe.objects.filter(is_hidden=True))

        response = self.client.get(self.url, {"order": "asc"})
        asclist = response.context["list"]
        self.assertSetEqual(set(asclist),hidden_items_set)

        response = self.client.get(self.url, {"order": "desc"})
        desclist = response.context["list"]
        self.assertSetEqual(set(desclist),hidden_items_set)

        response = self.client.get(self.url, {"order": "reports"})
        num_reportslist = response.context["list"]
        self.assertSetEqual(set(num_reportslist),hidden_items_set)
