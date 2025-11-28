from django.test import TestCase
from recipes.models import User
from django.urls import reverse

class ErrorView403Test(TestCase):
    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/superuser_user.json",
    ]
    def setUp(self):
        self.user = User.objects.get(username="@janedoe")
        self.client.force_login(self.user)
        self.url = reverse('reports_list') # a view where if the user is not staff, a 403 is raised  
    def test_403_error_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_error.html')