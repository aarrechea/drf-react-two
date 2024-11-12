""" Imports """
from django.db import models
from apps.abstract.models import AbstractModel



""" Relation model """
class Relation(AbstractModel):
    name = models.CharField(max_length=255, verbose_name='Relation name', unique=True, blank=False, null=False)
    total_elements = models.IntegerField(default=0)
    competences = models.SmallIntegerField(default=0, verbose_name='Competences')
    capabilities = models.SmallIntegerField(default=0, verbose_name='Capabilities')
    processes = models.IntegerField(default=0, verbose_name='Processes')
    eva_made = models.IntegerField(default=0, verbose_name='Evaluations made')
    eva_progress = models.IntegerField(default=0, verbose_name='Evaluations in progress')    
    user_creator = models.ForeignKey(to="apps_user.User", on_delete=models.CASCADE)   
    comments = models.CharField(max_length=255, verbose_name="Comments", default="None")
    status = models.BooleanField(default=0) # whether the relation is open or close
    
    class Meta:
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'
        ordering = ('name', 'eva_made', 'eva_progress', 'status')
        db_table = "apps.relation"



