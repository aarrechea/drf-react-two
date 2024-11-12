""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.sectors.models import Sector


                
class SectorSerializer(AbstractSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'supersector']
