from django.urls import path
from . import views

appname= 'newAccounting'

urlpatterns = [
    path('equivalentefficiency', views.EquivalentEfficiency.as_view(), name='equivalentefficiency'),
]