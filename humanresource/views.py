import mimetypes
import os
import urllib
from crudmember.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from ERP.settings import BASE_DIR

from datetime import datetime

from vehicle.models import Vehicle

from .forms import MemberForm
from .models import Member
from utill.decorator import option_year_deco

TODAY = str(datetime.now())[:10]

def member(request):

    return render(request, 'HR/member.html')

def mgmt(request):

    return render(request, 'HR/mgmt.html')

class MemberList(generic.ListView):
    template_name = 'HR/member.html'
    context_object_name = 'member_list'
    model = Member
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        if name:
            member_list = Member.objects.filter(name=name).order_by('name')
        else:
            member_list = Member.objects.order_by('name')
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        #페이징 끝

        context['name'] = self.request.GET.get('name', '')
        context['member_all'] = Member.objects.order_by('name')
        
        return context

def member_create(request):
    if request.method == "POST":
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            member = member_form.save(commit=False)
            member.creator = Member.objects.get(pk=request.session.get('user'))
            user_id = request.POST.get('user_id', None)
            if Member.objects.filter(user_id=user_id).exists(): #아이디 중복체크
                raise Http404
            
            member.user_id = user_id
            member.password = make_password('0000')
            member.save()

            return redirect('HR:member')
    else:
        return HttpResponseNotAllowed(['post'])

def member_edit(request):
    pk = request.POST.get('id', None)
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            if member_form.cleaned_data['role'] == '운전원' and member.name != member_form.cleaned_data['name']:
                for vehicle in Vehicle.objects.filter(driver=member):
                    vehicle.driver_name = member_form.cleaned_data['name']
                    vehicle.save()
            member.name = member_form.cleaned_data['name']
            member.role = member_form.cleaned_data['role']
            member.entering_date = member_form.cleaned_data['entering_date']
            member.license_number = member_form.cleaned_data['license_number']
            member.phone_num = member_form.cleaned_data['phone_num']
            member.birthdate = member_form.cleaned_data['birthdate']
            member.address = member_form.cleaned_data['address']
            
            
            member.save()


            return redirect('HR:member')
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def member_delete(request):
    if request.method == 'POST':
        del_list = request.POST.getlist('delete_check', '')
        for pk in del_list:
            member = get_object_or_404(Member, pk=pk)
            vehicle_list = Vehicle.objects.filter(driver=member)
            for vehicle in vehicle_list:
                vehicle.driver_name = ''
                vehicle.save()
            member.delete()

        return redirect('HR:member')
    else:
        return HttpResponseNotAllowed(['post'])
    
# class ManagementList(generic.ListView):
#     template_name = 'HR/mgmt.html'
#     context_object_name = 'hr_list'
#     model = HR
#     paginate_by = 10

#     def get_queryset(self):
#         name = self.request.GET.get('name', None)
#         hr_list = ''
#         if name:
#             member_list = Member.objects.filter(name=name)
#             for member in member_list:
#                 hr = HR.objects.filter(member_id=member).order_by('-start_date')
#                 if hr_list:
#                     hr_list = hr_list | hr
#                 else:
#                     hr_list = hr
                    
#         else:
#             hr_list = HR.objects.order_by('-start_date')
#         return hr_list
                
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)
#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index
#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range

#         yearly = Yearly.objects.select_related('member_id')
        
#         cnt = {}
#         for y in yearly:
#             cnt[int(y.member_id.id)] = {y.year: y.cnt}

#         # for hr in context['hr_list']:

#         print("CNTTT", cnt)
#         context['cnt'] = cnt
#         context['name'] = self.request.GET.get('name', '')
#         context['member_list'] = Member.objects.all()
#         return context

# def mgmt_create(request):
#     if request.method == "POST":
#         member_id=request.POST.get('member_id', None)
#         HR_form = HRForm(request.POST)
#         if HR_form.is_valid() and member_id:
#             hr = HR_form.save(commit=False)
            
#             hr.member_id = Member.objects.get(pk=member_id)
#             hr.creator = User.objects.get(pk=request.session.get('user'))
#             hr.save()
        
#             return redirect('HR:mgmt')
#         else:
#             raise Http404
#     else:
#         raise HttpResponseNotAllowed(['post'])
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
