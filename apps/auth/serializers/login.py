""" Imports """
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from apps.user.serializers import UserSerializer



""" Login serializer """
class LoginSerializer(TokenObtainPairSerializer):                
    def validate(self, attrs):        
        # super() is a built-in method in python that returns a temporary object that can
        # be used to access the class methods of the base class        
        data = super().validate(attrs)        
        refresh = self.get_token(self.user)
                                                
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
            
        return data


