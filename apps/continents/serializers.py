""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.continents.models import Continent
from apps.user.models import User



""" Company serializer """
class ContinentSerializer(AbstractSerializer):        
    class Meta:
        model = Continent
        fields = ['id', 'name', 'created', 'updated']