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
            "external_id": item["id"],
            "double_dmg_to": [link_to_external_id(i["url"]) for i in item.get("damage_relations", []).get("double_damage_from", [])],
            "double_dmg_from": [link_to_external_id(i["url"]) for i in item.get("damage_relations", []).get("double_damage_to", [])],
            "half_dmg_from": [link_to_external_id(i["url"]) for i in item.get("damage_relations", []).get("half_damage_from", [])],
            "half_dmg_to": [link_to_external_id(i["url"]) for i in item.get("damage_relations", []).get("half_damage_to", [])],
            "no_dmg_from": [link_to_external_id(i["url"]) for i in item.get("damage_relations", []).get("no_damage_from", [])],
            "no_dmg_to": [link_to_external_id(i["url"]) for i in item.get("damage_relations", []).get("no_damage_to", [])],
        }
