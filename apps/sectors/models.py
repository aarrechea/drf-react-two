# Imports
from django.db import models
from apps.supersectors.models import Supersector



"""--------------------------------------------------------------------------------------
   Sector model
--------------------------------------------------------------------------------------"""
class Sector(models.Model):
   name = models.CharField(max_length=150)
   supersector = models.ForeignKey(Supersector, on_delete=models.CASCADE, related_name='sectors')

   def __str__(self):
       return self.name