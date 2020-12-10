import csv
import os

dirname = os.path.dirname(__file__)
input_path = os.path.join(dirname, "../../data/fndds-fda/food_nutrients_fndds.csv")
servings_input_path = os.path.join(
    dirname, "../../data/fndds-fda/cleaned_food_servings_fndds.csv"
)
output_path = os.path.join(dirname, "../../results/foods/food_nutrients_fndds.csv")

with open(input_path, "r", newline="") as input_file:  # Input
    with open(servings_input_path, "r", newline="") as servings_input_file:
        with open(output_path, "a", newline="") as output_file:  # Output

            # Load in food nutrients
            food_reader = csv.reader(input_file, delimiter=",", quotechar='"')

            # Load in servings so that it's iterable by row index
            servings_reader = csv.DictReader(servings_input_file)
            servings = [serving for serving in servings_reader]

            writer = csv.writer(
                output_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            # Get the headers row
            file_headers = next(food_reader)[4:]

            # Load nutrient names and units and make new headers
            nutrients_dict = {}

            # Get newly titled headers
            headers = ["food_name", "serving_desc", "serving_size", "serving_size_unit"]

            for file_header in file_headers:
                file_header_split = file_header.split()

                nutrient_name = ""
                for word in file_header_split[:-1]:
                    nutrient_name += word.replace(",", "") + "_"
                nutrient_name = nutrient_name[:-1]
                nutrient_name = nutrient_name.replace("_+_", "+")
                nutrient_name = nutrient_name.lower()

                nutrient_unit = file_header_split[-1][1:-1]

                # Add unit to dictionary
                nutrients_dict[file_header] = nutrient_unit

                # Add newly titled header without units to headers
                headers.append(nutrient_name)
                headers.append(nutrient_name + "_unit")

            # Write headers to output file
            writer.writerow(headers)

            # headers = [
            #     "food_name",
            #     "serving_desc",
            #     "serving_size",
            #     "serving_size_unit",
            #     "energy",
            #     "energy_unit",
            #     "protein",
            #     "protein_unit",
            #     "carbohydrate",
            #     "carbohydrate_unit",
            #     "sugars",
            #     "sugars_unit",
            #     "dietary_fiber",
            #     "dietary_fiber_unit",
            #     "total_fat",
            #     "total_fat_unit",
            #     "saturated_fat",
            #     "saturated_fat_unit",
            #     "monounsaturated_fat",
            #     "monounsaturated_fat_unit",
            #     "polyunsaturated_fat",
            #     "polyunsaturated_fat_unit",
            #     "cholesterol",
            #     "cholesterol_unit",
            #     "retinol",
            #     "retinol_unit",
            #     "vitamin_a",
            #     "vitamin_a_unit",
            #     "carotene_alpha",
            #     "carotene_alpha_unit",
            #     "carotene_beta",
            #     "carotene_beta_unit",
            #     "cryptoxanthin_beta",
            #     "cryptoxanthin_beta_unit",
            #     "lycopene",
            #     "lycopene_unit",
            #     "lutein_zeaxanthin",
            #     "lutein_zeaxanthin_unit",
            #     "thiamin",
            #     "thiamin_unit",
            #     "riboflavin",
            #     "riboflavin_unit",
            #     "niacin",
            #     "niacin_unit",
            #     "vitamin_b6",
            #     "vitamin_b6_unit",
            #     "folic_acid",
            #     "folic_acid_unit",
            #     "folate",
            #     "folate_unit",
            #     "choline",
            #     "choline_unit",
            #     "vitamin_b12",
            #     "vitamin_b12_unit",
            #     "vitamin_c",
            #     "vitamin_c_unit",
            #     "vitamin_d",
            #     "vitamin_d_unit",
            #     "vitamin_e",
            #     "vitamin_e_unit",
            #     "vitamin_k",
            #     "vitamin_k_unit",
            #     "calcium",
            #     "calcium_unit",
            #     "phosphorus",
            #     "phosphorus_unit",
            #     "magnesium",
            #     "magnesium_unit",
            #     "iron",
            #     "iron_unit",
            #     "zinc",
            #     "zinc_unit",
            #     "copper",
            #     "copper_unit",
            #     "selenium",
            #     "selenium_unit",
            #     "potassium",
            #     "potassium_unit",
            #     "sodium",
            #     "sodium_unit",
            #     "caffeine",
            #     "caffeine_unit",
            #     "theobromine",
            #     "theobromine_unit",
            #     "alcohol",
            #     "alcohol_unit",
            #     "4:0",
            #     "4:0_unit",
            #     "6:0",
            #     "6:0_unit",
            #     "8:0",
            #     "8:0_unit",
            #     "10:0",
            #     "10:0_unit",
            #     "12:0",
            #     "12:0_unit",
            #     "14:0",
            #     "14:0_unit",
            #     "16:0",
            #     "16:0_unit",
            #     "18:0",
            #     "18:0_unit",
            #     "16:1",
            #     "16:1_unit",
            #     "18:1",
            #     "18:1_unit",
            #     "20:1",
            #     "20:1_unit",
            #     "22:1",
            #     "22:1_unit",
            #     "18:2",
            #     "18:2_unit",
            #     "18:3",
            #     "18:3_unit",
            #     "18:4",
            #     "18:4_unit",
            #     "20:4",
            #     "20:4_unit",
            #     "20:5_n-3",
            #     "20:5_n-3_unit",
            #     "22:5_n-3",
            #     "22:5_n-3_unit",
            #     "22:6_n-3",
            #     "22:6_n-3_unit",
            #     "water",
            #     "water_unit",
            # ]

            # Record which index we are at so we can just read that index for each food in the nutrients list
            serving_index = 0

            for row in food_reader:
                # Get all servings that match the current food name and write a new entry for each one
                food_name = row[1]

                while (
                    serving_index < len(servings)
                    and food_name == servings[serving_index]["food_name"]
                ):
                    # Create output row
                    output = [food_name]

                    # Set variables for writing
                    output.append(servings[serving_index]["serving_desc"])
                    output.append(servings[serving_index]["serving_size"])
                    output.append(servings[serving_index]["serving_size_unit"])

                    # Calculate variables for nutrients
                    for i in range(4, len(row)):
                        # Calculate nutrient amount based on serving size (original nutrient amount is per 100g)
                        nutrient_amount = (float(row[i]) / 100) * float(
                            servings[serving_index]["serving_size"]
                        )

                        # Get nutrient unit
                        nutrient_unit = nutrients_dict[file_headers[i - 4]]

                        # Add to output
                        output.append(nutrient_amount)
                        output.append(nutrient_unit)

                    # Increment serving index to get the next serving
                    serving_index += 1

                    # Write to output file
                    writer.writerow(output)