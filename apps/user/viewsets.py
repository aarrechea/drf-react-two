""" Imports """
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.abstract.viewsets import AbstractViewSet
from apps.user.serializers import UserSerializer
from apps.user.models import User



""" User viewset """
class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()                
        
        return User.objects.exclude(is_superuser=True)
    
    def get_object(self):        
        obj = User.objects.get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        
        return obj



