from django.urls import path
from . import views

app_name = 'newVehicle'

urlpatterns = [
    path('', views.vehicle_view)
]
