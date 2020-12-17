from recipe_scrapers import scrape_me
import os
import csv

dirname = os.path.dirname(__file__)

input_path = os.path.join(dirname, "../../data/fndds-fda/food_ingredients_fndds.csv")

output_path = os.path.join(dirname, "../../results/recipes/recipes_fndds.csv")

with open(input_path, "r", newline="") as input_file:  # Input
    with open(output_path, "a", newline="") as output_file:  # Output
        reader = csv.reader(input_file, delimiter=",", quotechar='"')
        next(reader, None)

        writer = csv.writer(
            output_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )

        recipe_headers = [
            "recipe_name",
            "recipe_category",
            "servings",
            "serving_size",
            "serving_size_unit",
            "ingredient_name",
            "ingredient_amount",
            "ingredient_unit",
        ]

        # Output
        writer.writerow(recipe_headers)

        # Check if we have this food name
        recipes = {}

        # Write each recipe to file and the corresponding ingredients
        last_name = ""
        for row in reader:
            # If we don't have this recipe, don't write first, add to dict to add the values up
            if recipes.get(row[1]) == None:
                # Write previous recipe to disk
                if last_name != "":
                    total_serving_size = 0
                    # Add ingredient amount to find total dish serving size
                    for recipe in recipes[last_name]:
                        total_serving_size += recipe[6]
                    # Update recipe rows to reflect serving size of dish
                    for recipe in recipes[last_name]:
                        recipe[3] = total_serving_size
                        writer.writerow(recipe)

                # Write new recipe row to disk
                recipe_name = row[1]
                recipe_category = row[3]
                servings = 1
                serving_size = 0
                serving_size_unit = "g"
                ingredient_name = row[6]
                ingredient_amount = float(row[7])
                ingredient_unit = "g"

                recipes[recipe_name] = [
                    [
                        recipe_name,
                        recipe_category,
                        servings,
                        serving_size,
                        serving_size_unit,
                        ingredient_name,
                        ingredient_amount,
                        ingredient_unit,
                    ]
                ]

                # Update last name
                last_name = recipe_name

            # Else we are still on current recipe, just different ingredient. Append it to list.
            else:
                # Write new recipe row to disk
                recipe_name = row[1]
                recipe_category = row[3]
                servings = 1
                serving_size = 0
                serving_size_unit = "g"
                ingredient_name = row[6]
                ingredient_amount = float(row[7])
                ingredient_unit = "g"

                recipes[recipe_name].append(
                    [
                        recipe_name,
                        recipe_category,
                        servings,
                        serving_size,
                        serving_size_unit,
                        ingredient_name,
                        ingredient_amount,
                        ingredient_unit,
                    ]
                )

        # Write last recipe to disk
        if last_name != "":
            total_serving_size = 0
            # Add ingredient amount to find total dish serving size
            for recipe in recipes[last_name]:
                total_serving_size += recipe[6]
            # Update recipe rows to reflect serving size of dish
            for recipe in recipes[last_name]:
                recipe[3] = total_serving_size
                writer.writerow(recipe)