# serializers.py
from rest_framework.serializers import (
    CharField,
    FloatField,
    IntegerField,
    ListField,
    ModelSerializer,
)

from .models import Pokemon


class PokemonSerializer(ModelSerializer):
    id = IntegerField()
    name = CharField()
    weight = FloatField()
    height = FloatField
    stats = ListField()
    evolutions = ListField()

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "name",
            "weight",
            "height",
            "stats",
            "evolutions",
        )
