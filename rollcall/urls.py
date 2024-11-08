from django.urls import path
from . import views

appname= 'rollcall'

urlpatterns = [
    path('management', views.Management.as_view(), name='management'),
    path('management_Human', views.Management_Human.as_view(), name='management_Human'),
    path('management_Drive', views.management_Drive.as_view(), name='management_Drive'),
]