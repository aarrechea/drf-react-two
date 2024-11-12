""" Imports """
from rest_framework import viewsets, filters



""" Abstract viewset """
class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter] # setting the default filter backend
    #ordering_fields = ['updated', 'created'] # ordering parameters when making a request
    #ordering = ['-updated'] # tells django in which order to send many objects as a response



