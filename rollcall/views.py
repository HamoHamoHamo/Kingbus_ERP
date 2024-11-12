from django.shortcuts import render
from django.views import generic
from humanresource.models import Member


# Create your views here.
def Management(request):
    return render(request, 'rollcall/management.html')