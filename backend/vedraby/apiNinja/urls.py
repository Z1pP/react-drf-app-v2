from django.urls import path
from .handlers import api

urlpatterns = [path("", api.urls)]
