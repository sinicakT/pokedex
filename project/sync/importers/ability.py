from project.pokemon.models import Ability
from project.sync.helpers import PokeApiHelper
from project.sync.importers.base import BaseImporter
from project.sync.utils import link_to_external_id


class AbilityImporter(BaseImporter):
    model = Ability

    def get_item(self):
        return self.service.get_items(PokeApiHelper.ABILITY, batch_size=50)

    def map_item(self, item):
        return {
            "name": item["name"],
            "external_id": link_to_external_id(item["url"])
        }
