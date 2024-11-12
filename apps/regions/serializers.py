""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.regions.models import Region
from apps.user.models import User



""" Region serializer """
class RegionSerializer(AbstractSerializer):        
    class Meta:
        model = Region
        fields = ['id', 'name', 'created', 'updated']