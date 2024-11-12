""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.element.models import Element
from apps.user.models import User
from apps.user.serializers import UserSerializer



""" Element serializer """
class ElementSerializer(AbstractSerializer):
    #user_creator = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    letter_display = serializers.CharField(source='get_letter_display', required=False)
    element_type_display = serializers.CharField(source='get_element_type_display', required=False)    
    
    
    def validate_user_creator(self, value):        
        #print("validate user creator - value: ", value)                        
        return value
    
    
    def to_representation(self, instance):                        
        rep = super().to_representation(instance)        
        user = User.objects.get(id=rep['user_creator'])
        rep['user'] = UserSerializer(user).data
        
        return rep

    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        return instance
    
    
    class Meta:
        model = Element
        fields = ['user_creator', 'id', 'element_type', 'letter', 'name', 'comments', 'eva_progress', 'eva_made',
                'definitions', 'symptoms', 'questions', 'assess_one', 'assess_two', 'assess_three',
                'assess_four', 'assess_five', 'letter_display', 'element_type_display']
    


