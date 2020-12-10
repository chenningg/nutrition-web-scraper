import csv

# Extract ingredients by searching for ", raw" regex
with open(
    "./results/foods/food_data_hpb.csv", "r", newline=""
) as food_data_file:  # Input
    with open(
        "./results/ingredients/ingredient_data_hpb.csv", "a", newline=""
    ) as food_ingredient_file:  # Output
        food_data_reader = csv.reader(food_data_file, delimiter="|", quotechar="\\")

        # Skip the headers row
        next(food_data_reader, None)

        spamwriter = csv.writer(
            food_ingredient_file,
            delimiter="|",
            quotechar="\\",
            quoting=csv.QUOTE_MINIMAL,
        )

        spamwriter.writerow(
            [
                "ingredient_name",
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
