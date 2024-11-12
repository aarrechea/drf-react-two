# Imports
from django.db import models
from apps.abstract.models import AbstractModel



# Logs model
class Logs(AbstractModel):    
    ip = models.CharField(max_length=25)
    location_country = models.CharField(max_length=200, default="None")
    location_city = models.CharField(max_length=200, default="None")
    
    
    def __str__(self):
       return f"Ip: {self.ip} - Country: {self.location_country} - City: {self.location_city}"


