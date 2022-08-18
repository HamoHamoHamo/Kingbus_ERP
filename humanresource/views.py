import mimetypes
import os
import urllib
from crudmember.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
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

class MemberList(generic.ListView):
    template_name = 'HR/member.html'
    context_object_name = 'member_list'
    model = Member
    paginate_by = 10

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        authority = self.request.session.get('authority')
        if authority >= 3:
            return redirect(self.request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        if authority == 2:
            authority = 1

        if name:
            member_list = Member.objects.filter(authority__gte=authority).filter(name=name).order_by('name')
        else:
            member_list = Member.objects.filter(authority__gte=authority).order_by('name')
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
    if request.session.get('authority') >= 3:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    if request.method == "POST":
        user_auth = request.session.get('authority')
        if user_auth == 2:
            user_auth = 1

        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            role = request.POST.get('role')
            if role == '용역':
                req_auth = 5
            elif role == '운전원':
                req_auth = 4
            elif role == '팀장':
                req_auth = 3
            elif role == '배차관리자':
                req_auth = 1
            elif role == '경리관리자':
                req_auth = 1
            elif role == '마스터':
                req_auth = 0
            
            if req_auth <= user_auth and user_auth != 0:
                return HttpResponseBadRequest()
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
    if request.session.get('authority') >= 3:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
    pk = request.POST.get('id', None)
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        user_auth = request.session.get('authority')
        if user_auth == 2:
            user_auth = 1
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            role = request.POST.get('role')
            if role == '용역':
                req_auth = 5
            elif role == '운전원':
                req_auth = 4
            elif role == '팀장':
                req_auth = 3
            elif role == '배차관리자':
                req_auth = 2
            elif role == '경리관리자':
                req_auth = 1
            elif role == '마스터':
                req_auth = 0

            cur_auth = member.authority
            if (cur_auth <= 2 or req_auth <= 2) and user_auth != 0:
                return HttpResponseBadRequest()

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
            member.authority = req_auth
            
            member.save()

            return redirect('HR:member')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['post'])

def member_delete(request):
    user_auth = request.session.get('authority')
    if user_auth >= 3:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    if request.method == 'POST':
        del_list = request.POST.getlist('delete_check', '')
        ####권한 확인
        
        if user_auth == 1:
            user_auth = 2
        for pk in del_list:
            req_auth = get_object_or_404(Member, pk=pk).authority
            if req_auth <= user_auth and user_auth != 0:
                return HttpResponseBadRequest()
        ####
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
