# views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Pokemon
from .serializers import PokemonSerializer


class PokeAPIRetrieveView(RetrieveAPIView):
    """
    PokeAPIRetrieveView gets details of a pokemon.
    """

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = (AllowAny,)
    lookup_field: str = "name"


class PokeAPIListView(ListAPIView):
    """
    PokeAPIListView gets a list of pokemons stored in database.
    """

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = (AllowAny,)
