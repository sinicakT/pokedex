from rest_framework import serializers

from .models import Pokemon, Stat, Type, Ability, PokemonStat


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'name']


class TypeSerializer(serializers.ModelSerializer):
    double_dmg_to = serializers.SerializerMethodField()
    double_dmg_from = serializers.SerializerMethodField()
    half_dmg_to = serializers.SerializerMethodField()
    half_dmg_from = serializers.SerializerMethodField()
    no_dmg_to = serializers.SerializerMethodField()
    no_dmg_from = serializers.SerializerMethodField()

    class Meta:
        model = Type
        fields = [
            'id', 'name', 'image',
            'double_dmg_to', 'double_dmg_from',
            'half_dmg_to', 'half_dmg_from',
            'no_dmg_to', 'no_dmg_from',
        ]

    def _resolve_types(self, external_ids):
        return list(Type.objects.filter(external_id__in=external_ids).values('name', 'image'))

    def get_double_dmg_to(self, obj):
        return self._resolve_types(obj.double_dmg_to)

    def get_double_dmg_from(self, obj):
        return self._resolve_types(obj.double_dmg_from)

    def get_half_dmg_to(self, obj):
        return self._resolve_types(obj.half_dmg_to)

    def get_half_dmg_from(self, obj):
        return self._resolve_types(obj.half_dmg_from)

    def get_no_dmg_to(self, obj):
        return self._resolve_types(obj.no_dmg_to)

    def get_no_dmg_from(self, obj):
        return self._resolve_types(obj.no_dmg_from)


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['id', 'name']


class PokemonStatSerializer(serializers.ModelSerializer):
    stat = StatSerializer()

    class Meta:
        model = PokemonStat
        fields = ['stat', 'base_stat', 'effort']


class PokemonDetailSerializer(serializers.ModelSerializer):
    stats = PokemonStatSerializer(source='pokemonstat_set', many=True)
    types = TypeSerializer(many=True)
    abilities = AbilitySerializer(many=True)

    class Meta:
        model = Pokemon
        fields = [
            'id', 'name', 'external_id', 'base_experience', 'image',
            'height', 'weight', 'order', 'stats', 'types', 'abilities'
        ]