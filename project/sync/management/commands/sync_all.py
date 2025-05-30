from django.core.cache import cache
from django.core.management.base import BaseCommand

from project.sync.importers.ability import AbilityImporter
from project.sync.importers.pokemon import PokemonImporter
from project.sync.importers.type import TypeImporter
from project.sync.importers.stat import StatImporter
from project.sync.importers.species import SpeciesImporter

class Command(BaseCommand):
    help = "Synchronize all models from external API"

    LOCK_KEY = "sync_lock"
    LOCK_TIMEOUT = 60 * 60

    def handle(self, *args, **options):
        if cache.get(self.LOCK_KEY):
            self.stdout.write(self.style.WARNING("⏳ Sync is already running. Exiting."))
            return

            # Set the lock
        cache.set(self.LOCK_KEY, True, timeout=self.LOCK_TIMEOUT)

        importers = [
            ("Ability", AbilityImporter),
            ("Type", TypeImporter),
            ("Stat", StatImporter),
            ("Species", SpeciesImporter),
            ("Pokemon", PokemonImporter),
        ]

        print(f"Grab a coffee, this might take a while...")
        try:
            for name, Importer in importers:
                try:
                    importer = Importer()
                    importer.sync()
                    print(f"[✓] Finished sync for {name}")
                except Exception as e:
                    print(f"[✗] Error syncing {name}: {e}")
        finally:
            cache.delete(self.LOCK_KEY)