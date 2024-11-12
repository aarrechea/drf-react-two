""" Imports """
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.abstract.viewsets import AbstractViewSet
from apps.auth.permissions import UserPermission
from apps.element.serializers import ElementSerializer
from apps.element.models import Element, LETTERS, ELEMENT_TYPE



""" Element viewset """
class ElementViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = ElementSerializer  
    
    def get_queryset(self):        
        queryset = Element.objects.all()    
        elemento = self.request.query_params.get('type')
        letter = self.request.query_params.get('letter')                        
                        
        if elemento is not None and int(elemento) > 0:
            queryset = queryset.filter(element_type=elemento)
            
        if letter is not None and int(letter) > 0:
            queryset = queryset.filter(letter=letter)                
                
        return queryset.order_by('element_type', 'letter', 'name')
        
    
    def get_object(self):                        
        obj = Element.objects.get(id=self.kwargs['pk'])        
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    
    # Create is the viewset action excecuted on POST requests on the endpoint linked to viewset
    def create(self, request, *args, **kwargs):        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    # Delete the element
    def destroy(self, request, *args, **kwargs):        
        obj = Element.objects.get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        obj_json = {"name":obj.name}
        return Response(obj_json, status=status.HTTP_200_OK)
        
    
    # Update
    def update(self, request, *args, **kwargs):
        instance = Element.objects.get(id=self.kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data)                        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def get_choices(self, request):        
        letters = {}                
        type = {}
        
        for tup in LETTERS:                        
            letters[tup[0]] = tup[1]
            
        for tup in ELEMENT_TYPE:
            type[tup[0]] = tup[1]
                                    
        return Response({
                'letters':letters,
                'type':type
            })
        
                
    




