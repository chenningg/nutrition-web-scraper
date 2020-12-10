from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import csv

# Load environment variables
load_dotenv()

# Load config
DRIVER_PATH = os.getenv("DRIVER_PATH")

# Open Edge driver and set various settings
options = EdgeOptions()
options.use_chromium = True
options.add_argument("headless")

driver = Edge(options=options, executable_path=DRIVER_PATH)

food_names = []

# Load in all food names to iterate through
with open("./data/food_names_hpb.txt", "r") as food_names_file:
    for food_name in food_names_file:
        food_names.append(food_name.rstrip())

# Open new file to write results to
with open("./results/foods/food_data_hpb.csv", "a", newline="") as food_desc_file:
    spamwriter = csv.writer(
        food_desc_file, delimiter="|", quotechar="\\", quoting=csv.QUOTE_MINIMAL
    )

    # Go to get the nutritional info of all food in a loop
    driver.get("https://focos.hpb.gov.sg/eservices/ENCF/foodsearch.aspx")

    # Write headers to csv
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

    for food_name in food_names:
        # Remove trailing newlines
        food_name = food_name.rstrip()

        try:
            search_food_name = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "txtFoodName"))
            )

            # Input food name
            search_food_name.clear()
            search_food_name.send_keys(food_name)

            # Search for the food
            driver.find_element_by_id("btnSearch").click()

            # Get serving size of food
            serving_size_element = driver.find_element_by_xpath(
                "//*[@id='gvData']/tbody/tr[2]/td[3]"
            )
            serving_size_raw = serving_size_element.get_attribute("innerText").split()[
                -1
            ]
            serving_size = serving_size_raw[1:-2]
            serving_size_unit = serving_size_raw[-2]

            # Select the first checkbox of the food
            driver.find_element_by_xpath("(//input[@type='checkbox'])[1]").click()

            # Click confirm to load nutrition
            driver.find_element_by_id("btnConfirm").click()

            # Get description of food if any
            description = ""
            if "Description:" in driver.page_source:
                description = driver.find_element_by_xpath(
                    "//*[@id='lblTable']/table/tbody/tr[2]/td[2]"
                ).get_attribute("innerText")
                if (
                    description == "nil"
                    or description == "Nil"
                    or description == "--"
                    or description == "-"
                    or description == "na"
                ):
                    description = ""

            # Create output
            output_row = [food_name, serving_size, serving_size_unit, description]

            # Get nutritional data of food
            nutrition_table = driver.find_elements_by_xpath(
                "((//*[@id='lblTable']/table/tbody/tr)[last()])/td/table/tbody/tr"
            )

            # Skip the first row (food name) loop and get all nutrients and their unit sizes
            for nutrient in nutrition_table[1:]:
                amount = (
                    nutrient.find_element_by_xpath(".//td[2]")
                    .get_attribute("innerText")
                    .split()
                )

                if len(amount) == 0 or amount[0] == "NA":
                    output_row.append("")
                    output_row.append("")
                else:
                    # Append nutrient amount and unit of nutrient separately
                    output_row.append(amount[0])
                    output_row.append(amount[1])

            spamwriter.writerow(output_row)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnBack"))
            ).click()

        # If we reach here, it means no results found for the food name search (e.g. 2pc chicken)
        except NoSuchElementException:
            continue

    driver.quit()
