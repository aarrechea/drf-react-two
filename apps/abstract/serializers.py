""" Imports """
from rest_framework import serializers



""" Abstract serializer """
class AbstractSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)




