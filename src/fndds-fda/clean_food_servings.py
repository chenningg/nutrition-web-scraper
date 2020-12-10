import csv
import os

dirname = os.path.dirname(__file__)
input_path = os.path.join(dirname, "../../data/fndds-fda/food_servings_fndds.csv")
output_path = os.path.join(
    dirname, "../../data/fndds-fda/cleaned_food_servings_fndds.csv"
)

# Get food portions for various types of food
with open(input_path, "r", newline="") as input_file:  # Input
    with open(output_path, "a", newline="") as output_file:  # Output

        reader = csv.reader(input_file, delimiter=",", quotechar='"')

        # Skip the headers rows
        next(reader, None)
        next(reader, None)

        writer = csv.writer(
            output_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )

        writer.writerow(
            [
                "food_name",
                "serving_desc",
                "serving_size",
                "serving_size_unit",
            ]
        )

        for row in reader:
            food_name = row[1]
            serving_desc = row[7]
            serving_size = row[8]
            serving_size_unit = "g"

            # If portion is specified, add it
            if serving_desc != "Quantity not specified":
                writer.writerow(
                    [food_name, serving_desc, serving_size, serving_size_unit]
                )
