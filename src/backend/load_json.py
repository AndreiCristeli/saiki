import json
from pathlib import Path
from saiki_site.models import HistoricalEntity  # ajuste o caminho do import

def load_entities():
    data_path = Path(__file__).resolve().parent / "../../data/ordering_template.json"

    with open(data_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for entry in entries:
        HistoricalEntity.objects.update_or_create(
            name=entry["name"],
            defaults={
                "type": entry["type"],
                "data": entry["data"]
        })
        