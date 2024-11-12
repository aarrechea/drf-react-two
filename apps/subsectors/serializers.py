""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.subsectors.models import Subsector


                
class SubsectorSerializer(AbstractSerializer):
    class Meta:
        model = Subsector
        fields = ['id', 'name', 'sector']
