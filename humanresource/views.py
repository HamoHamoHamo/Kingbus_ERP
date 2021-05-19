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
    paginate_by = 10

    def get_queryset(self):
        HR_list = HR.objects.order_by('-start_date')
        return HR_list
    
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

        return context

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

