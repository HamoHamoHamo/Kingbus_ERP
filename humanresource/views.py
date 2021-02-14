from crudmember.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import MemberForm, HRForm
from .models import Member, MemberDocument, HR


class ManagementList(generic.ListView):
    template_name = 'HR/management.html'
    context_object_name = 'HR_list'
    model = HR

    def get_queryset(self):
        HR_list = HR.objects.order_by('-start_date')
        return HR_list

def HR_create(request):
    context = {}
    if request.method == "POST":
        member_id=request.POST.get('member_id', None)
        HR_form = HRForm(request.POST)
        if HR_form.is_valid() and member_id:
            hr = HR_form.save(commit=False)
            print("테스트ㅡㅡㅡ",hr)
            hr.member_id = get_object_or_404(Member, pk=member_id)
            hr.creator = User.objects.get(pk=request.session.get('user'))
            hr.save()
            return redirect('HR:management')
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
            'HR_form' : HRForm(instance=hr),
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
    model = Member

class MemberDetail(generic.DetailView):
    template_name = 'HR/member_detail.html'
    context_object_name = 'member'
    model = Member
    
def member_create(request):
    context = {}
    if request.method == "POST":
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            member_form.save()
            return redirect('HR:member')
    else:
        context = {
            'member_form' : MemberForm(),
        }
    return render(request, 'HR/member_create.html', context)

def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            edit_member = member_form.save(commit=False)
            #print("테스트ㅡㅡㅡ",edit_member.id) id는 입력값이 없기 때문에 None으로 나옴
            member.delete()
            edit_member.id = pk
            edit_member.save()
            return redirect('HR:member')
    else:
        context = {
            'member_form' : MemberForm(instance=member),
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

