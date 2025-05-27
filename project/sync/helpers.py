
import requests
from django.conf import settings

from project.sync.utils import retry


class PokeApiHelper:
    POKEMON = "pokemon"
    STAT = "stat"
    TYPE = "type"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = settings.POKE_API.get("url", "")
        self.AVAILABLE_ENDPOINTS = {
          self.POKEMON: {
              "list": self.get_pokemon_list,
              "detail": self.get_pokemon_detail,
          },
          self.STAT: {
              "list": self.get_pokemon_list,
              "detail": None,
          },
          self.TYPE: {
              "list": self.get_pokemon_list,
              "detail": None,
          },
        }

    @retry()
    def get(self, endpoint, item_id=None, params=None, retries=3, delay=1):
        if not endpoint in self.AVAILABLE_ENDPOINTS:
            raise ValueError(f"Endpoint {endpoint} is not available")

        if not params:
            params = {}

        url = f"{self.url}/{endpoint}/"
        if item_id is not None:
            url = f"{url}{item_id}/"

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_pokemon_list(self, offset=0, limit=250):
        return self.get(self.POKEMON, params={"limit": limit, "offset": offset})

    def get_pokemon_detail(self, pokemon_id):
        return self.get(self.POKEMON, pokemon_id)

    def get_states(self, offset=0, limit=50):
        return self.get(self.STAT, params={"limit": limit, "offset": offset})

    def get_types(self, offset=0, limit=50):
        return self.get(self.TYPE, params={"limit": limit, "offset": offset})
