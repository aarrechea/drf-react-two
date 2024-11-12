""" Imports """
from django.db import models
from apps.abstract.models import AbstractModel
from apps.element.models import Element
from apps.relations.models import Relation


""" Relation tree holds each element in the relation with its respective information """
class RelationTree(models.Model):
    order = models.IntegerField()
    capability_number = models.CharField()
    process_number = models.CharField()
    percentage = models.DecimalField(decimal_places=2, max_digits=5)
    element_type = models.SmallIntegerField()
    relation_letter = models.SmallIntegerField()
    relation_letter_display = models.CharField()
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='element')
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE, related_name='relation_tree')
    related_capability = models.IntegerField(null=True, blank=True)
    related_competence = models.IntegerField(null=True, blank=True)
    
            
    class Meta:
        ordering = ('relation', 'order')
        db_table = "apps.relation_tree"




