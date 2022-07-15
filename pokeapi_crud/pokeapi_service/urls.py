# urls.py
from django.urls import path

from .views import PokeAPIListView, PokeAPIRetrieveView

urlpatterns = (
    path("<name>/", PokeAPIRetrieveView.as_view(), name="retrieve"),
    path("pokemons/", PokeAPIListView.as_view(), name="list"),
)
