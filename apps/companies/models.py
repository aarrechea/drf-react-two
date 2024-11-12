"""--------------------------------------------------------------------------------------
    Imports
--------------------------------------------------------------------------------------"""
from django.db import models
from apps.abstract.models import AbstractModel, AbstractManager
from apps.user.models import User
from apps.countries.models import Country
from apps.subsectors.models import Subsector



"""--------------------------------------------------------------------------------------
    Company model
--------------------------------------------------------------------------------------"""
class Company(AbstractModel):
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250, default='None', blank=True, null=True)
    postal_code = models.CharField(max_length=20, default='None', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, default='None', blank=True, null=True)
    year_establishment = models.IntegerField(default=0)
    year_first_expo = models.IntegerField(default=0)
    business_description = models.TextField(max_length=1000, default='None', blank=True, null=True)
    subsector = models.ForeignKey(Subsector, on_delete=models.CASCADE)
    comments = models.CharField(max_length=250, default='None', blank=True, null=True)
    eva_made = models.IntegerField(default=0)
    eva_progress = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ('name', 'user_creator', 'country', 'subsector', 'eva_made', 'created')
        db_table = 'apps.companies'









