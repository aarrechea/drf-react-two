""" Imports """
from rest_framework.permissions import BasePermission, SAFE_METHODS



""" User permission class """
class UserPermission(BasePermission):            
    basenameArray = ['element', 'relations', 'relations_tree', 'company', 'countries', 'industry', 'evaluations',
                    'data-model', 'region', 'continent', 'supersector', 'sector', 'subsector']
            
    # works in the object level
    def has_object_permission(self, request, view, obj):        
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS # get, options, and head
                
        if view.basename in self.basenameArray:
            # Any user that has permission could view the element
            if request.method == 'GET':
                return True
            
            # if the user did not create the object, it does not have access to it
            if view.basename == 'evaluations':
                if obj.creator_user.id != request.user.id:
                    return False
            else:                    
                if obj.user_creator.id != request.user.id:
                    return False                        
            
            return bool(request.user and request.user.is_authenticated)
        
        return False
    
    
    # works in the overall endpoint
    def has_permission(self, request, view):                
        if view.basename in self.basenameArray:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)
        
        return False
            



