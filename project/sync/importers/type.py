from project.pokemon.models import Type
from project.sync.helpers import PokeApiHelper
from project.sync.importers.base import BaseImporter
from project.sync.utils import link_to_external_id


class TypeImporter(BaseImporter):
    model = Type

    def get_item(self):
        return self.service.get_items(PokeApiHelper.TYPE, batch_size=50)

    def map_item(self, item):
        return {
            "name": item["name"],
            "external_id": link_to_external_id(item["url"])
        }
