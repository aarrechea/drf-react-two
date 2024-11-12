""" Imports """
from rest_framework import serializers
from apps.abstract.serializers import AbstractSerializer
from apps.user.models import User



""" User serializer class """
class UserSerializer(AbstractSerializer):    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_type', 'email', 'created', 'updated', 'is_active']
        read_only_fields = ['is_active']


