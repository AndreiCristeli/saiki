"""
backend/saiki_site/database.py

...
"""

import json
from typing import Iterable

from .models import Algorithm
from django.core.exceptions import ObjectDoesNotExist


class SaikiDatabase(object):
    """Handles the database for the project."""

    __static_json_data_stream: list[dict]

    def __init__(self) -> None:

        from os import path

        data_path: str = path.join(path.dirname(__file__), "test.json")

        # Currently, the database fetch is mocked.
        with open(data_path, "r", encoding="utf-8") as file:
            self.__static_json_data_stream: list[dict] = json.load(file)

        for entry in self.__static_json_data_stream:
            entry: dict = entry["data"]
            print("entry:", entry)

            for data_field in entry:
                if not isinstance(entry[data_field], list):
                    # then we have to list it.
                    entry[data_field] = [entry[data_field]]

    def __len__(self) -> int:
        return len(self.__static_json_data_stream)

    def get_entity(self, index: int) -> dict[str, str | list]:
        """Retrieves an entity by its index in the data pool.
            :param index: The 0-based index.
            :return: The json dictionary associated with the entity entry.
            :raises TypeError: If the index is out of the bounds."""
        return self.__static_json_data_stream[index]

    def fetch_algorithm(self, name: str):
        """Attempts getting an entity on the database."""

        for i, entity in enumerate(self.__static_json_data_stream):
            # @TODO: to abstract and improve comparison!
            if entity["name"].lower() == name:
                return entity, i

        return None, - 1

        try:
            return Algorithm.objects.get(name=name)

        except ObjectDoesNotExist:
            raise KeyError(f"Didn't found alg. with name {name}.")

    def get_all(self) -> Iterable:
        return self.__static_json_data_stream


# Main Instantiation
# ------------------

saiki_database: SaikiDatabase = SaikiDatabase()
