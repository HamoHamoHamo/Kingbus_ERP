from crudmember.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages

import datetime

from .forms import MemberForm, HRForm, MemberEditForm
from .models import Member, MemberDocument, HR
from utill.decorator import option_year_deco


class ManagementList(generic.ListView):
    template_name = 'HR/HR_list.html'
    context_object_name = 'HR_list'
    model = HR
    paginate_by = 10

    def get_queryset(self):
        self.selected_year = self.request.GET.get('year', "")
        self.selected_month = self.request.GET.get('month', "")
        
        if self.selected_year and self.selected_month:
            month = self.selected_year +"-" + self.selected_month
            HR_list = HR.objects.filter(start_date__startswith=month).order_by('-start_date')
        else:
            HR_list = HR.objects.order_by('-start_date')
        return HR_list
    
    @option_year_deco
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

        context['selected_year'] = self.selected_year
        context['selected_month'] = self.selected_month
        try:
            context['int_selected_year'] = int(self.selected_year)
            context['int_selected_month'] = int(self.selected_month)
        except Exception as e:
            print(e)
        return context

def HR_create(request):
    context = {}
    if request.method == "POST":
        member_id=request.POST.get('member_id', None)
        HR_form = HRForm(request.POST)
        if HR_form.is_valid() and member_id:
            hr = HR_form.save(commit=False)
            print("테스트ㅡㅡㅡ",hr)
            try:
                hr.member_id = Member.objects.get(pk=member_id)
                hr.creator = User.objects.get(pk=request.session.get('user'))
                hr.save()
            except Exception as e:
                print(e)
                raise Http404
            return redirect('HR:management')
        else:
            for msg in HR_form.errors:
                messages.error(request, f"{msg}: {HR_form.errors[msg]}")
            context = {
                'HR_form' : HRForm(),
                'members' : Member.objects.all()
            }
            return render(request, 'HR/HR_create.html', context)

    else:
        context = {
            'HR_form' : HRForm(),
            'members' : Member.objects.all()
        }
    return render(request, 'HR/HR_create.html', context)

def HR_edit(request, pk):
    hr = get_object_or_404(HR, pk=pk)

    if request.method == "POST":
        member_id=request.POST.get('member_id', None)
        HR_form = HRForm(request.POST)
        if HR_form.is_valid() and member_id:
            edit_hr = HR_form.save(commit=False)
            #print("테스트ㅡㅡㅡ",edit_hr.id) id는 입력값이 없기 때문에 None으로 나옴
            edit_hr.member_id = get_object_or_404(Member, pk=member_id)
            edit_hr.creator = User.objects.get(pk=request.session.get('user'))
            hr.delete()
            edit_hr.id = pk
            edit_hr.save()
            return redirect('HR:management')
    else:
        context = {
            'hr' : hr,
            'members' : Member.objects.all(),
            'member_id' : hr.member_id,
        }
    return render(request, 'HR/HR_edit.html', context)

def HR_delete(request, pk):
    hr = get_object_or_404(HR, pk=pk)
    # 권한 확인 필요
    if User.objects.get(pk=request.session['user']).authority == "관리자":
        hr.delete()
    return redirect('HR:management')

class MemberList(generic.ListView):
    template_name = 'HR/member_list.html'
    context_object_name = 'member_list'
    paginate_by = 10
    model = Member


    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            selector = self.request.GET.get('top_box_selector', None)    
            if  selector == 'name':
                member = Member.objects.filter(name__startswith=search)
                print("aaaaaaaa", member)
            elif selector == "role":
                member = Member.objects.filter(role=search)
            elif selector == "phone":
                member = Member.objects.filter(phone_num=search)
            elif selector == "address":
                member = Member.objects.filter(address__startswith=search)
            else:
                raise Http404()
            return member
        else:
            return super().get_queryset()

    # 페이징 처리
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
        context['current_page'] = current_page

        context['searched'] = self.request.GET.get('search', '')
        context['selector'] = self.request.GET.get('top_box_selector', 'name')
        return context

class MemberDetail(generic.DetailView):
    template_name = 'HR/member_detail.html'
    context_object_name = 'member'
    model = Member
    
    @option_year_deco
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_year'] = self.request.GET.get('year', "")
        context['selected_month'] = self.request.GET.get('month', "")
        month = context['selected_year'] +"-" + context['selected_month']
        try:
            context['int_selected_year'] = int(context['selected_year'])
            context['int_selected_month'] = int(context['selected_month'])
            context['hr'] = HR.objects.filter(member_id=context['member']).filter(start_date__startswith=month).order_by("finish_date", "start_date")
        except Exception as e:
            print(e)
            context['hr'] = HR.objects.filter(member_id=context['member']).order_by("finish_date", "start_date")
        return context

def member_create(request):
    context = {}
    if request.method == "POST":
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            member_form.save()
            return redirect('HR:member')
    else:
        context = {
            'member_form' : MemberForm(request.POST),
        }
    return render(request, 'HR/member_create.html', context)

def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        member_form = MemberEditForm(request.POST)
        if member_form.is_valid():
            
            member.name = member_form.cleaned_data['name']
            member.role = member_form.cleaned_data['role']
            member.person_id1 = member_form.cleaned_data['person_id1']
            member.person_id2 = member_form.cleaned_data['person_id2']
            member.address = member_form.cleaned_data['address']
            member.phone_num = member_form.cleaned_data['phone_num']
            member.entering_date = member_form.cleaned_data['entering_date']
            member.resignation_date = member_form.cleaned_data['resignation_date']
            member.license_num = member_form.cleaned_data['license_num']
            member.check = member_form.cleaned_data['check']
            member.save()
            return redirect('HR:member')
    else:
        context = {
            'member' : member
        }
    return render(request, 'HR/member_edit.html', context)

def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    # 권한 확인 필요
    if User.objects.get(pk=request.session['user']).authority == "관리자":
        member.delete()
    else:
        print("권한이 없습니다.")
    return redirect('HR:member')

