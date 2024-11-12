""" Imports """
from decimal import Decimal
from rest_framework import serializers
from apps.relations_tree.models import RelationTree
from apps.abstract.serializers import AbstractSerializer
from apps.element.models import Element
from apps.element.serializers import ElementSerializer

        
        
""" Relation tree serializer """        
class RelationTreeSerializer(AbstractSerializer):
    name = serializers.SerializerMethodField()    
    
    def to_representation(self, instance):                        
        rep = super().to_representation(instance)                
        element_object = Element.objects.get(id=rep['element'])        
        rep['element_object'] = ElementSerializer(element_object).data
        
        return rep
    
                
                
    def validate_user_creator(self, value):                
        return value
                
                
                
    def validate_percentage(self, value):                
        try:
            percentage = Decimal(value)
            return percentage
        except:
            return False
    
    
    
    # To match the new serializer method field that is not present in the original model.
    def get_name(self, obj):                
        try:            
            return obj.element.name
        except:                    
            return obj['element'].name
    
    
        
    class Meta:
        model = RelationTree
        fields = ['order', 'capability_number', 'process_number', 'percentage', 'element_type', 'id',
                'relation_letter', 'relation_letter_display', 'element', 'relation', 'name',
                'related_competence', 'related_capability']
        
        

            


