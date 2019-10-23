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
            self.assertEqual(expected_str, str(cocktail_recipe), "String representation is not equal to expected.")


if __name__ == '__main__':
    unittest.main()
