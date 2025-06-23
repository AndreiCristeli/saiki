"""
backend/saiki_site/models.py

Django models used by the site.
"""

from django.db import models


"""
(Initially on src/backend/db/models.py. 
@TODO: CHANGE IT TO THERE, EVENTUALLY)
"""

from django.db import models
from django.db.models import CharField, IntegerField
from django.http import JsonResponse

from abc import abstractmethod


class Model_Saiki(models.Model):

    @abstractmethod
    def to_json(self) -> JsonResponse:
        ...


class Model_Algorithm(Model_Saiki):
    """Represents an algorithm; the entity."""

    name = CharField(max_length=32)
    year = IntegerField()
    category = CharField(max_length=32)
    data_structures = CharField(max_length=512)
    design_paradigm = CharField(max_length=32)
    generality = CharField(max_length=32)
    temporal_complexity = CharField(max_length=32)
    spatial_complexity = CharField(max_length=32)
    solution_kind = CharField(max_length=32)

    def to_json(self) -> JsonResponse:
        data: dict[str, CharField] = {
            "name": self.name,
            "year": self.year,
            "category": self.category,
            "design_paradigm": self.design_paradigm,
            "generality": self.generality,
            "temporal_complexity": self.temporal_complexity,
            "spatial_complexity": self.spatial_complexity,
            "solution_kind": self.solution_kind,
        }

        return JsonResponse(data)


# Testing

example_algorithm = Model_Algorithm(name="Merge sort",
                                    year=1945,
                                    category="Sorting",
                                    temporal_complexity="O(n log n)",
                                    spatial_complexity="O(n)",
                                    data_structures="array",
                                    solution_kind="exact",
                                    generality="general-purpose")
