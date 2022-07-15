from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class PokeApiCommandTestCase(TestCase):
    def test_load_pokeapi_command(self):
        out = StringIO()
        call_command("pokecommand", 10, stdout=out)
        self.assertIn("PokeAPI loaded successfully", out.getvalue())
