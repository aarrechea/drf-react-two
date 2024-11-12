# Imports
from django.db import models
from apps.sectors.models import Sector



"""--------------------------------------------------------------------------------------
   Subsector model
--------------------------------------------------------------------------------------"""
class Subsector(models.Model):
   name = models.CharField(max_length=150)
   sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='subsectors')

   def __str__(self):
      return self.name
