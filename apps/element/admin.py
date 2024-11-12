# Imports
from django.contrib import admin
from apps.element.models import Element


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_creator',
        'element_type',
        'letter',
        'name',
        'comments',
        'eva_progress',
        'eva_made',
        'definitions',
        'symptoms',
        'questions',
        'assess_one',
        'assess_two',
        'assess_three',
        'assess_four',
        'assess_five',
        'created',
        'updated'
    )