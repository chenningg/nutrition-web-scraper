from recipe_scrapers import scrape_me


def scrape_ingredient(url):
    scraper = scrape_me(url)
    ingredients_list = scraper.ingredients()

    ingredients = []

    for ingredient in ingredients_list:
        ingredient_parts = ingredient.split(" ")
        if (ingredient_parts[0].isnumeric()):
            ingredient_parts = ingredient_parts[1:]
        ingredients.append(" ".join(ingredient_parts))

    return(ingredients)


print(scrape_ingredient(
    "https://www.allrecipes.com/recipe/70667/singapore-chicken-rice/"))
