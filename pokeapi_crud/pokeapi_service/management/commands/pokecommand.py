from django.core.management.base import BaseCommand, CommandError, CommandParser

from pokeapi_crud.pokeapi_service.api.pokemon_api import PokemonApi


class Command(BaseCommand):
    help = "Downloads pokemons from https://pokeapi.co/ and stores into database"

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)
        parser.add_argument("load_size", type=int)

    def handle(self, *args, **options):
        try:
            size = options.get("load_size", None)
            api: PokemonApi
            if size:
                api = PokemonApi(size)
            api = PokemonApi()
            api.initDb()
            self.stdout.write(self.style.SUCCESS("PokeAPI loaded successfully"))
        except RuntimeError as error:
            raise CommandError(f"Pokeapi error. {error}")
