from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.urls import reverse

def home(request):
    return render(request, 'dispatch/home.html')

def order(request):
    return render(request, 'dispatch/order.html')
def order_create(request):
    return render(request, 'dispatch/order_create.html')
def order_detail(request, order_id):
    return render(request, 'dispatch/order_detail.html')
def order_edit(request, order_id):
    return render(request, 'dispatch/order_edit.html')
def order_delete(request, order_id):
    return render(request, 'dispatch/order_edit.html')

def schedule(request):
    return render(request, 'dispatch/schedule.html')

def management(request):
    return render(request, 'dispatch/management.html')
def management_detail(request, order_id):
    return render(request, 'dispatch/management_detail.html')
def management_create(request, order_id):
    return render(request, 'dispatch/management_create.html')
def management_edit(request, order_id):
    return render(request, 'dispatch/management_edit.html')