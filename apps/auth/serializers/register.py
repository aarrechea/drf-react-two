""" Imports """
from rest_framework import serializers
from apps.user.models import User
from apps.user.serializers import UserSerializer



""" Register serializer. Registration serializer for requests and user creation """
class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, required=True, write_only=True)
    
    """ List all the fields that can be included in a request of a response """
    class Meta:
        model = User        
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'user_type']
        
    """ Use the create_user method for the UserManager to create a new user. """
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
    



