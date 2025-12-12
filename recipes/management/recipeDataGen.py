# ruff: noqa: PLR6301
import ast
import os

import pandas as pd
from faker import Faker
from random import randint
from django.utils.text import slugify


class RecipeDataGenerator:
    """Generator class for creating recipe data from CSV file for database seeding."""

    fake = Faker()
    df = pd.read_csv("recipes/management/recipes_data_sample_1.csv")

    def __init__(self):
        # Check if this is the new format (with image_name column)
        self.has_image_name = "image_name" in self.df.columns

        # Handle ingredients column - may be string list or already parsed
        if "ingredients" in self.df.columns:
            self.df["ingredients"] = self.df["ingredients"].apply(
                self._parse_list_column
            )

        # instructions column
        if "directions" in self.df.columns:
            self.df["directions"] = self.df["directions"].apply(self._parse_list_column)

        self.index = 0

    def _parse_list_column(self, x):
        """Parse a column that might be a string representation of a list."""
        if isinstance(x, (list, tuple)):
            return tuple(x)
        if pd.isna(x):
            return tuple()
        try:
            return tuple(ast.literal_eval(str(x)))
        except (ValueError, SyntaxError):
            # If it's just a plain string, return it as a single-item tuple
            return (str(x),)

    def series_to_string(self, series):
        """Convert a tuple/list of items to a newline-separated string."""
        if isinstance(series, str):
            return series.strip()
        text = ""
        for item in series:
            text += str(item) + "\n"
        return text.strip()

    def _get_thumbnail_path(self, slug, image_name=None):
        """Get the thumbnail image path based on slug or image_name."""
        if (
            self.has_image_name
            and image_name
            and os.path.exists(f"recipes/management/sample_images/{image_name}")
        ):
            # new format: use direct image_name
            return f"recipes/management/sample_images/{image_name}"
        elif os.path.exists(f"recipes/management/sample_images/{slug}.jpg"):
            # old format: use slug to find image
            return f"recipes/management/sample_images/{slug}.jpg"
        return None

    def get_next_recipe_data(self, user):
        """Get the next recipe data dictionary from the CSV for the given user."""
        if self.index >= len(self.df):
            self.index = 0  # Reset index if it exceeds dataframe length

        row = self.df.iloc[self.index]
        self.index += 1

        title = str(row["title"])
        ingredients = self.series_to_string(row["ingredients"])
        content = self.series_to_string(row["directions"])

        # Try to find matching thumbnail image
        thumbnail_path = self._get_thumbnail_path(
            slugify(title), row.get("image_name") if self.has_image_name else None
        )

        return {
            "title": title,
            "description": title,
            "ingredients": ingredients,
            "content": content,
            "author": user,
            "created_at": self.fake.date_time_this_year(),
            "updated_at": self.fake.date_time_this_year(),
            "views": randint(0, 1000),
            "is_reported": False,
            "num_reports": 0,
            "is_hidden": False,
            "date_hidden": None,
            "thumbnail_path": thumbnail_path,
        }
