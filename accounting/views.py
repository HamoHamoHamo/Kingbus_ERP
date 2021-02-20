from crudmember.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Salary, Outlay, Collect, Income

#지출
class OutlayList(generic.ListView):
    temeplate_name = 'accounting/outlay_list.html'
    context_object_name = 'outlay_list'
    model = Outlay

def outlay_create(request):

    return render(request, 'accounting/outlay_create.html')

class OutlayDetail(generic.DetailView):
    temeplate_name = 'accounting/outlay_detail.html'
    context_object_name = 'outlay'
    model = Outlay

def outlay_delete(request, pk):
    return render(request, 'accounting/outlay_detail.html')

def outlay_edit(request, pk):
    return render(request, 'accounting/outlay_edit.html')

#급여
class SalaryList(generic.ListView):
    temeplate_name = 'accounting/salary_list.html'
    context_object_name = 'salary_list'
    model = Salary

def salary_create(request):

    return render(request, 'accounting/salary_create.html')

class SalaryDetail(generic.DetailView):
    temeplate_name = 'accounting/salary_detail.html'
    context_object_name = 'salary'
    model = Salary

def salary_delete(request, pk):

    return render(request, 'accounting/salary_detail.html')

def salary_edit(request, pk):

    return render(request, 'accounting/salary_edit.html')

#수입
class IncomeList(generic.ListView):
    temeplate_name = 'accounting/income_list.html'
    context_object_name = 'income_list'
    model = Income

def income_create(request):

    return render(request, 'accounting/income_create.html')

class IncomeDetail(generic.DetailView):
    temeplate_name = 'accounting/income_detail.html'
    context_object_name = 'income'
    model = Income

def income_delete(request, pk):

    return render(request, 'accounting/income_detail.html')

def income_edit(request, pk):

    return render(request, 'accounting/income_edit.html')

#수금
class CollectList(generic.ListView):
    temeplate_name = 'accounting/collect_list.html'
    context_object_name = 'collect_list'
    model = Collect

class CollectDetail(generic.DetailView):
    temeplate_name = 'accounting/collect_detail.html'
    context_object_name = 'collect'
    model = Collect

def collect_edit(request, pk):

    return render(request, 'accounting/collect_edit.html')