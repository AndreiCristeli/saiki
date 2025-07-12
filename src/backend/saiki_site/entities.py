"""
backend/saiki_site/entities.py

@TODO
"""

from __future__ import annotations

from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import Any


class HistoricalEntity(ABC):
    """Represents a historical-entity in the system."""

    _json_dict: dict[str, list]

    @property
    def name(self) -> str:
        """Retrieves the entity's name."""
        return self["name"]

    @property
    @abstractmethod
    def type_name(self) -> str:
        return "entity"

    def __init__(self, name: str, ** kwargs) -> None:
        self._json_dict: dict[str, str | list] = {
            "name": name
        }

        for kw, v in kwargs.items():
            kw: str
            self._json_dict[kw] = v

    def __getitem__(self, item: str) -> str | list:
        """Returns the corresponding JSON item."""
        if not isinstance(item, str):
            raise TypeError

        return self._json_dict[item]

    def __matmul__(self, item: tuple[str, list]) -> str:
        """`compare_field` operator wrapper."""

        if not isinstance(item, tuple) and len(item) == 2:
            raise TypeError(0)

        elif not isinstance(item[1], list):
            raise TypeError(1)

        return self.compare_field(*item)

    def compare_field(self, field_name: str, field_item: list[str]) -> str:
        """Compares two entities fields for guessing, verifying if A \\subseteq B.
        Let A be the parameter field and B be the corresponding on this object.
        Returns "correct", if A == B, "partial" if A \\subset B, and "wrong" otherwise."""

        if field_name not in self._json_dict:
            raise ValueError(f"field_name: {field_name} ({self._json_dict})")

        # A == B
        if field_item == self._json_dict[field_name]:
            return "correct"

        # A \\subset B
        for a in field_item:
            if a in self._json_dict[field_name]:
                return "partial"

        # A \\nsubset B
        return "wrong"

    @staticmethod
    def from_type(entity_type: str, *args, **kwargs) -> HistoricalEntity:
        """Returns an Entity from the specified type."""

        possible_entities_type: dict[str, type] = {
            "algorithm": Algorithm,
        }

        if entity_type not in possible_entities_type:
            raise ValueError("...")

        return possible_entities_type[entity_type](
            *args,
            **kwargs,
        )


class Algorithm(HistoricalEntity):
    """Represents the algorithm entity."""

    @property
    def type_name(self) -> str:
        return "algorithm"

    def __init__(self, name: str, ** kwargs) -> None:

        fields: list[str] = ["category", "year", "average_time_complexity", "auxiliary_space_complexity",
                             "data_structure", "kind_of_solution", "generality"]

        for key in kwargs:
            if key not in fields:
                raise KeyError("arrombado1")

            fields.pop(fields.index(key))

        if fields:
            raise KeyError("arrombado2")

        super().__init__(name, ** kwargs)


if __name__ == "__main__":
    Algorithm("Victor's algorithm", category="cmrd", year=2025, average_time_complexity="O(n)",
              auxiliary_space_complexity="O(n)", data_structure="List", kind_of_solution="Just wrong",
              generality="Doidera")
