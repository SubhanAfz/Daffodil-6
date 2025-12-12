from django.test import TestCase, override_settings
from django.conf import settings
from django.conf.urls.static import static
from recipify import urls
from importlib import reload


class UrlsTestCase(TestCase):
    """Tests for URL configuration."""

    def test_static_and_media_urls_added_when_not_production(self):
        """Test that static and media URL patterns are added when PRODUCTION is False."""
        with override_settings(PRODUCTION=False):
            reload(urls)

            static_patterns = static(
                settings.STATIC_URL, document_root=settings.STATIC_ROOT
            )
            media_patterns = static(
                settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
            )

            # Check if static patterns are in urlpatterns
            for pattern in static_patterns:
                self.assertIn(pattern, urls.urlpatterns)

            # Check if media patterns are in urlpatterns
            for pattern in media_patterns:
                self.assertIn(pattern, urls.urlpatterns)

    def test_static_and_media_urls_not_added_when_production(self):
        """Test that static and media URL patterns are not added when PRODUCTION is True."""
        with override_settings(PRODUCTION=True):
            reload(urls)
            static_patterns = static(
                settings.STATIC_URL, document_root=settings.STATIC_ROOT
            )
            media_patterns = static(
                settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
            )

            # Check that static patterns are not in urlpatterns
            for pattern in static_patterns:
                self.assertNotIn(pattern, urls.urlpatterns)

            # Check that media patterns are not in urlpatterns
            for pattern in media_patterns:
                self.assertNotIn(pattern, urls.urlpatterns)
