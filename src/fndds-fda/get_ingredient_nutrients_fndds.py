import csv
import os

dirname = os.path.dirname(__file__)
input_path = os.path.join(
    dirname, "../../data/fndds-fda/ingredient_nutrients_fndds.csv"
)
food_input_path = os.path.join(dirname, "../../data/fndds-fda/food_nutrients_fndds.csv")
output_path = os.path.join(
    dirname, "../../results/ingredients/ingredient_nutrients_fndds.csv"
)

with open(input_path, "r", newline="") as input_file:  # Input
    with open(food_input_path, "r", newline="") as food_input_file:
        with open(output_path, "a", newline="") as output_file:  # Output

            # Load in ingredient nutrients
            ingredient_reader = csv.reader(input_file, delimiter=",", quotechar='"')

            # Load in food for the headings
            food_reader = csv.reader(food_input_file, delimiter=",", quotechar='"')

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
            headers = [
                "ingredient_name",
                "serving_size",
                "serving_size_unit",
            ]

            nutrient_headers = []
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
                nutrients_dict[nutrient_name] = nutrient_unit

                # Add newly titled header without units to headers
                nutrient_headers.append(nutrient_name)

            # Write headers to output file after sorting
            nutrient_headers.sort()
            for nutrient_header in nutrient_headers:
                headers.append(nutrient_header)
                headers.append(nutrient_header + "_unit")

            writer.writerow(headers)

            # Each row may be the same ingredient but different nutrient
            last_food = ""
            output_dict = {}
            output = []

            # Skip first row of ingredients csv
            next(ingredient_reader, None)

            for row in ingredient_reader:
                ingredient_name = row[1]

                # If ingredient name doesn't match, write to output since we've moved on to the next ingredient
                if ingredient_name != last_food and last_food != "":
                    # Write to output in order
                    output.append(last_food)
                    output.append(100)
                    output.append("g")

                    for nutrient_header in nutrient_headers:
                        output.append(output_dict[nutrient_header])
                        output.append(nutrients_dict[nutrient_header])

                    writer.writerow(output)
                    output_dict.clear()
                    output = []

                # If ingredient name matches, continue adding nutrients to output
                last_food = ingredient_name

                # Add to output
                nutrient_amount = float(row[4])

                nutrient_name = ""

                for word in row[3].split():
                    nutrient_name += word.replace(",", "") + "_"
                nutrient_name = nutrient_name[:-1]
                nutrient_name = nutrient_name.replace("_+_", "+")
                nutrient_name = nutrient_name.lower()

                output_dict[nutrient_name] = nutrient_amount

            # Write last ingredient to output
            for nutrient_header in nutrient_headers:
                output.append(output_dict[nutrient_header])
                output.append(nutrients_dict[nutrient_header])

            writer.writerow(output)