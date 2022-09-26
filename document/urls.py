from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('company', views.CompanyDocumentList.as_view(), name='company'),
    path('dispatch', views.DocumentList.as_view(), name="dispatch"),
    
    path('print/vehicle', views.vehicle_print, name="vehicle_print"),
    path('print/commitment', views.commitment_print, name="commitment_print"),
    path('print/safety', views.safety_print, name="safety_print"),
    path('print/school', views.school_print, name="school_print"),
    path('print/drinking', views.drinking_print, name="drinking_print"),
]