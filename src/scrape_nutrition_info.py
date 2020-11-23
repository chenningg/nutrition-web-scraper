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

# Open Edge driver
options = EdgeOptions()
options.use_chromium = True

driver = Edge(options=options, executable_path=DRIVER_PATH)

food_names = []

with open("./data/food_names.txt", "r") as food_names_file:
    for food_name in food_names_file:
        food_names.append(food_name.rstrip())

with open("./data/food_data.csv", "a") as food_desc_file:
    spamwriter = csv.writer(food_desc_file, delimiter='|',
                            quotechar='\\', quoting=csv.QUOTE_MINIMAL)

    # Go to get the nutritional info of all food in a loop
    driver.get("https://focos.hpb.gov.sg/eservices/ENCF/foodsearch.aspx")

    # Write headers to csv
    spamwriter.writerow(["food_name", "description", "energy", "protein", "total_fat",
                         "saturated_fat", "dietary_fibre", "carbohydrate", "cholesterol", "sodium"])

    for food_name in food_names:
        # Remove trailing newlines
        food_name = food_name.rstrip()

        try:
            search_food_name = driver.find_element_by_id("txtFoodName")

            # Input food name
            search_food_name.clear()
            search_food_name.send_keys(food_name)

            # Search for the food
            driver.find_element_by_id("btnSearch").click()

            # Select the first checkbox of the food
            driver.find_element_by_xpath(
                "(//input[@type='checkbox'])[1]").click()

            # Click confirm to load nutrition
            driver.find_element_by_id("btnConfirm").click()

            # Get description of food if any
            description = ""
            if "Description:" in driver.page_source:
                description = driver.find_element_by_xpath(
                    "//*[@id='lblTable']/table/tbody/tr[2]/td[2]").get_attribute("innerText")
                if (description == "nil" or description == "--"):
                    description = ""

            # Create output
            output_row = [food_name, description]

            # Get nutritional data of food
            nutrition_table = driver.find_elements_by_xpath(
                "((//*[@id='lblTable']/table/tbody/tr)[last()])/td/table/tbody/tr")

            # Skip the first row (food name)
            for nutrient in nutrition_table[1:]:
                amount = nutrient.find_element_by_xpath(
                    ".//td[2]").get_attribute("innerText")
                output_row.append(amount)

            spamwriter.writerow(output_row)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnBack"))).click()

            # driver.find_element_by_id("btnBack").click()

        # If we reach here, it means no results found for the food name search (e.g. 2pc chicken)
        except NoSuchElementException:
            continue

    driver.quit()
