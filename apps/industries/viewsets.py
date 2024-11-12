""" Imports """
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.abstract.viewsets import AbstractViewSet
from apps.auth.permissions import UserPermission
from apps.industries.models import Industry
from apps.industries.serializers import IndustrySerializer



""" Industry viewset """
class IndustryViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = IndustrySerializer
    
    
    def get_queryset(self):        
        queryset = Industry.objects.all()
                      
        return queryset
    

    def create(self, request, *args, **kwargs):        
        serializer = self.get_serializer(data=request.data)        
        serializer.is_valid(raise_exception=True)        
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)