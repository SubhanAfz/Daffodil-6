from django.forms import ValidationError
from django.test import TestCase

from recipes.models.report import Report


class ReportModelTestCase(TestCase):
    fixtures = [
        "recipes/tests/fixtures/reports.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/default_user.json",
    ]

    def setUp(self):
        self.report = Report.objects.get(id=6)

    def test_report_reason_str_less_than_1200(self):
        """Test validity of reason with 1201 characters"""

        self.report.reason = "a" * 1201
        self._assert_report_is_invalid()

        """Test validity of reason with 1200 characters"""
        self.report.reason = "a" * 1200
        self._assert_report_is_valid()

    def test_valid_report(self):
        self._assert_report_is_valid()

    def _assert_report_is_valid(self):
        try:
            self.report.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_report_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.report.full_clean()
