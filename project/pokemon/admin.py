from django.contrib import admin
from project.pokemon.models import (
    Pokemon, Type, Species, Stat, Ability, PokemonStat
)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ("name", "external_id", "species", "base_experience", "order")
    list_filter = ("species", "types", "abilities")
    search_fields = ("name",)
    autocomplete_fields = ("species", "types", "abilities", "stats")
    ordering = ("order",)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "gender_rate", "capture_rate", "is_legendary", "is_mythical", "external_id")
    search_fields = ("name",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "external_id")
    search_fields = ("name",)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "external_id")
    search_fields = ("name",)


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "external_id")
    search_fields = ("name",)

