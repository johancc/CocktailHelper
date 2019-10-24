import json

import requests

from cocktail import CocktailRecipe

EMPTY_DRINK_REQUEST = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="


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
    req = requests.get(api_request)
    data = json.loads(req.content)
    if data.get("drinks") is not None:
        closest_match = data.get("drinks")[0]
        return CocktailRecipe(closest_match)
    raise ValueError("Could not find a drink with name {}".format(name))


if __name__ == "__main__":
    drink_name = input("What drink would you like to make?\n")
    print(get_drink_by_name(drink_name))
