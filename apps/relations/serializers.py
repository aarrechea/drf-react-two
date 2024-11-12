""" Imports """
from rest_framework.exceptions import ValidationError
from apps.relations.models import Relation
from apps.abstract.serializers import AbstractSerializer



""" Relation serializer """
class RelationSerializer(AbstractSerializer):
    #user_creator = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    
    def validate_user_creator(self, value):        
        if self.context['request'].user != value:
            raise ValidationError("You can not create an element")
        
        return value        
    
    class Meta:
        model = Relation
        fields = ['name', 'total_elements', 'competences', 'capabilities', 'processes', 'eva_made',
                'eva_progress', 'comments', 'status', 'user_creator', 'id']
        
        
        


