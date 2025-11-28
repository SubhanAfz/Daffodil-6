from django.test import TestCase, RequestFactory
from recipes.views import error_500_view

class ErrorView500Test(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
        "recipes/tests/fixtures/reports.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]
        
    def test_500_error_view(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = error_500_view(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'500 Error', response.content)
