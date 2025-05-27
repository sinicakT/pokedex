import abc
from pyexpat import model

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from tqdm import tqdm

from project.sync.services import SyncService


class BaseImporter(metaclass=abc.ABCMeta):
    model = None
    sync_by = "external_id"
    batch_size = 100
    update_fields = "__all__"

    def __init__(self):
        if self.model is None:
            raise ImproperlyConfigured("You must define 'model' in your subclass.")

        self.service = SyncService()
        self.processed = set()
        self.items_batch = []
        self.existing_items = {item[self.sync_by]: item["id"] for item in self.model.objects.all().values(self.sync_by, "id")}

    @abc.abstractmethod
    def map_item(self, item):
        return item

    @abc.abstractmethod
    def get_item(self):
        pass

    def sync(self):
        model_name = self.model.__name__
        print(f"\nImporting {model_name}...")

        item_iterator = self.get_item()
        item_iterator = tqdm(item_iterator, desc=f"{model_name} import", unit="item")

        for item in item_iterator:
            mapped_item = self.map_item(item)
            if mapped_item:
                self.items_batch.append(mapped_item)
                self.processed.add(mapped_item[self.sync_by])

            if len(self.items_batch) >= self.batch_size:
                self.save_items()
                self.items_batch = []

        if self.items_batch:
            self.save_items()
            self.items_batch = []

    def save_items(self):
        create_objs = []
        update_objs = []

        for data in self.items_batch:
            obj = self.model(**data)
            sync_by_field = data.get(self.sync_by)

            if sync_by_field in self.existing_items.keys():
                if primary_key := self.existing_items[sync_by_field]:
                    obj.id = primary_key
                    update_objs.append(obj)
            else:
                create_objs.append(obj)
                self.existing_items[sync_by_field] = None

        with transaction.atomic():
            if create_objs:
                self.model.objects.bulk_create(create_objs, batch_size=self.batch_size)

            if update_objs:
                update_fields = self.update_fields
                if update_fields == "__all__":
                    update_fields = list(update_objs[0].__dict__.keys())
                    update_fields = [
                        f for f in update_fields if f not in ("_state", self.sync_by, "id")
                    ]

                self.model.objects.bulk_update(update_objs, update_fields, batch_size=self.batch_size)