import unittest

from Cocktail import CocktailRecipe
from tests.test_data import *

VALID_RECIPES_TUPLES = [
    (MOJITO_API_RESP, MOJITO_EXPECTED_STR),
    (TOM_COLLINS_API_RESP, TOM_COLLINS_EXPECTED_STR),
    (OLD_FASHIONED_API_RESP, OLD_FASHIONED_EXPECTED_STR)
]


class CocktailRecipeTest(unittest.TestCase):
    """
    Tests the basic functionality of the CocktailRecipe class.
    Note:
        It does not test the functionality of the CocktailDB
        API.
    Test strategy:
        - Ensure the expected string representation of the CocktailRecipe
        object matches the actual string representation:
            - Use instructions separated by sentences
            - Use instructions separated by line breaks.
    """

    def test_valid_cocktail(self):
        for api_resp, expected_str in VALID_RECIPES_TUPLES:
            cocktail_recipe = CocktailRecipe(api_resp)
            self.assertEqual(expected_str, str(cocktail_recipe),
                             "String representation is not equal to expected.")

    def test_get_name(self):
        mojito_recipe = CocktailRecipe(MOJITO_API_RESP)
        self.assertEqual("Mojito", mojito_recipe.get_name())

    def test_get_ingredients(self):
        mojito_recipe = CocktailRecipe(MOJITO_API_RESP)
        expected_ingredients = {
            "Light rum": "2-3 oz",
            "Lime": "Juice of 1",
            "Mint": '2-4',
            "Soda water": "To Taste",
            "Sugar": "2 tsp"
        }
        self.assertEqual(expected_ingredients, mojito_recipe.get_ingredients())

    def test_get_instructions(self):
        tom_collins_recipe = CocktailRecipe(TOM_COLLINS_API_RESP)
        expected_instructions = [
            "In a shaker half-filled with ice cubes, combine the gin, lemon juice, and sugar",
            "Shake well",
            "Strain into a collins glass almost filled with ice cubes",
            "Add the club soda",
            "Stir and garnish with the cherry and the orange slice."
        ]

        self.assertEqual(expected_instructions, tom_collins_recipe.get_instructions())

    def test_get_glass(self):
        old_fashioned_recipe = CocktailRecipe(OLD_FASHIONED_API_RESP)
        expected_glass = "Old-fashioned glass"
        self.assertEqual(expected_glass, old_fashioned_recipe.get_glass())

if __name__ == '__main__':
    unittest.main()
