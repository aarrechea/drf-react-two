""" Imports """
from django.db import models



"""--------------------------------------------------------------------------------------
    Continet model
--------------------------------------------------------------------------------------"""
class Continent(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"Name: {self.name} - Id: {self.id}"

