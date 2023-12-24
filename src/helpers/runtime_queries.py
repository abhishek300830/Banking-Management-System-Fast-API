import json

from src.utils.setting_file import SQL_QUERYS_JSON_PATH

QUERIES = None


with open(SQL_QUERYS_JSON_PATH, "r") as file:
    QUERIES = json.load(file)
