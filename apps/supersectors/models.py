# Imports
from django.db import models
from apps.industries.models import Industry



"""--------------------------------------------------------------------------------------
   Supersector model
--------------------------------------------------------------------------------------"""
class Supersector(models.Model):
   name = models.CharField(max_length=150)
   industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='supersectors')

   def __str__(self):
       return self.name