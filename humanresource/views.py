from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Member, MemberDocument, HR
from .forms import MemberForm, HRForm
from crudmember.models import User


class ManageMemberList(generic.ListView):
    template_name = 'HR/management_list.html'
    context_object_name = 'HR_list'
    model = HR

def HR_create(request):
    return render(request, 'HR/HR_create.html')

def HR_edit(request, pk):
    return render(request, 'HR/HR_edit.html')

def HR_delete(request, pk):
    return render(request, 'HR/HR_create.html')

class MemberDetail(generic.DetailView):
    template_name = 'HR/member_detail.html'
    context_object_name = 'member'
    model = Member

def member_create(request):
    return render(request, 'HR/member_create.html')

def member_edit(request, pk):
    return render(request, 'HR/member_edit.html')

def member_delete(request, pk):
    return render(request, 'HR/member_create.html')

