from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PokeapiServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pokeapi_crud.pokeapi_service"
    verbose_name: str = _("Pokeapi Service")
