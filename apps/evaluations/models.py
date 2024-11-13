""" Imports """
from django.db import models
from apps.abstract.models import AbstractModel
from apps.companies.models import Company
from apps.element.models import Element
from apps.relations.models import Relation
from apps.relations_tree.models import RelationTree
from apps.user.models import User



""" Evaluation model """
class Evaluation(AbstractModel):
    end_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='end_user', blank=True, null=True)
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_user')
    processes_evaluated = models.IntegerField(default=0)   
    finalized = models.BooleanField(default=0) # if it is open or already close
    score = models.DecimalField(default=0, max_digits=5, decimal_places=2) # final score   
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE, related_name='evaluation')
    
    class Meta:
        ordering = ('company', 'relation')
        
        
        
""" Data model for the first step in the evaluation """        
class DataModel(models.Model):
    years_exporting = models.IntegerField(default=0)
    plans_to_export = models.BooleanField(default=0)
    export_variation = models.IntegerField(default=0)
    foreign_investment = models.BooleanField(default=0)
    average_years = models.IntegerField(default=0)
    top_or_middle = models.IntegerField(default=0)
    women_employed = models.IntegerField(default=0)
    women_top_or_middle = models.IntegerField(default=0)
    ceo_title = models.SmallIntegerField(default=1)
    given_name = models.CharField(max_length=100, default='Empty')
    family_name = models.CharField(max_length=100, default='Empty')
    gender = models.SmallIntegerField(default=1)
    telephone = models.CharField(max_length=20, default='Empty')
    email = models.CharField(max_length=100, default='Empty')
    business_position = models.CharField(max_length=100, default='Empty')
    years_in_the_post = models.IntegerField(default=0)
    comments = models.TextField(max_length=255, default='Empty')
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
        


""" Main products of the company and their impact on sales """
class MainProducts(models.Model):
    product = models.CharField(max_length=30)
    percentage = models.IntegerField(default=0)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    
    
    
""" Element score save the information related to each element of the relation with 
    its respective score calculated.
"""    
class EvaluationScore(models.Model):
    first_score = models.IntegerField(default=0) # original score
    form_number = models.IntegerField(default=0)
    order = models.SmallIntegerField(default=0)
    element_type = models.IntegerField(default=0)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='element_related')
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='evaScore')
    relation_tree = models.ForeignKey(RelationTree, on_delete=models.CASCADE, related_name='relation_tree_related')
    final_score = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    
    # percetage representation of the original score
    percentage_score = models.DecimalField(default=0, max_digits=5, decimal_places=2)    
    
    

class EvaluationCapabilityScore(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='related_capability')
    competence = models.IntegerField()
    capability = models.IntegerField()
    score = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    competence_weight = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    
    
    
class EvaluationCompetenceScore(AbstractModel):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='related_competence')
    competence = models.IntegerField()    
    score = models.DecimalField(default=0, max_digits=5, decimal_places=2)
