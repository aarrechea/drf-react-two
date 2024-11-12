""" Imports """
from django.contrib import admin
from django.urls import path, include



""" Patterns """
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(("apps.routers", "apps"), namespace="apps-api")),
]
