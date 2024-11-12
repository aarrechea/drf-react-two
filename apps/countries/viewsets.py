""" Imports """
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.abstract.viewsets import AbstractViewSet
from apps.auth.permissions import UserPermission
from apps.countries.models import Country
from apps.countries.serializers import CountrySerializer



""" Country viewset """
class CountryViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = CountrySerializer
    
    
    def get_queryset(self):
        queryset = Country.objects.all()
                        
        return queryset
    
    
    def create(self, request, *args, **kwargs):        
        serializer = self.get_serializer(data=request.data)        
        serializer.is_valid(raise_exception=True)        
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)