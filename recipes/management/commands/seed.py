"""
Management command to seed the database with demo data.

This command creates a small set of named fixture users and then fills up
to ``USER_COUNT`` total users using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""

from faker import Faker

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from recipes.models import User
from recipes.models import Recipe
from recipes.models.tag import Tag
from recipes.management.recipeDataGen import recipeDataGen


user_fixtures = [
    {
        "username": "@johndoe",
        "email": "john.doe@example.org",
        "first_name": "John",
        "last_name": "Doe",
        "is_superuser": True,
    },
    {
        "username": "@janedoe",
        "email": "jane.doe@example.org",
        "first_name": "Jane",
        "last_name": "Doe",
    },
    {
        "username": "@charlie",
        "email": "charlie.johnson@example.org",
        "first_name": "Charlie",
        "last_name": "Johnson",
    },
]

tag_fixtures = [
    "Chinese",
    "Italian",
    "Mexican",
    "Indian",
    "Mediterranean",
    "Spicy",
    "Vegan",
    "Gluten-Free",
    "Comfort Food",
    "BBQ",
]


class Command(BaseCommand):
    """
    Build automation command to seed the database with data.

    This command inserts a small set of known users (``user_fixtures``) and then
    repeatedly generates additional random users until ``USER_COUNT`` total users
    exist in the database. Each generated user receives the same default password.

    Attributes:
        USER_COUNT (int): Target total number of users in the database.
        DEFAULT_PASSWORD (str): Default password assigned to all created users.
        help (str): Short description shown in ``manage.py help``.
        faker (Faker): Locale-specific Faker instance used for random data.
    """

    USER_COUNT = 200
    RECIPES_PER_USER = 2
    SEEDED_RECIPE_COUNT = USER_COUNT * RECIPES_PER_USER

    DEFAULT_PASSWORD = "Password123"
    help = "Seeds the database with sample data"

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker("en_US")
        self.recipeDataGen = recipeDataGen()

    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores ``self.users`` for any
        post-processing or debugging (not required for operation).
        """

        self.create_users()
        # self.users = User.objects.all()
        self.assign_recipes_to_users()
        self.assign_tags_to_recipes()

    def assign_tags_to_recipes(self):
        """
        Assign predefined tags to recipes in the database.
        """
        # Create tag objects
        for tag_name in tag_fixtures:
            tag = Tag.objects.get_or_create(name=tag_name)

        tags = Tag.objects.all()

        # Assign tags to recipes
        recipes = Recipe.objects.all()
        for recipe in recipes:
            print("Adding tags to recipes...", end="\r")
            # For simplicity, assign 2 random tags to each recipe
            assigned_tags = self.faker.random_elements(
                elements=list(tags), length=2, unique=True
            )
            for tag in assigned_tags:
                tag.recipes.add(recipe)
                tag.save()
        print("Tag assignment complete.      ")

    def assign_recipes_to_users(self):
        """
        For each user in the database, assign RECIPES_PER_USER recipes.
        """
        users = User.objects.all()
        for user in users:
            for _ in range(self.RECIPES_PER_USER):
                recipe_count = Recipe.objects.count()
                print(
                    f"Seeding recipes {recipe_count}/{self.SEEDED_RECIPE_COUNT}",
                    end="\r",
                )

                recipe_data = self.recipeDataGen.get_next_recipe_data(user)
                self.try_create_recipe(recipe_data)
        print("Seeding recipes complete.      ")

    def try_create_recipe(self, data):
        """
        Attempt to create a recipe and ignore any errors.

        Args:
            data (dict): Mapping with recipe data | ``title``, ``description``,
            ``content``, ``author``, ``created_at``, ``updated_at``, ``views`` |.
        """
        try:
            self.create_recipe(data)
        except IntegrityError:
            pass

    def create_recipe(self, data):
        """
        Create a recipe with the given data.
        Args:
            data (dict): Mapping with recipe data | ``title``, ``description``,
            ``content``, ``author``, ``created_at``, ``updated_at``, ``views`` |.
        """

        Recipe.objects.create(
            title=data["title"],
            description=data["description"],
            ingredients=data["ingredients"],
            content=data["content"],
            author=data["author"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            views=data["views"],
            is_reported=data["is_reported"],
            num_reports=data["num_reports"],
            is_hidden=data["is_hidden"],
            date_hidden=data["date_hidden"],
        )

    def create_users(self):
        """
        Create fixture users and then generate random users up to USER_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on username/email) are ignored and generation continues.
        """
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        """Attempt to create each predefined fixture user."""
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        """
        Generate random users until the database contains USER_COUNT users.

        Prints a simple progress indicator to stdout during generation.
        """
        user_count = User.objects.count()
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end="\r")
            self.generate_user()
            user_count += 1
        print("User seeding complete.      ")

    def generate_user(self):
        """
        Generate a single random user and attempt to insert it.

        Uses Faker for first/last names, then derives a simple username/email.
        """
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user(
            {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

    def try_create_user(self, data):
        """
        Attempt to create a user and ignore any errors.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        try:
            self.create_user(data)
        except IntegrityError:
            pass

    def create_user(self, data: dict):
        """
        Create a user with the default password.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        if data.get("is_superuser", False):
            User.objects.create_superuser(
                username=data["username"],
                email=data["email"],
                password=Command.DEFAULT_PASSWORD,
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
        else:
            User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=Command.DEFAULT_PASSWORD,
                first_name=data["first_name"],
                last_name=data["last_name"],
            )


def create_username(first_name, last_name):
    """
    Construct a simple username from first and last names.

    Args:
        first_name (str): Given name.
        last_name (str): Family name.

    Returns:
        str: A username in the form ``@{firstname}{lastname}`` (lowercased).
    """
    return "@" + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    """
    Construct a simple example email address.

    Args:
        first_name (str): Given name.
        last_name (str): Family name.

    Returns:
        str: An email in the form ``{firstname}.{lastname}@example.org``.
    """
    return first_name + "." + last_name + "@example.org"
