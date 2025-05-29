from project.pokemon.models import Species
from project.sync.helpers import PokeApiHelper
from project.sync.importers.base import BaseImporter


class SpeciesImporter(BaseImporter):
    model = Species

    def get_item(self):
        return self.service.get_items(PokeApiHelper.SPECIES, batch_size=50)

    def map_item(self, item):
        return {
            "name": item["name"],
            "external_id": item["id"],
            "order": item.get("order", 0),
            "gender_rate": item.get("gender_rate", 0),
            "capture_rate": item.get("capture_rate", 0),
            "base_happiness": item.get("base_happiness", 0),
            "hatch_counter": item.get("hatch_counter", 0),
            "is_baby": item.get("is_baby", False),
            "is_legendary": item.get("is_legendary", False),
            "is_mythical": item.get("is_mythical", False),
            "has_gender_differences": item.get("has_gender_differences", False),
            "forms_switchable": item.get("forms_switchable", False),
        }
