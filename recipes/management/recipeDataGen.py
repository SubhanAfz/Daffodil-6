
import pandas as pd
from faker import Faker
from random import randint

class recipeDataGen:

    fake = Faker()
    df = pd.read_csv('recipes/management/recipes_data_sample_1.csv')
    index = 0

    def get_next_recipe_data(self, user):
        if self.index >= len(self.df):
            self.index = 0  # Reset index if it exceeds dataframe length

        row = self.df.iloc[self.index]
        self.index += 1

        title = str(row['title'])
        desc = str(row['ingredients'])
        content = str(row['directions'])

        return {
            "title": title,
            "description": desc,
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
    