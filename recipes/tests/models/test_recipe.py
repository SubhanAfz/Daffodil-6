from django.forms import ValidationError
from django.test import TestCase
from recipes.models.recipe import Recipe

class RecipeModelTestCase(TestCase):
    """Unit tests for recipe model."""

    fixtures = [
        'recipes/tests/fixtures/recipes.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/reports.json'
    ]

    def setUp(self):
        self.recipe = Recipe.objects.get(id=6)

    def test_valid_recipe(self):
        self._assert_recipe_is_valid()

    def test_title_must_be_less_than_200_characters(self):
        """Test validity of title with 201 characters"""

        self.recipe.title="kchraecniymklfdptacdzlqufcftqsoshhylxumlllmqqwdlnwqjqbbrghbaxsigfcoarmouobvlquvpkutxsmmfrfuhordwzmjomxcwziumjoqwqzuhkhimphwdtdixuisclusaghqfwpgxttfwxbkyheglrxnrwdgdzzhgmrngthjozwywbyhbazhmsnmobqvuaqhbr"
        self._assert_recipe_is_invalid()

        """Test validity of title with 200 characters"""
        self.recipe.title="zreuzugjjiwksovvlhdwauqxcuvdomknpffsncvrkcxyafpndmxnsxqzaaapcrthteveypujovgabfhfqvxoiwgunqztruvivqnwbzqoohpcuxohpucgpkxibvxsnfzcgtevhuwclhexsovrvywabgmafpenidgcfmbzieebixlrjvprrmaoskvqulgaxikhzeztbgpe"
        self._assert_recipe_is_valid()

    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail('Test user should be valid')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
