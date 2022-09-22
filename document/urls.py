from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('company', views.CompanyDocumentList.as_view(), name='company'),
    path('dispatch', views.DocumentList.as_view(), name="dispatch"),
]