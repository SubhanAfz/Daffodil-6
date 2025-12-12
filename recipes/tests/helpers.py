from django.urls import reverse
from with_asserts.mixin import AssertHTMLMixin
import os
from django.core.files.uploadedfile import SimpleUploadedFile


def reverse_with_next(url_name, next_url):
    """Extended version of reverse to generate URLs with redirects"""
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url


# Common fixture lists for test classes
STANDARD_FIXTURES = [
    "recipes/tests/fixtures/default_user.json",
    "recipes/tests/fixtures/other_users.json",
    "recipes/tests/fixtures/recipes.json",
    "recipes/tests/fixtures/superuser_user.json",
]

MODERATION_FIXTURES = [
    "recipes/tests/fixtures/default_user.json",
    "recipes/tests/fixtures/other_users.json",
    "recipes/tests/fixtures/recipes.json",
    "recipes/tests/fixtures/reports.json",
    "recipes/tests/fixtures/staff_user.json",
    "recipes/tests/fixtures/superuser_user.json",
]

RECIPE_FIXTURES = [
    "recipes/tests/fixtures/default_user.json",
    "recipes/tests/fixtures/other_users.json",
    "recipes/tests/fixtures/recipes.json",
]


def get_sign_up_form_input():
    """Returns standard form input for sign up tests."""
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "@janedoe",
        "email": "janedoe@example.org",
        "new_password": "Password123",
        "password_confirmation": "Password123",
    }


def create_test_recipe(title, description, content, author):
    """Helper to create a test recipe with standard fields."""
    from recipes.models import Recipe

    return Recipe.objects.create(
        title=title, description=description, content=content, author=author
    )


def get_test_image_file(fixtures_relative_path="../fixtures", filename="burger.png"):
    """Load and return a SimpleUploadedFile for testing image uploads."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_dir = os.path.join(current_dir, fixtures_relative_path)
    image_path = os.path.join(fixtures_dir, filename)

    with open(image_path, "rb") as img_file:
        return SimpleUploadedFile(
            name=filename, content=img_file.read(), content_type="image/png"
        )


class LogInTester:
    """Class to support login in tests."""

    def _is_logged_in(self):
        """Returns True if a user is logged in.  False otherwise."""

        return "_auth_user_id" in self.client.session.keys()


class MenuTesterMixin(AssertHTMLMixin):
    """Class to extend tests with tools to check the presents of menu items."""

    menu_urls = [reverse("password"), reverse("profile"), reverse("log_out")]

    def assert_menu(self, response):
        """Check that menu is present."""

        for url in self.menu_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

    def assert_no_menu(self, response):
        """Check that no menu is present."""

        for url in self.menu_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')


class CommonTestMixin:
    """Mixin with common test helper methods."""

    def assert_unauthenticated_redirect(self, url, expected_redirect_code=302):
        """Assert that unauthenticated access redirects to login."""
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_redirect_code)

    def assert_405_on_get(self, url):
        """Assert that GET request returns 405 error."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")

    def assert_405_on_post(self, url):
        """Assert that POST request returns 405 error."""
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, "405_error.html")

    def assert_403_forbidden(self, url):
        """Assert that access returns 403 forbidden."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403_error.html")

    def assert_redirect_to_dashboard(self, response):
        """Assert that response redirects to dashboard."""
        response_url = reverse("dashboard")
        self.assertRedirects(
            response, response_url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, "dashboard.html")

    def assert_user_count_unchanged(self, before_count, after_count):
        """Assert that user count hasn't changed."""
        self.assertEqual(after_count, before_count)

    def assert_no_recipes_text(self, response):
        """Assert that 'no recipes' text is present."""
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="no-recipes-text"')

    def assert_has_recipes(self, response):
        """Assert that recipes are present (no 'no recipes' text)."""
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="no-recipes-text"')
