""" Imports """
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.abstract.viewsets import AbstractViewSet
from apps.auth.permissions import UserPermission
from apps.element.models import Element
from apps.evaluations.serializers import EvaluationScoreSerializer
from apps.relations.serializers import RelationSerializer
from apps.relations.models import Relation
from apps.relations_tree.viewsets import RelationTreeViewSet




""" Relations viewset """
class RelationViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = RelationSerializer
            
            
    def get_queryset(self):
        queryset = Relation.objects.all()                                
        return queryset
    
    
    def perform_create(self, serializer):                        
        new_object = serializer.save()
        
        return new_object
    
    
    # Create is the viewset action excecuted on POST requests on the endpoint linked to viewset    
    def create(self, request, *args, **kwargs):
        newData = fcnPrepareData(request)        
        serializer = self.get_serializer(data=newData)                
                
        if serializer.is_valid():
            with transaction.atomic():                
                newObject = self.perform_create(serializer)                
                #errorsTree = create_relation_tree(request.data[0]['table'], newObject.id, self)
                
                # newObject is the new Relation created. Table is the new table of the relations
                # created in the front end.
                kwargs = {'table':request.data[0]['table'], 'newRelation':newObject.id}
                RelationTreeViewSet.create(self, request, kwargs)
                
                # to send the id of the new relation created to change the mode from create to edit
                newElement = Relation.objects.all().order_by('-id')[:1].values()
                                                
                return Response(newElement[0], status=status.HTTP_201_CREATED)
        
        elif serializer.errors:                                    
            return Response({'error':serializer.errors['name'][0]})        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)        
    
        
    # Update method override    
    def update(self, request, *args, **kwargs):        
        newData = fcnPrepareData(request)
                
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=newData)
        
        if serializer.is_valid():
            with transaction.atomic():
                self.perform_update(serializer)
            
                RelationTreeViewSet.update_relation_tree(self, request.data[0]['table'], instance)
            
                return Response({'status':'ok', 'serializer':serializer.data}, status=status.HTTP_200_OK)
            
        elif serializer.errors:            
            return Response({'error':serializer.errors['name'][0]})
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
        
    # Delete the relation
    def destroy(self, request, *args, **kwargs):        
        obj = Relation.objects.get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)    
        
        queryset = self.get_queryset()
                
        return Response(queryset.values(), status=status.HTTP_200_OK)
    
        


""" Count competences, capabilities, and processes in the relation tree """
def fcnCountElements(table):
    elements = []
    processes = 0
    capabilities = 0
    competences = 0
    
    for element in table:
        match int(element['element_type']):
            case 1:
                competences += 1
            case 2:
                capabilities += 1
            case 3:
                processes += 1 
        
    elements.append(competences)
    elements.append(capabilities)
    elements.append(processes)
        
    return elements


""" Function to prepare data to create or update the relation. Data will be pulled from request """
def fcnPrepareData(request):
    total_elements = len(request.data[0]['table'])
    count_elements = fcnCountElements(request.data[0]['table'])    
    
    newData = {
        "name": request.data[1]['name'], 
        "user_creator": request.data[3]['userId'],
        "status": request.data[2]['open'],
        "total_elements": total_elements,
        "competences": count_elements[0],
        "capabilities": count_elements[1],
        "processes": count_elements[2],
    }   
    
    return newData




