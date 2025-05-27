from django.db import models

from project.pokemon.abstract_models import BaseModel


class State(BaseModel):
    class Meta:
        app_label = "pokemon"
        verbose_name = "Stat"
        verbose_name_plural = "Stats"


class Type(BaseModel):
    class Meta:
        app_label = "pokemon"
        verbose_name = "Type"
        verbose_name_plural = "Types"


class Pokemon(models.Model):
    name = models.CharField("Name", max_length=255)
    external_id = models.IntegerField("External id", db_index=True)
    base_experience = models.IntegerField("Base experience", default=0)
    height = models.IntegerField("Height", default=0)
    weight = models.IntegerField("Weight", default=0)
    order = models.IntegerField("Order", default=0)
    stats = models.ManyToManyField(State, related_name="pokemon_states")
    types = models.ManyToManyField(Type, related_name="pokemon_types")

    def __str__(self):
        return self.name

    class Meta:
        app_label = "pokemon"
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"