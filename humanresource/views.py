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

from .forms import MemberForm, HRForm
from .models import Member, HR, Yearly
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
            member.creator = User.objects.get(pk=request.session.get('user'))
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
    
class ManagementList(generic.ListView):
    template_name = 'HR/mgmt.html'
    context_object_name = 'hr_list'
    model = HR
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        hr_list = ''
        if name:
            member_list = Member.objects.filter(name=name)
            for member in member_list:
                hr = HR.objects.filter(member_id=member).order_by('-start_date')
                if hr_list:
                    hr_list = hr_list | hr
                else:
                    hr_list = hr
                    
        else:
            hr_list = HR.objects.order_by('-start_date')
        return hr_list
                
    
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

        yearly = Yearly.objects.select_related('member_id')
        
        cnt = {}
        for y in yearly:
            cnt[int(y.member_id.id)] = {y.year: y.cnt}

        # for hr in context['hr_list']:

        print("CNTTT", cnt)
        context['cnt'] = cnt
        context['name'] = self.request.GET.get('name', '')
        context['member_list'] = Member.objects.all()
        return context

def mgmt_create(request):
    if request.method == "POST":
        member_id=request.POST.get('member_id', None)
        HR_form = HRForm(request.POST)
        if HR_form.is_valid() and member_id:
            hr = HR_form.save(commit=False)
            
            hr.member_id = Member.objects.get(pk=member_id)
            hr.creator = User.objects.get(pk=request.session.get('user'))
            hr.save()
        
            return redirect('HR:mgmt')
        else:
            raise Http404
    else:
        raise HttpResponseNotAllowed(['post'])
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class ManagementList(generic.ListView):
#     template_name = 'HR/HR_list.html'
#     context_object_name = 'HR_list'
#     model = HR
#     #paginate_by = 10

#     def get_queryset(self):
#         hr_name = self.request.GET.get('hr_name', None)
#         hr_type = self.request.GET.get('hr_type', None)
#         date1 = self.request.GET.get('date1', None)
#         date2 = self.request.GET.get('date2', None)
#         print(hr_name, hr_type)

#         if not hr_name and not hr_type and not date1 and not date2:
#             hr = HR.objects.all().order_by('start_date')
#         else:
#             hr = None
#             if hr_name:
#                 member = Member.objects.filter(name__startswith=hr_name)                 
#                 for m in member:
#                     result = HR.objects.filter(member_id=m.id)
#                     if hr == None:
#                         hr = result
#                     hr = hr | result

#             if hr_type:
#                 if hr:
#                     hr = hr.filter(hr_type=hr_type)
#                 else:
#                     hr = HR.objects.filter(hr_type=hr_type)
                
#             if date1 or date2:
#                 if hr:
#                     hr = hr.filter(start_date__range=[date1,date2])            
#                 else: 
#                     hr = HR.objects.filter(start_date__range=[date1,date2])

#         return hr
    
#     #@option_year_deco
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         '''
#         페이징
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
#         '''
        
#         '''
#         context['selected_year'] = self.selected_year
#         context['selected_month'] = self.selected_month
#         try:
#             context['int_selected_year'] = int(self.selected_year)
#             context['int_selected_month'] = int(self.selected_month)
#         except Exception as e:
#             print(e)
#         '''
#         context['member_list'] = Member.objects.all()
#         return context

# def HR_create(request):
#     context = {}
#     if request.method == "POST":
#         member_id=request.POST.get('member_id', None)
#         HR_form = HRForm(request.POST)
#         print("aaaaaaaaaa", member_id)
#         if HR_form.is_valid() and member_id:
#             hr = HR_form.save(commit=False)
#             print("테스트ㅡㅡㅡ",hr)
#             try:
#                 hr.member_id = Member.objects.get(pk=member_id)
#                 hr.creator = User.objects.get(pk=request.session.get('user'))
#                 hr.save()
#             except Exception as e:
#                 print("error", e)
#                 raise Http404
#             return redirect('HR:management')
#         else:
#             for msg in HR_form.errors:
#                 messages.error(request, f"{msg}: {HR_form.errors[msg]}")
#             context = {
#                 'HR_form' : HRForm(),
#                 'members' : Member.objects.all()
#             }
#             return redirect('HR:management')

#     else:
#         raise Http404

# class HRDetail(generic.DetailView):
#     template_name = 'HR/HR_detail.html'
#     context_object_name = 'HR'
#     model = HR
#     #paginate_by = 10

    
#     #@option_year_deco
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         member_name = self.request.GET.get('member_name', None)
#         member_role = self.request.GET.get('member_role', None)
#         member_list = None

#         if not member_name and not member_role:
#             context['member_list'] = Member.objects.all()
#         else:
#             if member_name:
#                 member_list = Member.objects.filter(name__startswith=member_name)
#             if member_role:
#                 if member_list:
#                     member_list.filter(role=member_role)
#                 else:
#                     member_list = Member.objects.filter(role=member_role)
#             context['member_list'] = member_list
        
#         hr_name = self.request.GET.get('hr_name', None)
#         hr_type = self.request.GET.get('hr_type', None)
#         date1 = self.request.GET.get('date1', None)
#         date2 = self.request.GET.get('date2', None)

#         if not hr_name and not hr_type and not date1 and not date2:
#             context['HR_list'] = HR.objects.all().order_by('start_date')
            
#         else:
#             hr = None
#             if hr_name:
#                 member = Member.objects.filter(name__startswith=hr_name)                 
#                 for m in member:
#                     result = HR.objects.filter(member_id=m.id)
#                     if hr == None:
#                         hr = result
#                     hr = hr | result

#             if hr_type:
#                 if hr:
#                     hr = hr.filter(hr_type=hr_type)
#                 else:
#                     hr = HR.objects.filter(hr_type=hr_type)
                
#             if date1 or date2:
#                 if hr:
#                     hr = hr.filter(start_date__range=[date1,date2])            
#                 else: 
#                     hr = HR.objects.filter(start_date__range=[date1,date2])
#             context['HR_list'] = hr
#         return context


# def HR_edit(request, pk):
#     hr = get_object_or_404(HR, pk=pk)

#     if request.method == "POST":
#         member_id=request.POST.get('member_id', None)
#         HR_form = HRForm(request.POST)
#         if HR_form.is_valid() and member_id:
#             edit_hr = HR_form.save(commit=False)
#             #print("테스트ㅡㅡㅡ",edit_hr.id) id는 입력값이 없기 때문에 None으로 나옴
#             edit_hr.member_id = get_object_or_404(Member, pk=member_id)
#             edit_hr.creator = User.objects.get(pk=request.session.get('user'))
#             hr.delete()
#             edit_hr.id = pk
#             edit_hr.save()
#             return redirect('HR:management')
#     else:
#         raise Http404

# def HR_delete(request):
#     hr_list = request.POST.getlist('hr_delete')    

#     for pk in hr_list:
#         hr = get_object_or_404(HR, pk=pk)
#         hr.delete()

#     return redirect('HR:management')

# class MemberList(generic.ListView):
#     template_name = 'HR/member_list.html'
#     context_object_name = 'member_list'
#     model = Member


#     def get_queryset(self):
#         name = self.request.GET.get('name', None)
#         role = self.request.GET.get('role', None)
#         date1 = self.request.GET.get('date1', None)
#         date2 = self.request.GET.get('date2', None)

#         if not name and not role and not date1 and not date2:
#             member = Member.objects.all().order_by('-pk')
#         else:            
#             member = None
#             if name:
#                 member = Member.objects.filter(name__startswith=name)
#             if role:
#                 if member:
#                     member = member.filter(role=role)
#                 else:
#                     member = Member.objects.filter(role=role)
#             if date1 or date2:
#                 if member:
#                     member = member.filter(entering_date__range=[date1,date2])            
#                 else: 
#                     member = Member.objects.filter(entering_date__range=[date1,date2])
#             member.order_by('-pk')
#         return member

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context['name'] = self.request.GET.get('name', '')
#         context['selector'] = self.request.GET.get('top_box_selector', 'name')
#         return context

# class MemberDetail(generic.DetailView):
#     template_name = 'HR/member_detail.html'
#     context_object_name = 'member'
#     model = Member
    
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['files'] = MemberDocument.objects.filter(member_id=self.kwargs['pk'])
#         context['name'] = self.request.GET.get('name', '')
#         context['selector'] = self.request.GET.get('top_box_selector', 'name')

#         #
#         name = self.request.GET.get('name', None)
#         role = self.request.GET.get('role', None)
#         date1 = self.request.GET.get('date1', None)
#         date2 = self.request.GET.get('date2', None)

#         if not name and not role and not date1 and not date2:
#             member = Member.objects.all().order_by('-pk')
#         else:
#             member = None
#             if name:
#                 member = Member.objects.filter(name__startswith=name)
#             if role:
#                 if member:
#                     member = member.filter(role=role)
#                 else:
#                     member = Member.objects.filter(role=role)
#             if date1 or date2:
#                 if member:
#                     member = member.filter(entering_date__range=[date1,date2])            
#                 else: 
#                     member = Member.objects.filter(entering_date__range=[date1,date2])
#             member.order_by('-pk')
#         context['member_list'] = member

        
#         return context

# def member_create(request):
#     context = {}
#     if request.method == "POST":
#         member_form = MemberForm(request.POST)
#         if member_form.is_valid():
#             files = request.FILES.getlist('file', None)
#             #print("aaaaaaaaaaaaaaaaaaaaaaaa",files)
#             member = member_form.save(commit=False)
#             member.save()

#             member_file_save(files,member)
#             return redirect('HR:member')
#     else:
#         raise Http404

# def member_file_save(upload_file, member):
#     for file in upload_file:
#         member_file = MemberDocument(
#             member_id=member,
#             file=file,
#             filename=file.name,
#         )
#         member_file.save()
#     return
# def download(request, pk, file_id):
#     download_file = get_object_or_404(MemberDocument, pk=file_id)
#     if download_file.member_id == Member.objects.get(pk=pk):
#         url = download_file.file.url
#         root = str(BASE_DIR)+url

#         if os.path.exists(root):
#             with open(root, 'rb') as fh:
#                 quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
#                 response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
#                 response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
#                 return response
#             raise Http404
#         else:
#             #print("에러")
#             raise Http404
#     else:
#         raise Http404

# def file_del(request, pk, file_id):
    
#     member = Member.objects.get(pk=pk)
#     member_file = MemberDocument.objects.get(pk=file_id)
#     os.remove(member_file.file.path)
#     member_file.delete()
    
#     return redirect(reverse('HR:member_detail', args=(pk,)))

# def member_edit(request, pk):
#     member = get_object_or_404(Member, pk=pk)

#     if request.method == "POST":
#         member_form = MemberForm(request.POST)
#         if member_form.is_valid():
#             files = request.FILES.getlist('file', None)
#             member_file_save(files,member)
#             member.name = member_form.cleaned_data['name']
#             member.role = member_form.cleaned_data['role']
#             member.person_id1 = member_form.cleaned_data['person_id1']
#             member.person_id2 = member_form.cleaned_data['person_id2']
#             member.address = member_form.cleaned_data['address']
#             member.phone_num = member_form.cleaned_data['phone_num']
#             member.entering_date = member_form.cleaned_data['entering_date']
#             member.resignation_date = member_form.cleaned_data['resignation_date']
#             member.save()

#             return redirect('HR:member')
#     else:
#         raise Http404

# def HR_edit(request, pk):
#     hr = get_object_or_404(HR, pk=pk)

#     if request.method == "POST":
#         member_id=request.POST.get('member_id', None)
#         HR_form = HRForm(request.POST)
#         if HR_form.is_valid() and member_id:
#             edit_hr = HR_form.save(commit=False)
#             #print("테스트ㅡㅡㅡ",edit_hr.id) id는 입력값이 없기 때문에 None으로 나옴
#             edit_hr.member_id = get_object_or_404(Member, pk=member_id)
#             edit_hr.creator = User.objects.get(pk=request.session.get('user'))
#             hr.delete()
#             edit_hr.id = pk
#             edit_hr.save()
#             return redirect('HR:management')
#     else:
#         raise Http404

# def member_delete(request):
#     list = request.POST.getlist('member_delete')
#     for pk in list:
#         member = get_object_or_404(Member, pk=pk)
#         member.delete()


#     return redirect('HR:member')
#     '''
#     # 권한 확인 필요
#     if User.objects.get(pk=request.session['user']).authority == "관리자":
#         member.delete()
#     else:
#         print("권한이 없습니다.")
#     '''
#     return redirect('HR:member')

# def HR_delete(request):
#     hr_list = request.POST.getlist('hr_delete')    

#     for pk in hr_list:
#         hr = get_object_or_404(HR, pk=pk)
#         hr.delete()

#     return redirect('HR:management')