import json

import requests

from cocktail import CocktailRecipe

EMPTY_DRINK_REQUEST = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
SEARCH_BY_INGREDIENT_REQUEST = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="


def get_drink_by_name(name: str) -> CocktailRecipe:
    """
    Searches for a given cocktail_recipe in the CocktailDB API
    and returns the recipe for the closest match to the
    desired cocktail_recipe.
    Note:
    Does not guarantee the drink desired will have the same name
    as the drink returned.
    :param name: Cocktail to find a recipe for.
    :raises ValueError: Raised if no drink could be found with the provided name.
    :return: A CocktailRecipe object for the closest match to the desired drink.
    """
    api_request = "".join([EMPTY_DRINK_REQUEST, name])
    response = requests.get(api_request)
    data = json.loads(response.content)
    if data.get("drinks") is None:
        raise ValueError("Could not find a drink with name {}".format(name))
    closest_match = data.get("drinks")[0]
    return CocktailRecipe(closest_match)


def get_drinks_based_on_ingredient(ingredient: str, limit: int = 1):
    """
    :param ingredient: Ingredient which the drink should contain
    :param limit: The maximum number of drinks to retrieve
    :return: n number of drinks with the given ingredient
    """
    api_request = "".join([SEARCH_BY_INGREDIENT_REQUEST, ingredient])
    response = requests.get(api_request)
    if len(response.content) == 0:
        raise ValueError("Could not find a drink with the ingredient {}".format(ingredient))
    data = json.loads(response.content)
    if data.get("drinks") is None:
        raise ValueError("Could not find a drink with the ingredient {}".format(ingredient))
    print(data.get("drinks"))
    drink_names = list(data.get("drinks")[i]["strDrink"] for i in range(min(limit, len(data.get("drinks")))))
    return list(get_drink_by_name(drink_name) for drink_name in drink_names)


if __name__ == "__main__":
    main_ingredient = input("What ingredient would you like your drink to have?\n")
    n = int(input("How many?\n"))
    for drink in get_drinks_based_on_ingredient(main_ingredient, n):
        print(drink)
