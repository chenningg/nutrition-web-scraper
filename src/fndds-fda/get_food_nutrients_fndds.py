import csv
import os

dirname = os.path.dirname(__file__)
input_path = os.path.join(dirname, "../../data/fndds-fda/food_nutrients_fndds.csv")
servings_input_path = os.path.join(
    dirname, "../../data/fndds-fda/cleaned_food_servings_fndds.csv"
)
output_path = os.path.join(dirname, "../../results/foods/food_nutrients_fnddsv2.csv")

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

            # Sort nutrient headers
            nutrient_headers.sort()
            for nutrient_header in nutrient_headers:
                headers.append(nutrient_header)
                headers.append(nutrient_header + "_unit")

            # Write headers to output file
            writer.writerow(headers)

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

                    output_dict = {}

                    # Calculate variables for nutrients
                    for i in range(4, len(row)):
                        # Calculate nutrient amount based on serving size (original nutrient amount is per 100g)
                        nutrient_amount = (float(row[i]) / 100) * float(
                            servings[serving_index]["serving_size"]
                        )

                        # Store to dictionary output
                        nutrient_name = ""
                        for word in file_headers[i - 4].split()[:-1]:
                            nutrient_name += word.replace(",", "") + "_"
                        nutrient_name = nutrient_name[:-1]
                        nutrient_name = nutrient_name.replace("_+_", "+")
                        nutrient_name = nutrient_name.lower()

                        output_dict[nutrient_name] = nutrient_amount

                    # Add to output
                    for nutrient_header in nutrient_headers:
                        output.append(output_dict[nutrient_header])
                        output.append(nutrients_dict[nutrient_header])

                    # Increment serving index to get the next serving
                    serving_index += 1

                    # Write to output file
                    writer.writerow(output)