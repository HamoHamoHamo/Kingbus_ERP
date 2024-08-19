from django.urls import path
from . import views

appname= 'education'

urlpatterns = [
    path('', views.Educational.as_view(), name='educational'),
    path('manager', views.Educational_Manager.as_view(), name='educational_manager'),
    path('completionstatus', views.CompletionStatus.as_view(), name='completionstatus'),
    path('educational_create', views.Educational_Create.as_view(), name="educational_create"),
]