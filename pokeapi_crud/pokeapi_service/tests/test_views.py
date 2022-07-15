from django.test import Client, TestCase
from django.urls import reverse

from pokeapi_crud.pokeapi_service.models import Pokemon

from .test_defaults import (
    DEFAULT_POKEMON_EVOLUTIONS,
    DEFAULT_POKEMON_HEIGHT,
    DEFAULT_POKEMON_NAME,
    DEFAULT_POKEMON_STATS,
    DEFAULT_POKEMON_WEIGHT,
)


class PokeAPIRetrieveViewTestCase(TestCase):
    def setUp(self):
        self.pokemon: Pokemon = Pokemon.objects.create(
            name=DEFAULT_POKEMON_NAME,
            height=DEFAULT_POKEMON_HEIGHT,
            weight=DEFAULT_POKEMON_WEIGHT,
            stats=DEFAULT_POKEMON_STATS,
            evolutions=DEFAULT_POKEMON_EVOLUTIONS,
        )
        self.client = Client()

    def test_pokeapiretrieveview_success(self):
        response = self.client.get(
            reverse("pokemon:retrieve", kwargs={"name": DEFAULT_POKEMON_NAME})
        )
        expected_status_code = 200
        self.assertEqual(response.status_code, expected_status_code)

    def test_pokeapiretrieveview_name_exists(self):
        response = self.client.get(
            reverse("pokemon:retrieve", kwargs={"name": DEFAULT_POKEMON_NAME})
        )
        pokemon_json: dict[str, any] = response.json()
        expected_pokemon_name = "charmander"
        self.assertEqual(pokemon_json.get("name"), expected_pokemon_name)

    def test_pokeapilistview_success(self):
        response = self.client.get(reverse("pokemon:list"))
        expected_status_code = 200
        self.assertEqual(response.status_code, expected_status_code)

    def test_pokeapilist_view_pokemon_in_json(self):
        response = self.client.get(reverse("pokemon:list"))
        pokemon_json: list[dict[str, any]] = response.json()
        expected_name = "charmander"
        self.assertIn(expected_name, pokemon_json[0]["name"])
