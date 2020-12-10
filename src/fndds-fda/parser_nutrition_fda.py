import csv

# We want to store food_id|food_name|[nutrient_id, nutrient_amnt + nurient unit] (comma separated)
with open("./data/food_names_fda.csv", "r", newline="") as food_names_file:  # Input
    with open("./data/food_nutrients_fda.csv", "r", newline="") as food_nutrients_file:  # Input
        with open("./data/food_intermediate_fda.csv", "a", newline="") as food_intermediate_file:  # Output
            food_names_reader = csv.reader(
                food_names_file, delimiter=',', quotechar='"')
            food_nutrients_reader = csv.reader(
                food_names_file, delimiter=',', quotechar='"')
            spamwriter = csv.writer(
                food_intermediate_file, delimiter='|', quotechar='\\', quoting=csv.QUOTE_MINIMAL)

            output = []

            for row in food_names_reader:
                # Get details
                food_ID = row[0]
                food_name = row[2]

                # Write food ID and food name to output
                output.append(food_ID, food_name)

                # For each food ID, we need to find the corresponding nutrient ID and amounts as well.
