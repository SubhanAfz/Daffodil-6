from django.test import TestCase
from django.urls import reverse
from recipes.tests.helpers import CommonTestMixin


class ReportsListViewTest(TestCase, CommonTestMixin):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/reports.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]

    def setUp(self):
        self.url = reverse("reports_list")

    def test_non_staff_user_receives_403(self):
        """Test that non-staff users receive a 403 error when accessing reports list."""

        self.client.login(username="@johndoe", password="Password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403_error.html")

    def test_default_order(self):
        """Test the default order when requesting without order is asc."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url)

        self.assertEqual(response.context["order"], "asc")

    def test_order_asc(self):
        """Test the order of reports is correct when requesting order is asc."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url, {"order": "asc"})

        list = response.context["list"]

        report_times = []
        for report in list:
            report_times.append(report.report_time)

        self.assertEqual(report_times, sorted(report_times, reverse=True))

    def test_order_desc(self):
        """Test the order of reports is correct when requesting order is desc."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url, {"order": "desc"})

        list = response.context["list"]

        report_times = []
        for report in list:
            report_times.append(report.report_time)

        self.assertEqual(report_times, sorted(report_times))

    def test_order_post(self):
        """Test list returned is posts in descending order of num_reports."""

        self.client.login(username="@superuser", password="Password123")
        response = self.client.get(self.url, {"order": "posts"})

        list = response.context["list"]

        num_reports = []
        for post in list:
            num_reports.append(post.num_reports)

        self.assertEqual(num_reports, sorted(num_reports, reverse=True))
