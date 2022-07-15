# models.py
from django.db.models import CharField, FloatField, JSONField, Model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Pokemon(Model):
    """
    Pokemon model
    """

    name = CharField(_("Name"), max_length=30)
    weight = FloatField(_("Weight"))
    height = FloatField(_("Height"))
    stats = JSONField(_("stats"))
    evolutions = JSONField(_("evolutions"))

    def get_absolute_url(self):
        """
        get url for the details pokemon view
        """
        return reverse_lazy("pokemon:retrieve", kwargs={"id": self.id})

    def __str__(self) -> str:
        """
        get a string representation of this object
        """
        return f"Pokemon({self.name})"
