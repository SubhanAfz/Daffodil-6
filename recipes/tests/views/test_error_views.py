from django.test import TestCase, RequestFactory


class ErrorViewsTest(TestCase):
    """Test suite for error views."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_404_view(self):
        response = self.client.get("/nonexistent-page/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404_error.html")
