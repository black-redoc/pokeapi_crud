from django.contrib import admin

from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "height",
        "weight",
        "stats",
        "evolutions",
    )
