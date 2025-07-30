import json
from pathlib import Path
from .models import ModelAlgorithm


def load_entities():
    data_path = Path(__file__).resolve().parent / "test.json"

    with open(data_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for entry in entries:
        ModelAlgorithm.objects.update_or_create(
            name=entry["name"],
            defaults={
                "category": entry["data"]["category"],
                "year": entry["data"]["year"],
                "generality": entry["data"]["generality"],
                "data_structure": entry["data"]["data_structure"],
                "temporal_complexity": entry["data"]["average_time_complexity"],
                "spatial_complexity": entry["data"]["auxiliary_space_complexity"],
                "solution_type": entry["data"]["kind_of_solution"]
            }
        )


if __name__ == "__main__":
    load_entities()
