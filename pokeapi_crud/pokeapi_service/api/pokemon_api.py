# pokemon_requests.py
import logging
from json import loads

from requests_threads import AsyncSession
from twisted.internet.task import react

from pokeapi_crud.pokeapi_service.models import Pokemon

from .defaults import DEFAULT_LOAD_SIZE, EVOLUTION_CHAIN_URL, POKEMON_URL


class PokemonApi:
    def __init__(self, load_size: int = DEFAULT_LOAD_SIZE):
        self.session = AsyncSession(n=100)
        self.log = logging.getLogger(__name__)
        self.load_size = load_size

    def initDb(self) -> None:
        """
        initDb initializes the database with pokemons data
        """

        async def main(refactor):
            if Pokemon.objects.count():
                self.log.info("Loading pokeapi command")
                Pokemon.objects.all().delete()
            evolution_chain = await self.get_evolution_chain()
            species_url = await self.get_species_url_list(evolution_chain)
            evolution_list = await self.get_evolutions(evolution_chain)
            pokemons = await self.get_pokemons(species_url, evolution_list)
            poke = None
            for pokemon in pokemons:
                if pokemon:
                    poke = Pokemon.objects.create(
                        name=pokemon.get("name"),
                        weight=pokemon.get("weight"),
                        height=pokemon.get("height"),
                        stats=pokemon.get("stats", []),
                        evolutions=pokemon.get("evolutions", []),
                    )
                    self.log.info(str(poke))

            if not poke:
                raise RuntimeError("There's an error during filling database.")

        try:
            react(main)
        except:  # noqa: E722
            """
            The execution of the coroutines finish successfully. Also exists
            a final result with an Error raised but there's no a clear message
            about the incident.
            TODO: fix this
            """
        finally:
            self.log.info("PokeAPI command `success`")

    async def get_evolution_chain(self) -> list[dict[str, any]]:
        """
        get the evolution chain of first 400 pokemons stored into pokeapi
        evolution chain service
        Returns:
            - pokemon_evolution_chain: List[Dict[str, any]] | A list with the result
                of the evolution chain pokemon api service.
        """
        self.log.info("Getting evolution chain.")
        res = [
            await self.session.get(f"{EVOLUTION_CHAIN_URL}/{id}/")
            for id in range(self.load_size)
        ]
        return [loads(response.text) for response in res if response.status_code == 200]

    async def get_species_url_list(
        self, pokemon_evolution_chains: list[dict[str, any]]
    ) -> list[str]:
        """
        get a list of pokemon species url
        Parameters:
            - pokemon_evolution_chains: List[Dict[str, any] | A list with evolution chains of pokemons.
        Returns:
            - species_url_list: List[str] | A list with all urls of the pokemons to get its information
                on pokeapi pokemon service.
        """
        self.log.info("Getting species url list.")
        pokemon_url_list = [
            pokemon.get("chain", {}).get("species", {}).get("url")
            for pokemon in pokemon_evolution_chains
            if pokemon
        ]
        pokemon_id_list = [
            pokemon_id.split("/")[-2] for pokemon_id in pokemon_url_list if pokemon_id
        ]
        return [f"{POKEMON_URL}/{id}/" for id in pokemon_id_list if id]

    async def get_pokemons(
        self, pokemon_species_url_list: list[str], evolutions: dict[str, any]
    ) -> list[dict[str, any]]:
        """
        get pokemons dictionary with some properties
        Parameters:
            - pokemon_species_url_list: List[str]
            - evolutions: Dict[str, any]
        Returns:
            - pokemons: List[Dict[str, any]] | A list with dicts of pokemons data.
        """
        self.log.info("Creating pokemon data.")
        res = [
            await self.session.get(pokemon_species_url)
            for pokemon_species_url in pokemon_species_url_list
            if pokemon_species_url
        ]

        pokemons: list[dict[str, any]] = []
        for response in res:
            if response.status_code == 200:
                data = loads(response.text)
                pokemon_name = data.get("name")
                pokemons.append(
                    {
                        "id": int(data.get("id")),
                        "name": pokemon_name,
                        "weight": data.get("weight"),
                        "height": data.get("height"),
                        "stats": data.get("stats", {}),
                        "evolutions": evolutions.get(pokemon_name, []),
                    }
                )
        return pokemons

    async def get_evolutions(
        self, chain_list: list[dict[str, any]]
    ) -> dict[str, list[str]]:
        """
        get evolution chains list with the pokemon names of each pokemon
        Parameters:
            - chain_list: List[Dict[str, any]] | The chain evolution of the pokemons.
        Returns:
            - evolutions: Dict[str, List[str]] | The key is the name of the pokemon and the
                value is a list with its evolution names.
        """
        self.log.info("Getting evolutions by pokemon name.")
        evolutions = dict()
        for chain in chain_list:
            chain: dict[str, any] = chain.get("chain", {})
            pokemon_name = chain.get("species", {}).get("name")
            if pokemon_name:
                evolutions[pokemon_name] = []
                current_chain: list[dict[str, any]] = chain.get("evolves_to")
                while True:
                    if current_chain:
                        current_name = current_chain[0].get("species").get("name")
                        if current_name:
                            evolutions[pokemon_name].append(current_name)
                            current_chain = current_chain[0].get("evolves_to")
                    else:
                        break
        return evolutions
