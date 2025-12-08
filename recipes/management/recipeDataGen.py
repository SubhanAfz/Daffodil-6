import ast

import pandas as pd
from faker import Faker
from random import randint


class recipeDataGen:
    fake = Faker()
    df = pd.read_csv("recipes/management/recipes_data_sample_1.csv")

    def __init__(self):
        # Convert string representations of lists back to actual lists
        self.df["ingredients"] = self.df["ingredients"].apply(
            lambda x: tuple(ast.literal_eval(x))
        )
        self.df["directions"] = self.df["directions"].apply(
            lambda x: tuple(ast.literal_eval(x))
        )
        self.index = 0

    @staticmethod
    def series_to_string(self, series):
        text = ""
        for item in series:
            text += str(item) + "\n"

        return text.strip()

    def get_next_recipe_data(self, user):
        if self.index >= len(self.df):
            self.index = 0  # Reset index if it exceeds dataframe length

        row = self.df.iloc[self.index]
        self.index += 1

        title = str(row["title"])
        ingredients = self.series_to_string(row["ingredients"])
        content = self.series_to_string(row["directions"])

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
        }
