# Imports
from django.contrib import admin
from apps.user.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'created', 
        'updated', 
        'email',
        'first_name',
        'last_name',
        'eva_closed',
        'eva_in_progress',
        'user_type',
        'photo',
        'is_staff',
        'is_active',
        'is_superuser',
    )
