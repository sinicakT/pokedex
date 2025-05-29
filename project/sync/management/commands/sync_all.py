from django.core.management.base import BaseCommand

from project.sync.importers.ability import AbilityImporter
from project.sync.importers.pokemon import PokemonImporter
from project.sync.importers.type import TypeImporter
from project.sync.importers.stat import StatImporter
from project.sync.importers.species import SpeciesImporter

class Command(BaseCommand):
    help = "Synchronize all models from external API"

    def handle(self, *args, **options):
        importers = [
            ("Ability", AbilityImporter),
            ("Type", TypeImporter),
            ("Stat", StatImporter),
            ("Species", SpeciesImporter),
            ("Pokemon", PokemonImporter),
        ]

        print(f"Grab a coffee, this might take a while...")
        for name, Importer in importers:
            try:
                importer = Importer()
                importer.sync()
                print(f"[✓] Finished sync for {name}")
            except Exception as e:
                print(f"[✗] Error syncing {name}: {e}")