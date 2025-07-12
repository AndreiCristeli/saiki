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

    def __init__(self, name: str) -> None:
        self._json_dict: dict[str, str | list] = {
            "name": name
        }

    def __getitem__(self, item: str) -> str | list:
        """Returns the corresponding JSON item."""
        if not isinstance(item, str):
            raise TypeError

        return self._json_dict[item]

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def type_name(self) -> str:
        return "entity"

    def __matmul__(self, item: tuple[str, list]) -> str:
        """`compare_field` operator wrapper."""

        if not isinstance(item, tuple) and len(item) == 2:
            raise TypeError(0)

        elif not isinstance(item[1], list):
            raise TypeError(1)
                
        return self.compare_field(* item)

    def compare_field(self, field_name: str, field_item: list[str]) -> str:
        """Compares two entities fields for guessing, verifying if A \\subseteq B.
        Let A be the parameter field and B be the corresponding on this object.
        Returns "correct", if A == B, "partial" if A \\subset B, and "wrong" otherwise."""

        if field_name not in self._json_dict:
            raise ValueError(0)

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
    def from_type(entity_type: str, * args, ** kwargs) -> HistoricalEntity:
        """Returns an Entity from the specified type."""

        possible_entities_type: dict[str, type] = {
            "algorithm": Algorithm,
        }

        if entity_type not in possible_entities_type:
            raise ValueError("...")

        return possible_entities_type[entity_type](
            * args,
            ** kwargs,
        )


class Algorithm(HistoricalEntity):

    def __init__(self, name: str, ** kwargs) -> None:
        super().__init__(name)

        for kw, v in kwargs.items():
            self._json_dict[kw] = v

    # def __contains__(self, item: tuple[str, list]) -> bool: ...



if __name__ == "__main__":
    Algorithm()
