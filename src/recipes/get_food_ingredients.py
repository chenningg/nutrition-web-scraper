import json
import csv

# Open JSON data file and load ingredients
with open("./data/recipes_raw_nosource_ar.json") as recipe_file:
    data = json.load(recipe_file)
    with open(
        "./results/recipes/recipe_ingredients_ar.csv", "a", newline=""
    ) as food_ingredients_file:  # Output

        spamwriter = csv.writer(
            food_ingredients_file,
            delimiter="|",
            quotechar="\\",
            quoting=csv.QUOTE_MINIMAL,
        )

        spamwriter.writerow(
            [
                "food_name",
                "serving_size",
                "serving_size_unit",
                "description",
                "energy",
                "energy_unit",
                "protein",
                "protein_unit",
                "total_fat",
                "total_fat_unit",
                "saturated_fat",
                "saturated_fat_unit",
                "dietary_fibre",
                "dietary_fibre_unit",
                "carbohydrate",
                "carbohydrate_unit",
                "cholesterol",
                "cholesterol_unit",
                "sodium",
                "sodium_unit",
            ]
        )

        # Ignore headers
        for row in food_data_reader:
            # Check if this is an ingredient
            food_name = row[0]

            # If ingredient, we write it to output
            if (
                ", raw" in food_name
                and "Sushi" not in food_name
                or "nuts," in food_name
            ):
                spamwriter.writerow(row)
