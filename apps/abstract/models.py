""" Imports """
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404



""" Abstract manager """
class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
        
        

""" Abstract model """    
class AbstractModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    class Meta:
        abstract = True





