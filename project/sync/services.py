from project.sync.helpers import PokeApiHelper
from project.sync.utils import link_to_external_id


class SyncService:
    def __init__(self):
        self.helper = PokeApiHelper()

    def get_items(self, endpoint, with_detail=False, batch_size=250):
        if endpoint not in self.helper.AVAILABLE_ENDPOINTS:
            raise ValueError(f"Unsupported endpoint: {endpoint}")

        list_func = self.helper.AVAILABLE_ENDPOINTS[endpoint]["list"]
        detail_func = self.helper.AVAILABLE_ENDPOINTS[endpoint].get("detail")

        offset = 0
        total = None

        while True:
            data = list_func(offset=offset, limit=batch_size)
            results = data.get("results", [])

            if not results:
                break

            if total is None:
                total = data.get("count", 0)

            for item in results:
                if with_detail and detail_func:
                    item_id = link_to_external_id(item["url"])
                    yield detail_func(item_id)
                else:
                    yield item

            offset += batch_size

            if offset >= total:
                break