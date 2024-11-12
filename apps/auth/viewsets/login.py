""" Imports """
import datetime
from django.contrib.gis.geoip2 import GeoIP2
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from apps.auth.serializers import LoginSerializer
from apps.logs.models import Logs



""" Login viewset """
class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):                        
        serializer = self.serializer_class(data=request.data)
                        
        # To get the ip address to know where the user is conncected from.
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
                      
                
        # Get the city and the country of the ip
        g = GeoIP2()
        try:            
            country = g.country(ip_address)['country_name']
        except:
            country = "Unknown"
        
        try:                    
            city = g.city(ip_address)['city']
        except:
            city = "Unknown"
            
            
        # Create the object in the database.
        new_log = Logs(ip=ip_address, location_country=country, location_city=city)
        new_log.save()
                
        try:                        
            serializer.is_valid(raise_exception=True)
        except TokenError as e:                                    
            raise InvalidToken(e.args[0])                                         
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    



