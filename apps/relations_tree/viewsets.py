""" Imports """
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.abstract.viewsets import AbstractViewSet
from apps.auth.permissions import UserPermission
from apps.element.models import Element
from apps.evaluations.serializers import EvaluationScoreSerializer
from apps.relations.models import Relation
from apps.relations_tree.serializers import RelationTreeSerializer
from apps.relations_tree.models import RelationTree



""" Relations tree viewset """
class RelationTreeViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = RelationTreeSerializer
    
    def get_queryset(self):        
        idRelation = self.request.query_params.get('idRel')        
        queryset = RelationTree.objects.filter(relation=idRelation)                
        return queryset            
    
    
    
    @action(methods=['get'], detail=False, permission_classes=[UserPermission])
    def get_queryset_filtered(self, request):
        newObject = []                                    
        
        relation = Relation.objects.get(id=self.request.query_params.get('id'))        
        relation_name = relation.name     
        
        try:
            eva_scores_to_send = list(relation.evaluation.all()[0].evaScore.all().order_by('form_number').values())
                                    
        except:
            eva_scores_to_send = {}
            
            
        obj = relation.relation_tree.all().order_by('order').values()        
        obj_list = list(obj)
                
        for object in obj_list:            
            element = Element.objects.get(id=object['element_id'])
            
            newObject.append({
                'order': object['order'],
                'capability_number': object['capability_number'],
                'process_number': object['process_number'],
                'percentage': object['percentage'],
                'element_type': int(object['element_type']),
                'relation_letter': object['relation_letter'],
                'relation_letter_display': object['relation_letter_display'],
                'element': element.id,
                'relation': relation.id,
                'name':element.name,
                'elementObject':element,                
            })

        serializer = self.get_serializer(data=newObject, many=True)        
        serializer.is_valid(raise_exception=True)                
        self.check_object_permissions(self.request, obj)
        
        response = {
            'data':serializer.data,
            'relation_name':relation_name,
            'eva_scores': eva_scores_to_send
        }
                                
        return Response(response)
    

    def perform_create(self, serializer):                        
        new_object = serializer.save()        
        return new_object
    

    """ Function to create the relation tree related to the relation created before. """
    #def create(table, id, self, request):
    def create(self, request, kwargs):
        newObject = []                
        
        table = kwargs['table']
        id = kwargs['newRelation']
                
        relation = Relation.objects.get(id=id)                
                        
        for object in table:            
            element = Element.objects.get(id=object['id'])
            
            print("element: ", element)
            
            if int(element.element_type) == 1:
                related_competence = element.id
                related_capability = 0            
            elif int(element.element_type) == 2:
                related_capability = element.id
                                
            newObject.append({                                
                'order': object['order'],
                'capability_number': object['capability_number'],
                'process_number': object['process_number'],
                'percentage': object['percentage'],
                'element_type': int(object['element_type']),
                'relation_letter': object['letter'],
                'relation_letter_display': object['letter_display'],
                'element': element.id,
                'relation': relation.id,
                'related_competence':related_competence,
                'related_capability':related_capability                
            })
            
        print("new object: ", newObject)
                                    
        serializer = RelationTreeSerializer(data=newObject, many=True)        
        serializer.is_valid(raise_exception=True)                                
        self.perform_create(serializer)
        
        return serializer
    
    
    """ Function to update the relation tree after to update the relation """    
    def update_relation_tree(self, table, instance):
        newObject = []        
        
        for object in table:                
            element = Element.objects.get(id=object['element'])
                
            newObject.append({                                
                'order': object['order'],
                'capability_number': object['capability_number'],
                'process_number': object['process_number'],
                'percentage': object['percentage'],
                'element_type': int(object['element_type']),
                'relation_letter': object['relation_letter'],
                'relation_letter_display': object['relation_letter_display'],
                'element': element.id,
                'relation': instance.id
            })
        
        RelationTree.objects.filter(relation=instance.id).delete()
                            
        serializer = RelationTreeSerializer(data=newObject, many=True)
        serializer.is_valid(raise_exception=True)        
        self.perform_create(serializer)
        
        return serializer


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




