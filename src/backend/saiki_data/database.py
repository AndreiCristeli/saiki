"""
backend/saiki_site/database.py

Defines the databases interface.
Interaction externally to this module must be made via them.
"""

import json
from typing import Iterator

from django.core.exceptions import ObjectDoesNotExist

from .models import ModelAlgorithm
from .entities import HistoricalEntity


class SaikiEntityDatabase(object):
    """Handles the historical-entity database for the project.
    @TODO: Singleton. Base-class."""

    __slots__: list[str] = [
        "__static_json_data_stream",
        "__entities"
    ]

    __static_json_data_stream: list[dict]

    def __init__(self) -> None:
        try:
            __all_objects = list(ModelAlgorithm.objects.all())
            self.__entities = list(map(lambda x: x.to_historical_entity(), __all_objects))

        except Exception as e:
            print(e)
            self.__entities: list = list()

        print(self.__entities)
        
        # Obs:
        # Currently, the database fetch is mocked.

        from os import path
        data_path: str = path.join(path.dirname(__file__), "test.json")

        with open(data_path, "r", encoding="utf-8") as file:
            self.__static_json_data_stream: list[dict] = json.load(file)

        for entry in self.__static_json_data_stream:
            entry: dict = entry["data"]

            for data_field in entry:
                if not isinstance(entry[data_field], list):
                    # then we have to list it.
                    entry[data_field] = [entry[data_field]]

    def __len__(self) -> int:
        """Returns how many historical entities are there in the database."""
        return len(self.__static_json_data_stream)

    def __getitem__(self, item: int) -> HistoricalEntity:
        """`get_entity()` callback. Retrieves an entity by its index."""
        if not isinstance(item, int):
            raise TypeError()

        return self.get_entity(index=item)
    
    def all(self) -> list[HistoricalEntity]:
        return self.__entities

    def get_entity(self, index: int) -> HistoricalEntity:
        """Retrieves an entity by its index in the data pool.
            :param index: The 0-based index.
            :return: The json dictionary associated with the entity entry.
            :raises IndexError: If the index is out of the bounds."""

        if index < 0 or index >= len(self):
            raise IndexError()

        # @TODO: Replace mock with ModelAlgorithm interaction.
        return HistoricalEntity.from_json_mock_data(self.__static_json_data_stream[index])

    def fetch_entity(self, name: str) -> tuple[HistoricalEntity, int]:
        """Attempts finding an entity on the database.
        Returns it, as well as its index."""

        # @TODO: Replace mock with ModelAlgorithm interaction.
        for i, entity in enumerate(self.__static_json_data_stream):
            if entity["name"].lower() == name:
                return HistoricalEntity.from_json_mock_data(entity), i

        raise KeyError(f"Couldn't find entity with name '{name}'.")

        try:
            return ModelAlgorithm.objects.get(name=name)

        except ObjectDoesNotExist:
            raise KeyError(f"Didn't found alg. with name {name}.")

    def __iter__(self) -> Iterator:
        """Iterates over all the entities."""

        # @TODO: Replace mock with ModelAlgorithm interaction.
        def __generate_entities() -> Iterator:
            """Generator over the static mocked data."""
            for entity in self.__static_json_data_stream:
                yield entity

        return __generate_entities()


# Main Instantiation
# ------------------

saiki_entities: SaikiEntityDatabase = SaikiEntityDatabase()

