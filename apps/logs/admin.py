# Imports
from django.contrib import admin
from apps.logs.models import Logs


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'location_country', 'location_city', 'created', 'updated')