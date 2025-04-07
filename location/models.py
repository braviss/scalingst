from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    country = CountryField(verbose_name=_("Country"))  # используем код страны (например, 'UA')
    name = models.CharField(max_length=100, verbose_name=_("Region"))

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        unique_together = ("country", "name")

    def __str__(self):
        return f"{self.name} ({self.country.code})"


class Locality(models.Model):
    class LocalityType(models.TextChoices):
        CITY = 'city', _('City')
        TOWN = 'town', _('Town')
        VILLAGE = 'village', _('Village')

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='localities')
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    type = models.CharField(max_length=10, choices=LocalityType.choices, verbose_name=_("Type"))

    class Meta:
        verbose_name = _("Locality")
        verbose_name_plural = _("Localities")
        unique_together = ("region", "name", "type")

    def __str__(self):
        return f"{self.get_type_display()} {self.name} ({self.region.name})"