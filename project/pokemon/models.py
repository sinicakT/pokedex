from django.contrib.postgres.fields import ArrayField
from django.db import models

from project.pokemon.abstract_models import BaseModel


class Ability(BaseModel):
    class Meta:
        app_label = "pokemon"
        verbose_name = "Ability"
        verbose_name_plural = "Abilities"


class Stat(BaseModel):
    class Meta:
        app_label = "pokemon"
        verbose_name = "Stat"
        verbose_name_plural = "Stats"

class Species(BaseModel):
    order = models.IntegerField(verbose_name="Order", default=0)
    gender_rate = models.IntegerField(verbose_name="Gender Rate", default=0)
    capture_rate = models.IntegerField(verbose_name="Capture Rate", default=0)
    base_happiness = models.IntegerField(verbose_name="Base Happiness", default=0)
    hatch_counter = models.IntegerField(verbose_name="Hatch Counter", default=0)
    is_baby = models.BooleanField(verbose_name="Is Baby", default=False)
    is_legendary = models.BooleanField(verbose_name="Is Legendary", default=False)
    is_mythical = models.BooleanField(verbose_name="Is Mythical", default=False)
    has_gender_differences = models.BooleanField(verbose_name="Has Gender Differences", default=False)
    forms_switchable = models.BooleanField(verbose_name="Forms Switchable", default=False)

    class Meta:
        app_label = "pokemon"
        verbose_name = "Species"
        verbose_name_plural = "Species"


class Type(BaseModel):
    double_dmg_to = ArrayField(models.IntegerField(), default=list, blank=True)
    double_dmg_from = ArrayField(models.IntegerField(), default=list, blank=True)
    half_dmg_from = ArrayField(models.IntegerField(), default=list, blank=True)
    half_dmg_to = ArrayField(models.IntegerField(), default=list, blank=True)
    no_dmg_from = ArrayField(models.IntegerField(), default=list, blank=True)
    no_dmg_to = ArrayField(models.IntegerField(), default=list, blank=True)
    image = models.URLField("Image url", default=None, null=True)

    class Meta:
        app_label = "pokemon"
        verbose_name = "Type"
        verbose_name_plural = "Types"

class Pokemon(models.Model):
    name = models.CharField("Name", max_length=255)
    external_id = models.IntegerField("External id", db_index=True)
    base_experience = models.IntegerField("Base experience", default=0)
    image = models.URLField("Image url", default=None, null=True)
    height = models.IntegerField("Height", default=0)
    weight = models.IntegerField("Weight", default=0)
    order = models.IntegerField("Order", default=0)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    stats = models.ManyToManyField(Stat, through="PokemonStat", related_name="pokemon_stats")
    types = models.ManyToManyField(Type, related_name="pokemon_types")
    abilities = models.ManyToManyField(Ability, related_name="pokemon_abilities")

    def __str__(self):
        return self.name

    class Meta:
        app_label = "pokemon"
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"


class PokemonStat(models.Model):
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    stat = models.ForeignKey("Stat", on_delete=models.CASCADE)
    base_stat = models.IntegerField(default=0)
    effort = models.IntegerField(default=0)

    class Meta:
        unique_together = ("pokemon", "stat")
        verbose_name = "Pokemon Stat"
        verbose_name_plural = "Pokemon Stats"