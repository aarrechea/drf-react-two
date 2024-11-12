""" Imports """
from django.db import models
from apps.abstract.models import AbstractModel, AbstractManager



""" Choices """
LETTERS = (
        (1,'A'), (2,'B'), (3,'C'), (4,'D'), (5,'E'), (6,'F'), (7,'G'), (8,'H'), (9,'I'),
        (10,'J'), (11,'K'), (12,'L'), (13,'M'), (14,'N'), (15,'O'), (16,'P'), (17,'Q'), (18,'R'),
        (19,'S'), (20,'T'), (21,'U'), (22,'V'), (23,'W'), (24,'X'), (25,'Y'), (26,'Z')
    )

ELEMENT_TYPE = (
        ('1', 'Competence'), ('2', 'Capability'), ('3', 'Process')
    )



""" Element manager """
class ElementManager(AbstractManager):
    pass



""" Element class """
class Element(AbstractModel):                    
    user_creator = models.ForeignKey(to="apps_user.User", on_delete=models.CASCADE)
    element_type = models.CharField(choices=ELEMENT_TYPE, verbose_name='Element Type')
    letter = models.IntegerField(choices=LETTERS, verbose_name="Letter")
    name = models.CharField(max_length=250, verbose_name='Competence name', null=False, blank=False)
    comments = models.CharField(max_length=255, verbose_name='Comments', default='None')
    eva_progress = models.IntegerField(default=0)
    eva_made = models.IntegerField(default=0)
    definitions = models.TextField(verbose_name="Definitions", blank=True, default="None", max_length=2000)
    symptoms = models.TextField(verbose_name="Symptoms", blank=True, default="None", max_length=3000)
    questions = models.TextField(verbose_name="Sample questions", blank=True, default="None", max_length=3000)
    assess_one = models.TextField(default="None", blank=True, max_length=1000)
    assess_two = models.TextField(default="None", blank=True, max_length=1000)
    assess_three = models.TextField(default="None", blank=True, max_length=1000)
    assess_four = models.TextField(default="None", blank=True, max_length=1000)
    assess_five = models.TextField(default="None", blank=True, max_length=1000)
   
    class Meta:
        verbose_name = 'Element'
        verbose_name_plural = 'Elements'
        ordering = ('element_type', 'letter', 'name', 'created')
        db_table = 'apps.element'

    





