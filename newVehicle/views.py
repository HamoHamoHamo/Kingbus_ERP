from django.shortcuts import render
from django.views import generic



# Create your views here.
def vehicle_view(request):
    return render(request, 'newVehicle/vehicle.html')