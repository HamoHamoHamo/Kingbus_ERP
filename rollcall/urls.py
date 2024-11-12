from django.urls import path
from . import views

appname= 'rollcall'

urlpatterns = [
    path('management', views.Management, name='management'),
]