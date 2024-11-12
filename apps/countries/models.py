""" Imports """
from django.db import models
from apps.abstract.models import AbstractModel
from apps.continents.models import Continent
from apps.regions.models import Region



"""--------------------------------------------------------------------------------------
    Country model
--------------------------------------------------------------------------------------"""
class Country(models.Model):
    name = name = models.CharField(max_length=150, verbose_name='Country')
    inhabitants = models.IntegerField(default=0)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
   
   
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name', 'continent', 'region')
        db_table = 'apps.country'
