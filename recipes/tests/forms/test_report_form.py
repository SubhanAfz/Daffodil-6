"""Unit tests of the report form."""

from django import forms
from django.test import TestCase
from recipes.forms import ReportForm
from recipes.models import User, Recipe, Report


class ReportFormTestCase(TestCase):
    """Unit tests of the report form."""

    fixtures = [
        "recipes/tests/fixtures/default_user.json",
        "recipes/tests/fixtures/other_users.json",
        "recipes/tests/fixtures/recipes.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.recipe = Recipe.objects.get(pk=1)
        self.form_input = {"reason": "This recipe contains inappropriate content."}

    def test_form_contains_required_fields(self):
        form = ReportForm()
        self.assertIn("reason", form.fields)

    def test_form_uses_model_validation(self):
        form = ReportForm()
        self.assertEqual(form.Meta.model, Report)
        self.assertEqual(form.Meta.fields, ["reason"])

    def test_reason_field_uses_textarea_widget(self):
        form = ReportForm()
        reason_field = form.fields["reason"]
        self.assertTrue(isinstance(reason_field.widget, forms.Textarea))

    def test_reason_widget_has_correct_attributes(self):
        form = ReportForm()
        reason_widget = form.fields["reason"].widget
        self.assertEqual(reason_widget.attrs.get("class"), "form-control")
        self.assertEqual(reason_widget.attrs.get("rows"), 4)
        self.assertEqual(
            reason_widget.attrs.get("placeholder"), "Why are you reporting this recipe?"
        )

    def test_reason_field_has_correct_label(self):
        form = ReportForm()
        self.assertEqual(
            form.fields["reason"].label, "Why are you reporting this recipe?"
        )

    def test_form_accepts_valid_input(self):
        form = ReportForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_reason(self):
        self.form_input["reason"] = ""
        form = ReportForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_long_reason(self):
        self.form_input["reason"] = "x" * 1200
        form = ReportForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_reason_exceeding_max_length(self):
        self.form_input["reason"] = "x" * 1201
        form = ReportForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_strips_whitespace_from_reason(self):
        self.form_input["reason"] = "  Valid reason with spaces  "
        form = ReportForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        # Django's CharField strips leading/trailing whitespace by default
        self.assertEqual(form.cleaned_data["reason"], "Valid reason with spaces")

    def test_form_saves_correctly(self):
        form = ReportForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        report = form.save(commit=False)
        report.reporter = self.user
        report.recipe = self.recipe
        report.save()
        saved_report = Report.objects.get(reporter=self.user, recipe=self.recipe)
        self.assertEqual(saved_report.reason, self.form_input["reason"])
        self.assertEqual(saved_report.reporter, self.user)
        self.assertEqual(saved_report.recipe, self.recipe)
