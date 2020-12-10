from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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
# options.add_argument("headless")

driver = Edge(options=options, executable_path=DRIVER_PATH)

# Open new file to write results to
with open(
    "./results/foods/food_categories_hpb.csv", "a", newline=""
) as food_categories_file:
    spamwriter = csv.writer(
        food_categories_file, delimiter="|", quotechar="\\", quoting=csv.QUOTE_MINIMAL
    )

    # Go to get the nutritional info of all food in a loop
    driver.get("https://focos.hpb.gov.sg/eservices/ENCF/")

    # Write headers to csv
    spamwriter.writerow(["food_name", "food_category", "food_sub_category"])

    # Get main food categories
    food_categories_options = [
        "BEVERAGES",
        "CEREAL AND CEREAL PRODUCTS",
        "EGG AND EGG PRODUCTS",
        "FAST FOODS",
        "FISH AND FISH PRODUCTS",
        "FRUIT AND FRUIT PRODUCTS",
        "MEAT AND MEAT PRODUCTS",
        "MILK AND MILK PRODUCTS",
        "MISCELLANEOUS",
        "MIXED ETHNIC DISHES, ANALYZED IN SINGAPORE",
        "NUTS AND SEEDS, PULSES AND PRODUCTS",
        "OILS AND FATS",
        "OTHER MIXED ETHNIC DISHES",
        "SUGARS, SWEETS AND CONFECTIONERY",
        "VEGETABLE AND VEGETABLE PRODUCTS",
    ]

    # Get all foods in each category and their sub categories
    for food_category_option in food_categories_options:
        try:
            select_food_category = Select(
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "ddlFoodGroup"))
                )
            )

            # Input food category
            select_food_category.select_by_visible_text(food_category_option)

            # Wait a while for lag
            driver.implicitly_wait(1)

            # Search for the food
            driver.find_element_by_id("btnSearch").click()

            # Wait till results seclector is loaded
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "Pagination1_ddLimit"))
            )

            # Make sure to show all results
            show_results_selector = Select(
                driver.find_element_by_id("Pagination1_ddLimit")
            )
            show_results_selector.select_by_visible_text("All")

            # Wait till data is loaded
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "gvData"))
            )

            # Get results of all rows
            food_table = driver.find_elements_by_xpath("//*[@id='gvData']/tbody/tr")

            # Skip the first row (headers) and loop and get categories of each food
            for food in food_table[1:]:
                food_name = food.find_element_by_xpath(".//td[2]").get_attribute(
                    "innerText"
                )

                food_category = food.find_element_by_xpath(".//td[3]").get_attribute(
                    "innerText"
                )

                food_sub_category = food.find_element_by_xpath(
                    ".//td[4]"
                ).get_attribute("innerText")

                # Write to file
                output_row = [food_name, food_category, food_sub_category]
                spamwriter.writerow(output_row)

        # If we reach here, it means no results found for the food name search (e.g. 2pc chicken)
        except NoSuchElementException:
            continue

driver.quit()
