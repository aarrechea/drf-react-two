""" Imports """
from apps.abstract.serializers import AbstractSerializer
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.element.models import Element
from apps.evaluations.models import Evaluation, DataModel, EvaluationScore, MainProducts, EvaluationCapabilityScore
from apps.relations.models import Relation
from apps.relations.serializers import RelationSerializer
from apps.user.models import User
from apps.user.serializers import UserSerializer



""" Evaluation serializer """
class EvaluationsSerializer(AbstractSerializer):    
    def to_representation(self, instance):
        rep = super().to_representation(instance)                
        
        relation = Relation.objects.get(id=rep['relation'])
        company = Company.objects.get(id=rep['company'])
        
        relation_serialized = RelationSerializer(relation).data
        company_serialized = CompanySerializer(company).data
        
        user = User.objects.get(id=rep['creator_user'])                
        
        rep['company_display'] = relation_serialized['name']
        rep['total_processes'] = relation_serialized['processes']
        rep['relation_display'] = company_serialized['name']
        rep['user_display'] = UserSerializer(user).data # user object
        
        return rep
            
    class Meta:
        model = Evaluation
        fields = ['creator_user', 'id', 'end_user', 'processes_evaluated', 'finalized', 'score',                
                'relation', 'company']
        
        
        
""" Data model serializer """        
class DataModelSerializer(AbstractSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
                
        products = MainProducts.objects.filter(evaluation=rep['evaluation'])                
        if len(products) > 0:
            rep['products'] = MainProductsSerializer(products).data
        else:
            rep['products'] = []
        
        return rep
            
    class Meta:
        model = DataModel
        fields = ['id', 'years_exporting', 'plans_to_export', 'export_variation', 'foreign_investment',
                'average_years', 'top_or_middle', 'women_employed', 'women_top_or_middle',
                'ceo_title', 'given_name', 'family_name', 'gender', 'telephone', 'email',
                'business_position', 'years_in_the_post', 'comments', 'evaluation']
        



""" Main products serializer """
class MainProductsSerializer(AbstractSerializer):
    class Meta:
        model = MainProducts
        fields = ('__all__')

        
        
""" Evaluation score serializer """        
class EvaluationScoreSerializer(AbstractSerializer):
    def to_representation(self, instance):        
        rep = super().to_representation(instance)                
        element = Element.objects.get(id=rep['element'])
        rep['element_type'] = element.element_type
        rep['element_name_display'] = element.name
        
        return rep
        
        
    class Meta:
        model = EvaluationScore
        fields = ['id', 'first_score', 'form_number', 'order', 'element', 'evaluation', 'relation_tree', 
                'final_score', 'percentage_score', 'element_type']
                                


""" Evaluation capability score serializer """
class EvaluationCapabilityScoreSerializer(AbstractSerializer):
    class Meta:
        model = EvaluationCapabilityScore
        fields = ['id', 'competence', 'capability', 'evaluation', 'score']
