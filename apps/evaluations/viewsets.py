from django.db import transaction
from django.db.models import Sum, F, Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.abstract.viewsets import AbstractViewSet
from apps.auth.permissions import UserPermission
from apps.companies.models import Company
from apps.evaluations.models import (Evaluation, DataModel, EvaluationScore, 
    EvaluationCompetenceScore, EvaluationCapabilityScore)
from apps.evaluations.serializers import EvaluationsSerializer, EvaluationScoreSerializer, DataModelSerializer
from apps.relations.models import Relation
from apps.relations_tree.models import RelationTree



""" Evaluations viewset """
class EvaluationsViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = EvaluationsSerializer  
    queryset = Evaluation.objects.all()


    # Create is the viewset action excecuted on POST requests on the endpoint linked to viewset
    def create(self, request, *args, **kwargs):        
        try:
            with transaction.atomic():                                
                company = Company.objects.get(id=request.data['company'])
                company.eva_progress += 1
                company.save()
                
                relation = Relation.objects.get(id=request.data['relation'])
                relation.eva_progress += 1
                relation.save()
                
                
                # Creating the evaluation    
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)        
                self.perform_create(serializer)
                
                """ Get the last evaluation id created to create de data model row """
                maxId = Evaluation.objects.all().order_by('-id')[:1]
                DataModel.objects.create(evaluation=maxId[0])
                
                """ Create the evaluation score table calling RelationTree first to know the elements involved """
                maxId_serialized = EvaluationsSerializer(maxId[0]).data
                relation_tree = RelationTree.objects.filter(relation=maxId_serialized['relation']).order_by('order')
                #relation_tree = RelationTree.objects.select_for_update().filter(relation=maxId_serialized['relation']).order_by('order')
                
                array = []
                for item in relation_tree:            
                    item.element.eva_progress += 1                                    
                    item.element.save()
                    
                    evaluation_score = EvaluationScore(
                        element = item.element,
                        form_number = item.order,
                        order = item.order,
                        evaluation = maxId[0],
                        relation_tree = item,
                        element_type = item.element.element_type
                    )
                    array.append(evaluation_score)                    
                        
                EvaluationScore.objects.bulk_create(array)
                                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Error":"Error creating the evaluation", "Exception": e})
    
    
    # Delete the evaluation
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                obj = Evaluation.objects.get(id=self.kwargs['pk'])
                self.check_object_permissions(self.request, obj)
                                                
                company = Company.objects.get(id=obj.company.id)                
                company.eva_progress -= 1
                                
                relation = Relation.objects.get(id=obj.relation.id)
                relation.eva_progress -= 1
                                
                rel_tree = obj.relation.relation_tree.all()

                self.perform_destroy(obj)
                company.save()
                relation.save()
                
                # update each item in the relation tree
                for item in rel_tree:                    
                    item.element.eva_progress -= 1
                    item.element.save()
                
                return Response({'result':'success'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"Error":"Error deleting the evaluation", "Exception": e})
    
    
    # To get the evaluation score, and adding the field element_type through to_rep in the serializer
    @action(methods=['get'], detail=True, permission_classes=[UserPermission])
    def getRelation(self, request, pk=None):        
        eva_score = EvaluationScore.objects.filter(evaluation=pk).order_by('order')
        serializer = EvaluationScoreSerializer(data=eva_score, many=True)        
        serializer.is_valid()
        
        return JsonResponse(serializer.data, safe=False)
    
    
    
    # To get the evaluation score related a relation tree
    @action(methods=['get'], detail=True, permission_classes=[UserPermission])
    def getEvaluationScore(self, request, pk=None):        
        eva_scores = list(EvaluationScore.objects.filter(evaluation=pk).order_by('form_number').values())        
        return Response(eva_scores)
    
    
    # Update the score
    @action(methods=['put'], detail=True, permission_classes=[UserPermission])
    def updateScore(self, request, pk=None):        
        eva_score = EvaluationScore.objects.filter(evaluation=pk).get(element=request.data['id_element'])        
        eva_score.first_score = request.data['newScore']
        eva_score.save()
        
        serializer = self.getEvaluationScore(request, pk)
        
        # Update the number of elements evaluated, to put the count in the evaluations table.
        total_evaluated = EvaluationScore.objects.filter(evaluation=pk, first_score__gt=0).aggregate(total_evaluated=Count('first_score'))
        actual_eva = Evaluation.objects.get(id=pk)
        actual_eva.processes_evaluated = total_evaluated['total_evaluated']
        actual_eva.save()
                
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    #---------------------------------------------------------------------
    # Finalize the evaluation
    #---------------------------------------------------------------------
    @action(methods=['post'], detail=True, permission_classes=[UserPermission])
    def finalizeEvaluation(self, request, pk=None):        
        # First step is to translate the first score to a final score for each process.
        # The element that are not processess will hold a value of -0.25.
        eva_score = EvaluationScore.objects.filter(evaluation=pk)
        for element in eva_score:            
            if element.first_score > 0:
                element.final_score = (element.first_score - 1) * 0.25
                element.save()
                
        eva_relation_tree = calculate_percentage_score(eva_score)        
        
        calculate_capability_score(eva_relation_tree, pk)                
        calculate_competence_score(pk)        
        calculate_final_score(pk)        
        implement_element_finalized_count(eva_relation_tree)
        
        # Change the value of the finilezed evaluation in Relation and in Company
        relation = Evaluation.objects.get(id=pk).relation                
        relation.eva_made += 1
        relation.eva_progress -= 1
        relation.save()
        
        company = Evaluation.objects.get(id=pk).company
        company.eva_made += 1
        company.eva_progress -= 1
        company.save()
        
        return Response({'Response':'Ok'}, status=status.HTTP_200_OK)



# Calculate percentage score
def calculate_percentage_score(eva_score):    
    eva_relation_tree = eva_score.select_related("relation_tree")
    
    for element in eva_relation_tree:        
        element.percentage_score = element.final_score * element.relation_tree.percentage
        element.save()
        
    return eva_relation_tree
        
        
# Capability score
def calculate_capability_score(eva_relation_tree, pk):
    # array to save the EvaluationCapabilityScore objects
    array = []
        
    # Filter an join tables to calculate the final score, which is the sum of the process percentages
    new_queryset = (eva_relation_tree
        .filter(relation_tree__related_capability__gt=0)
        .values('evaluation', 'relation_tree__related_competence', 'relation_tree__related_capability')
        .annotate(capability_score=Sum(F('final_score') * F('percentage_score') / 100))        
    )    
                
    for element in new_queryset:                
        evaluation = Evaluation.objects.get(id=element['evaluation'])                
                
        new_cap = EvaluationCapabilityScore(
                evaluation= evaluation,
                competence= element['relation_tree__related_competence'],
                capability= element['relation_tree__related_capability'],
                score= element['capability_score']
            )
        
        array.append(new_cap)
        
    EvaluationCapabilityScore.objects.bulk_create(array)
    
    # Count numbers of competences to calculate the score of the capabilities
    evaluation_capabilities = EvaluationCapabilityScore.objects.filter(evaluation=pk)
    
    count_competences = (evaluation_capabilities
                            .values('competence')
                            .annotate(count=Count('competence'))
                        )
    
    # Put the values that represent the weight of each competence in each group of capabilities.
    for line in evaluation_capabilities:
        for element in count_competences:            
            if int(line.competence) == int(element['competence']):                
                line.competence_weight = 1 / element['count']
                line.save()                    

    return 1



""" -----------------------------------------------------------------
Calculate the competences score from the numbers in the competence score table
----------------------------------------------------------------- """
def calculate_competence_score(pk):
    capability_score = EvaluationCapabilityScore.objects.filter(evaluation=pk)
    
    # array to save the EvaluationCapabilityScore objects
    array = []
        
    # Filter an join tables to calculate the final score, which is the sum of the process percentages
    new_queryset = (capability_score        
        .values('evaluation', 'competence')        
        .annotate(competence_score=Sum(F('score') * F('competence_weight')))
    )
    
    for element in new_queryset:                
        evaluation = Evaluation.objects.get(id=element['evaluation'])
                
        new_comp = EvaluationCompetenceScore(
                evaluation= evaluation,
                competence= element['competence'],                
                score= element['competence_score']
            )
        
        array.append(new_comp)
        
    EvaluationCompetenceScore.objects.bulk_create(array)
    
    return Response(status=status.HTTP_200_OK)


""" ----------------------------------------------------------------------
Calculate the final score, and put the finalized field in True
---------------------------------------------------------------------- """
def calculate_final_score(pk):
    competence_data = EvaluationCompetenceScore.objects.filter(evaluation=pk)
    evaluation = Evaluation.objects.get(id=pk)
    
    # Queryset that contains the final score of the evaluation.
    final_score = (competence_data
                .values('evaluation')
                .annotate(score=Sum('score') / Count('score'))
            )
        
    print("\nevaluation in calculate final score: ", evaluation)
    print("final score: ", final_score)
        
    evaluation.score = final_score[0]['score']
    evaluation.finalized = True
    evaluation.save()
        
    return final_score


""" ----------------------------------------------------------------------
Implement finalized count, and substract in progress count.
---------------------------------------------------------------------- """
def implement_element_finalized_count(eva_relation_tree):        
    for element in eva_relation_tree:
        element.element.eva_progress -= 1
        element.element.eva_made += 1
        element.element.save()
    
    return 1




""" Data model viewset """
class DataModelViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = DataModelSerializer  
    queryset = DataModel.objects.all()
    
    
    def get_object(self):        
        evaluation = Evaluation.objects.get(id=self.kwargs['pk'])
        
        if evaluation.finalized == True:
            raise Exception("The evaluation is finalized", status=status.HTTP_400_BAD_REQUEST)
        else:        
            obj = DataModel.objects.get(evaluation=self.kwargs['pk'])                        
            return obj
        
        
    def update(self, request, *args, **kwargs):        
        obj = DataModel.objects.get(id=self.kwargs['pk'])
        
        serializer = self.serializer_class(obj, data=request.data)        
        serializer.is_valid()        
        serializer.save()
        
        return Response({'updated':'updated'})
    


""" Evaluations scores viewset """
class EvaluationScoreViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = EvaluationScoreSerializer
    queryset = EvaluationScore.objects.all()
