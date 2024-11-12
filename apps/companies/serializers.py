""" Imports """
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.companies.models import Company
from apps.countries.models import Country
from apps.countries.serializers import CountrySerializer
from apps.industries.models import Industry
from apps.supersectors.models import Supersector
from apps.supersectors.serializers import SupersectorSerializer
from apps.sectors.models import Sector
from apps.sectors.serializers import SectorSerializer
from apps.subsectors.models import Subsector
from apps.subsectors.serializers import SubsectorSerializer
from apps.industries.serializers import IndustrySerializer



""" Company serializer """
class CompanySerializer(AbstractSerializer):
    #user_creator = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')    
    country_display = serializers.CharField(required=False)
    subsector_display = serializers.CharField(required=False)
    sector_display = serializers.CharField(required=False)
    sector_id = serializers.IntegerField(required=False)
    supersector_display = serializers.CharField(required=False)
    supersector_id = serializers.IntegerField(required=False)
    industry_display = serializers.CharField(required=False)
    industry_id = serializers.IntegerField(required=False)
    continent_display = serializers.CharField(required=False)
    region_display = serializers.CharField(required=False)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Country
        country = Country.objects.get(id=rep['country'])                        
        rep['country_display'] = country.name
        
        #Subsector
        subsector = Subsector.objects.get(id=rep['subsector'])        
        subsector = SubsectorSerializer(subsector).data                        
        rep['subsector_display'] = subsector['name']
        
        # Sector
        sector = Sector.objects.get(id=subsector['sector'])
        sector = SectorSerializer(sector).data        
        rep['sector_display'] = sector['name']
        rep['sector_id'] = sector['id']
        
        # Supersector
        supersector = Supersector.objects.get(id=sector['supersector'])
        supersector = SupersectorSerializer(supersector).data
        rep['supersector_display'] = supersector['name']
        rep['supersector_id'] = supersector['id']
        
        # Industry
        industry = Industry.objects.get(id=supersector['industry'])
        industry = IndustrySerializer(industry).data
        rep['industry_display'] = industry['name']
        rep['industry_id'] = industry['id']
        
        # Continent and region        
        country = Country.objects.get(id=rep['country'])
        country = CountrySerializer(country).data
        rep['continent_display'] = country['continent']
        rep['region_display'] = country['region']
                        
        return rep
        
    
    
    def validate_user_creator(self, value):        
        if self.context['request'].user != value:
            raise ValidationError("You can not create an element")
        
        return value
    
    class Meta:
        model = Company
        fields = ['id', 'user_creator', 'name', 'address', 'postal_code', 'country', 
                'city', 'year_establishment', 'year_first_expo', 'business_description',
                'subsector', 'comments', 'eva_made', 'eva_progress', 'created', 'updated',
                'country_display', 'subsector_display', 'sector_display', 
                'supersector_display', 'industry_display', 'continent_display', 'region_display',
                'industry_id', 'supersector_id', 'sector_id']