from tqdm import tqdm

from project.pokemon.models import Pokemon, Species, Type, Stat, Ability, PokemonStat
from project.sync.helpers import PokeApiHelper
from project.sync.importers.base import BaseImporter
from project.sync.utils import link_to_external_id


class PokemonImporter(BaseImporter):
    model = Pokemon

    def __init__(self):
        super().__init__()
        self.species_map = {}
        self.types_map = {}
        self.abilities_map = {}
        self.stats_map = {}

    def get_item(self):
        return self.service.get_items(PokeApiHelper.POKEMON, batch_size=50)

    def prepare_maps(self):
        self.species_map = {s.external_id: s for s in Species.objects.all()}
        self.types_map = {t.external_id: t for t in Type.objects.all()}
        self.abilities_map = {a.external_id: a for a in Ability.objects.all()}
        self.stats_map = {s.external_id: s for s in Stat.objects.all()}

    def sync(self):
        model_name = self.model.__name__
        print(f"\nImporting {model_name}...")

        self.prepare_maps()

        item_iterator = self.get_item()
        item_iterator = tqdm(item_iterator, desc=f"{model_name} import", unit="item")

        for item in item_iterator:
            mapped = self.map_item(item)
            if not mapped:
                continue

            ext_id = mapped["external_id"]
            defaults = mapped["defaults"]

            types = defaults.pop("types", [])
            abilities = defaults.pop("abilities", [])
            stats = defaults.pop("stats", [])

            pokemon, created = self.model.objects.update_or_create(
                external_id=ext_id,
                defaults=defaults
            )

            pokemon.types.set(types)
            pokemon.abilities.set(abilities)

            for s in item.get("stats", []):
                stat_id = link_to_external_id(s["stat"]["url"])
                stat_obj = self.stats_map.get(stat_id)
                if not stat_obj:
                    continue

                PokemonStat.objects.update_or_create(
                    pokemon=pokemon,
                    stat=stat_obj,
                    defaults={
                        "base_stat": s.get("base_stat", 0),
                        "effort": s.get("effort", 0)
                    }
                )

    def map_item(self, item):
        # --- species ---
        species_url = item.get("species", {}).get("url")
        if not species_url:
            return None
        species_id = link_to_external_id(species_url)
        species = self.species_map.get(species_id)
        if not species:
            return None

        # --- types ---
        types = []
        for t in item.get("types", []):
            type_id = link_to_external_id(t["type"]["url"])
            type_obj = self.types_map.get(type_id)
            if not type_obj:
                return None
            types.append(type_obj)

        # --- abilities ---
        abilities = []
        for a in item.get("abilities", []):
            ability_id = link_to_external_id(a["ability"]["url"])
            ability_obj = self.abilities_map.get(ability_id)
            if not ability_obj:
                return None
            abilities.append(ability_obj)

        return {
            "external_id": item["id"],
            "defaults": {
                "name": item["name"],
                "height": item.get("height", 0),
                "weight": item.get("weight", 0),
                "base_experience": item.get("base_experience", 0),
                "order": 99999 if (order := item.get("order", 0)) < 0 else order,
                "image": item.get("sprites", {}).get("front_default"),
                "species": species,
                "types": types,
                "abilities": abilities,
                "stats": item.get("stats", []),
            }
        }
