from django.urls import path
from . import views

appname= 'rollcall'

urlpatterns = [
    path('management', views.Management.as_view(), name='management'),
]