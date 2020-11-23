from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load config
DRIVER_PATH = os.getenv("DRIVER_PATH")

print(os.listdir())

# Write food names to file
with open("./data/food_names.txt", "a") as food_names_file:
    # Open Edge driver
    options = EdgeOptions()
    options.use_chromium = True

    driver = Edge(options=options, executable_path=DRIVER_PATH)

    # Get all food names available in HPB database
    driver.get("https://focos.hpb.gov.sg/eservices/NIP/Add_ProductOIA.aspx")

    element = driver.find_element_by_id("ddlFoodIngredient")
    food_elements = element.find_elements_by_tag_name("option")

    for food in food_elements:
        food_names_file.write(food.get_attribute("innerText") + '\n')

    driver.quit()
