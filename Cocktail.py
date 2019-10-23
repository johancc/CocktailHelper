"""
Finds the recipe for a particular cocktail and provides a simple class to
show instructions, ingredients, and materials needed. It is able to find a
drink based on the name or the ingredients that you have. Uses the
CocktailDB API as a backend.
Note:
    This module is a wrapper on the CocktailDB API, any change in the API
    will break the wrapper.
"""
from typing import List, Dict


class CocktailRecipe:

    def __init__(self, cocktail_db_api_response: dict):
        """
        Represents the recipe for a cocktail, including instructions, ingredients,
        materials needed, and portions.
        based on the api response of CocktailDB
        :param cocktail_db_api_response: Response from the CocktailDB API detailing
        how to make a given cocktail.
        :raises ValueError: Raised if the provided dictionary does not have the
        expected keys: strDrink, strGlass, strIngredient+{number}, strMeasure + {number}
        """
        if not self.check_requirements(cocktail_db_api_response):
            raise ValueError("Provided api response is malformed.")
        self.name = cocktail_db_api_response.get("strDrink")
        self.glass = cocktail_db_api_response.get("strGlass")
        self.ingredients = self._parse_ingredients(cocktail_db_api_response)
        if self._uses_line_breaks(cocktail_db_api_response.get("strInstructions")):
            self.instructions = list(
                instruction for instruction in cocktail_db_api_response.get("strInstructions").split("\r\n")
                if len(instruction) is not 0)
        else:
            self.instructions = cocktail_db_api_response.get("strInstructions").split(". ")

    @staticmethod
    def check_requirements(cocktail_db_api_response: dict) -> bool:
        """
        Checks that a given api response is a valid cocktail recipe.
        :param cocktail_db_api_response: Response from the CocktailDB API detailing
        how to make a given cocktail.
        :return: True if the provided dictionary does has the  expected keys:
        strDrink, strGlass, strInstructions, strIngredient+{number}, strMeasure + {number}
        """
        required_keys = {"strGlass", "strDrink", "strInstructions"}
        required_keys.union({"strMeasure" + str(n) for n in range(1, 16)})
        required_keys.union({"strIngredient" + str(n) for n in range(1, 16)})
        return all([required_key in cocktail_db_api_response for required_key in required_keys])

    @staticmethod
    def _parse_ingredients(cocktail_db_api_response):
        ingredients = {}

        for ingredient_num in range(1, 16):  # The API is restricted to up to 16 ingredients max
            ingredient_key = "strIngredient%s" % str(ingredient_num)
            amount_key = "strMeasure%s" % str(ingredient_num)
            ingredient = cocktail_db_api_response.get(ingredient_key)
            amount = cocktail_db_api_response.get(amount_key)
            if ingredient is not None:
                if amount is None:
                    amount = "To Taste"
                ingredients[ingredient] = amount.strip()

        return ingredients

    def get_instructions(self) -> List[str]:
        return self.instructions

    def get_glass(self) -> str:
        return self.glass

    def get_ingredients(self) -> Dict:
        return self.ingredients

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        name_str = f"Name: {self.name}\n"
        ingredient_str = f"Ingredients:\n"
        for ingredient, amount in self.ingredients.items():
            ingredient_str += f"- {str(ingredient)} : {str(amount)}\n"
        instructions_str = "Instructions:\n"
        for i, instruction in enumerate(self.instructions):
            instructions_str += str(i + 1) + f") {instruction}\n"

        return "".join([name_str, ingredient_str, instructions_str])

    @staticmethod
    def _uses_line_breaks(instructions: str) -> bool:
        """
        Some instructions returned by the API use line breaks to denote the next
        step while others use a one sentence per instruction approach. This helper
        function helps differentiate between the two.
        :param instructions: The instructions retrieved from the CocktailDB API
        :return: whether the instructions are separated by line breaks or not.
        """
        return "\r\n" in instructions
