""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.supersectors.models import Supersector


class SupersectorSerializer(AbstractSerializer):
    class Meta:
        model = Supersector
        fields = ['id', 'name', 'industry']       
