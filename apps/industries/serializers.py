""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.industries.models import Industry
from apps.supersectors.models import Supersector
from apps.supersectors.serializers import SupersectorSerializer
from apps.sectors.models import Sector
from apps.sectors.serializers import SectorSerializer
from apps.subsectors.models import Subsector
from apps.subsectors.serializers import SubsectorSerializer



""" Industry serializer """
class IndustrySerializer(AbstractSerializer):
    def to_representation(self, instance):        
        rep = super().to_representation(instance)
        
        # Supersector
        supersector = Supersector.objects.filter(industry=rep['id'])
        sup_serialized = SupersectorSerializer(supersector, many=True).data
        rep['supersector'] = sup_serialized
        
        # Sector
        lst_sector = []
        for item in supersector:
            lst_sector.append(item.id)
                
        sector = Sector.objects.filter(supersector__in=lst_sector)        
        sector_serialized = SectorSerializer(sector, many=True).data
        rep['sector'] = sector_serialized
        
        # Subsector
        lst_subsector = []
        for item in sector:
            lst_subsector.append(item.id)
        
        subsector = Subsector.objects.filter(sector__in=lst_subsector)
        subsector_serialized = SubsectorSerializer(subsector, many=True).data
        rep['subsector'] = subsector_serialized
        
        
        return rep
        
                
    class Meta:
        model = Industry
        fields = '__all__'
        
                    