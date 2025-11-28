from django.test import TestCase

class ErrorView404Test(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]
    def test_404_error_view(self):
        response = self.client.get('/random-url/') # random url to trigger 404
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404_error.html')