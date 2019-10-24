"""
Script utility which creates two sheets inside a google sheets file.
One of the sheets contains cocktail instructions, another
contains the ingredients necessary for the the set of cocktails
requested, and another contains a mapping from an ingredient to drink name.
Note:
    You need create a Google API project with Google Sheets integration,
    the service must credentials must be saved under a file called credentials.json
    You must make a google sheet and share the sheet with the service email
    in the credentials json file.
"""
from time import sleep
from typing import Union

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from cocktail import CocktailRecipe
from drink_lookup import get_drink_by_name, get_drinks_based_on_ingredient

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)


def write_cocktail_instructions_return_next_row(
        cocktail_recipe: CocktailRecipe,
        ws: gspread.Worksheet = None,
        row: int = None) -> int:
    """
    Writes a cocktail_recipe recipe into a google sheet worksheet.
    Format:
        0, 0, 0,
        Cocktail name,
        Instruction 1,
        ...,
        Instruction limit
    The cocktail has a separator line after the previous entry in the
    worksheet, unless the worksheet is empty.
    :param ws: The worksheet where to write the cocktail_recipe to
    :param cocktail_recipe: The cocktail_recipe recipe to write
    :param row: the row the entries should populate from
    :return: The next empty row below the instructions for this cocktail.
    """
    current_row = write_cocktail_header_return_next_row(cocktail_recipe, ws, row)
    for instruction in cocktail_recipe.get_instructions():
        ws.update_cell(current_row, 2, instruction)
        current_row += 1
    return current_row


def write_cocktail_header_return_next_row(cocktail_recipe: CocktailRecipe, ws: gspread.Worksheet, row: int = None):
    """
    Writes a separator line and drink name into the spreadsheet at the next available row
    :param cocktail_recipe: Recipe to which to write the header for.
    :param ws: Worksheet that should be written to.
    :param row: Row which to write the header into.
    :return: The rwo below the cocktail header
    """
    top_margin_row = 3
    current_row = row
    if row is None:
        current_row = find_next_empty_row_index(ws)
    if current_row >= top_margin_row:
        write_separator_line(ws, current_row, width=3, separator="0")
        current_row += 1
    ws.update_cell(current_row, 1, cocktail_recipe.get_name())
    current_row += 1
    return current_row


def write_ingredient_header_return_next_row(ingredient: str, ws: gspread.Worksheet, row: int = None):
    """
    Writes a separator line and ingredient name into the spreadsheet at the next available row.
    If no row is given, it finds the next empty row in the worksheet.
    :param ingredient: The ingredient of the drinks
    :param ws: Worksheet that should be written to.
    :param row: Row which to write the header to.
    :return: The row below the ingredient header.
    """
    top_margin_row = 3
    current_row = row
    if current_row is None:
        current_row = find_next_empty_row_index(ws)
    if current_row >= top_margin_row:
        write_separator_line(ws, current_row, width=2, separator="0")
        current_row += 1
    ws.update_cell(current_row, 1, ingredient)
    current_row += 1
    return current_row


def write_cocktail_ingredients_into_spreadsheet_return_next_row(cocktail_recipe: CocktailRecipe, ws: gspread.Worksheet,
                                                                next_empty_row=None) -> int:
    """
    Inserts the cocktail_recipe recipe into the bottom of the spreadsheet.
    The first entry in the row is the
    :param cocktail_recipe: The cocktail_recipe recipe to insert into the spreadsheet.
    :param ws: The worksheet to insert the cocktail_recipe to
    :param next_empty_row: If known, the next empty row where to write the ingredients to.
    :return The next empty row below the current row.
    """
    current_row = write_cocktail_header_return_next_row(cocktail_recipe, ws, next_empty_row)
    for ingredient, amount in cocktail_recipe.get_ingredients().items():
        ws.update_cell(current_row, 2, ingredient)
        ws.update_cell(current_row, 3, amount)
        current_row += 1
    return current_row


def write_cocktail_names_based_on_ingredient_return_next_row(ingredient: str, ws: gspread.Worksheet,
                                                             next_empty_row=None, limit: int = 1) -> int:
    """
    :param ingredient: The main ingredient of the drinks whose name to write.
    :param ws: The worksheet to insert the drink name to
    :param next_empty_row: If known, the next empty row where to write the drink names to.
    :param limit: The maximum number of drink names to write for the given ingredient.
    :return: The next empty row below where the drink names were written.
    """
    current_row = write_ingredient_header_return_next_row(ingredient, ws, next_empty_row)
    for cocktail in get_drinks_based_on_ingredient(ingredient, limit):
        ws.update_cell(current_row, 2, cocktail.get_name())
        current_row += 1
    return current_row


def write_separator_line(ws: gspread.Worksheet, separator_row_index: int, width: int,
                         separator: Union[str, int]) -> None:
    """
    Writes a separator line to mark the start of a new entry.
    :param ws: Worksheet to write the line to
    :param separator_row_index: index of the row to write the line in
    :param width: How many cells should be written to in the given row
    :param separator: The value which to fills the cells with
    :return: None
    """
    for col in range(1, width + 1):
        ws.update_cell(separator_row_index, col, separator)


def find_next_empty_row_index(
        ws: gspread.Worksheet,
        empty_rows_below: int = 1,
        min_horizontal_empty_cells: int = 3,
        start_index: int = 1) -> int:
    """
    Finds the next empty row index in a worksheet. It also ensures that there
    are at least empty_rows_below rows below the row which are empty.
    :param ws: The worksheet to look for an empty row in
    :param empty_rows_below: The number of rows below the returned row that should be empty
    :param min_horizontal_empty_cells: Minimum number of empty continuous cells needed, from left to right.
    :param start_index: Row to start the search from
    :return: The index of the row in the worksheet that is empty and has the specified number of rows below.
    """
    row = start_index
    while True:
        if is_row_empty(ws, row, min_horizontal_empty_cells):
            satisfies_requirements = True
            for row_below in range(row + 1, empty_rows_below + 1):
                if not is_row_empty(ws, row_below, min_horizontal_empty_cells):
                    satisfies_requirements = False
                    break
            if satisfies_requirements:
                return row
            else:
                row += 1
        else:
            row += 1


def is_row_empty(ws: gspread.Worksheet, row: int, min_horizontal_empty_cells: int) -> bool:
    """
    Checks whether a given row in a worksheet is empty
    :param ws: Worksheet to check whether the given row is empty on.
    :param row: The index of the row to check
    :param min_horizontal_empty_cells: Minimum number of empty continuous cells needed, from left to right.
    :return: Whether there are at least min_horizontal_empty continuous empty cells in the row from left to right.
    """
    for col in range(1, 1 + min_horizontal_empty_cells):
        if ws.cell(row, col).value:
            return False
    return True


if __name__ == '__main__':
    sheet_name = "EID Data"  # Sheet name which the project has authorization for."
    sheet = gc.open(sheet_name)
    drinks_to_insert = {
        "Tom Collins",
        "Pina Colada",
        "Margarita",
        "Whiskey Sour",
        "Mojito",
        "Daiquiri",
        "Martini",
        "Old Fashioned",
        "White Russian",
        "Cuba Libre",
        "Long Island Iced Tea",
    }
    ingredients_to_insert = {
        "Gin",
        "Vodka",
        "Tequila",
        "Whiskey",
        "Rum",
        "Light rum",
        "Coffee liqueur",
        "Lemonade",
        "Scotch",
        "Tea",
        "Kahlua",
        "Everclear",
        "7-up"
    }
    # Pre-processing
    ingredients_sheet = sheet.add_worksheet("Ingredients", 100, 100)
    ingredients_sheet.insert_row(["Drink Name", "Ingredient", "Amount"])
    instructions_sheet = sheet.add_worksheet("Instructions", 100, 100)
    instructions_sheet.insert_row(["Drink Name", "Instruction"])
    drink_by_ingredient_sheet = sheet.add_worksheet("Ingredient to Drink", 100, 100)
    drink_by_ingredient_sheet.insert_row(["Ingredient", "Drink Names"])
    next_empty_row_ingredient = 2  # starting row
    next_empty_row_instructions = 2
    next_empty_row_drink_by_ingredient = 2
    while drinks_to_insert and False:
        name = drinks_to_insert.pop()
        cocktail = get_drink_by_name(name)
        try:
            next_empty_row_ingredient = write_cocktail_ingredients_into_spreadsheet_return_next_row(
                cocktail, ingredients_sheet, next_empty_row_ingredient)
            next_empty_row_instructions = write_cocktail_instructions_return_next_row(
                cocktail, instructions_sheet, next_empty_row_instructions)

        except gspread.exceptions.APIError:
            print("Reached rate limit. Waiting 30 seconds.")
            sleep(30)
            drinks_to_insert.add(name)
    while ingredients_to_insert:
        main_ingredient = ingredients_to_insert.pop()
        try:
            next_empty_row_drink_by_ingredient = write_cocktail_names_based_on_ingredient_return_next_row(
                main_ingredient, drink_by_ingredient_sheet, next_empty_row_drink_by_ingredient, limit=5
            )
        except gspread.exceptions.APIError:
            print("Reached rate limit. Waiting 30 seconds.")
            sleep(30)
            ingredients_to_insert.add(main_ingredient)
