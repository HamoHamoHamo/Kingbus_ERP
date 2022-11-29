import os
from dateutil.relativedelta import relativedelta
from dispatch.models import DispatchRegularlyConnect, DispatchOrderConnect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from dispatch.views import FORMAT
from datetime import datetime, timedelta

from vehicle.models import Vehicle
from .forms import MemberForm
from .models import Member, MemberFile, Salary, AdditionalSalary, DeductionSalary

TODAY = str(datetime.now())[:10]
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]

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
        name = self.request.GET.get('name', '')
        age = self.request.GET.get('age', '나이 전체')
        use = self.request.GET.get('use', '사용')
        up65 = f'{int(TODAY[:4]) - 65}{TODAY[4:10]}'

        authority = self.request.session.get('authority')

        if authority >= 3:
            return redirect(self.request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        if authority == 2:
            authority = 1

        if name:
            member_list = Member.objects.filter(use=use).filter(authority__gte=authority).filter(name__contains=name).order_by('name')
        else:
            member_list = Member.objects.filter(use=use).filter(authority__gte=authority).order_by('name')
            print('memberrrrrr', member_list, use)
        if age == '65세 이상':
            print('testtt')
            member_list = member_list.filter(birthdate__lte=up65)
            
        
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
        context['start_num'] = paginator.count - paginator.per_page * (current_page-1)

        member_list = context['member_list']
        data_list = []
        for member in member_list:
            bus_license_name = ''
            license_name = ''
            license_id = ''
            bus_license_id = ''
            for file in member.member_file.all():
                if file.type == '면허증':
                    license_name = file.filename
                    license_id = file.id
                elif file.type == '버스운전 자격증':
                    bus_license_name = file.filename
                    bus_license_id = file.id
                    
            data_list.append({
                'name': member.name,
                'role': member.role,
                'birthdate': member.birthdate,
                'address': member.address,
                'phone_num': member.phone_num,
                'entering_date': member.entering_date,
                'id': member.user_id,
                'license': license_name,
                'bus_license': bus_license_name,
                'note': member.note,
                'user_id': member.id,
                'emergency': member.emergency,
                'license_id': license_id,
                'bus_license_id': bus_license_id,
                'use': member.use
            })
        context['data_list'] = data_list
        context['name'] = self.request.GET.get('name', '')
        context['use'] = self.request.GET.get('use', '사용')
        context['age'] = self.request.GET.get('age', '나이 전체')
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
            creator = Member.objects.get(pk=request.session.get('user'))
            member = member_form.save(commit=False)
            member.num = Member.objects.count() + 1
            member.creator = creator
            member.authority = req_auth
            user_id = request.POST.get('user_id', None)
            if Member.objects.filter(user_id=user_id).exists(): #아이디 중복체크
                raise Http404
            
            member.user_id = user_id
            member.password = make_password('0000')
            member.emergency = request.POST.get('emergency1', '') + ' ' + request.POST.get('emergency2', '')
            member.save()

            license = request.FILES.get('license_file', None)
            bus_license = request.FILES.get('bus_license_file', None)

            if license:
                member_file_save(license, member, '면허증', creator)
            
            if bus_license:
                member_file_save(bus_license, member, '버스운전 자격증', creator)


            return redirect('HR:member')
    else:
        return HttpResponseNotAllowed(['post'])

def member_file_save(upload_file, member, type, creator):
    member_file = MemberFile(
        member_id=member,
        file=upload_file,
        filename=upload_file.name,
        type=type,
        creator=creator,
    )
    member_file.save()
    # print(vehicle_file)
    return

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
            member.phone_num = member_form.cleaned_data['phone_num']
            member.birthdate = member_form.cleaned_data['birthdate']
            member.address = member_form.cleaned_data['address']
            member.note = member_form.cleaned_data['note']
            member.emergency = request.POST.get('emergency1', '') + ' ' + request.POST.get('emergency2', '')
            member.authority = req_auth
            
            member.save()

            # 파일
            creator = Member.objects.get(pk=request.session.get('user'))
            license_file = request.FILES.get('license_file', None)
            bus_license_file = request.FILES.get('bus_license_file', None)
            l_file_name = request.POST.get('license', None)
            b_file_name = request.POST.get('bus_license', None)

            cur_files = MemberFile.objects.filter(member_id=member)
            try:
                cur_license_file = cur_files.get(type='면허증')
            except:
                cur_license_file = None
            try:
                cur_bus_license_file = cur_files.get(type='버스운전 자격증')
            except:
                cur_bus_license_file = None

            if license_file:
                if cur_license_file:
                    os.remove(cur_license_file.file.path)
                    cur_license_file.delete()
                file = MemberFile(
                    member_id=member,
                    file=license_file,
                    filename=license_file.name,
                    type='면허증',
                    creator=creator,
                )
                file.save()
            elif not l_file_name and cur_license_file:
                os.remove(cur_license_file.file.path)
                cur_license_file.delete()

            if bus_license_file:
                if cur_bus_license_file:
                    os.remove(cur_bus_license_file.file.path)
                    cur_bus_license_file.delete()

                file = MemberFile(
                    member_id=member,
                    file=bus_license_file,
                    filename=bus_license_file.name,
                    type='버스운전 자격증',
                    creator=creator,
                )
                file.save()
            elif not b_file_name and cur_bus_license_file:
                os.remove(cur_bus_license_file.file.path)
                cur_bus_license_file.delete()
                
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
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

def member_img(request, file_id):
    context = {
        'img': get_object_or_404(MemberFile, id=file_id)
    }
    return render(request, 'vehicle/document_img.html', context)



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

class SalaryList(generic.ListView):
    template_name = 'HR/salary_list.html'
    context_object_name = 'member_list'
    model = Member

    def get_queryset(self):
        month = self.request.GET.get('month', TODAY[:7])
        name = self.request.GET.get('name', '')

        
        member_list = Member.objects.filter(entering_date__lt=month+'-32').order_by('name')
        if name:
            member_list = member_list.filter(name__contains=name)
        
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month = self.request.GET.get('month', TODAY[:7])
        name = self.request.GET.get('name', '')

        salary_list = []
        additional_list = []
        deduction_list = []
        for member in context['member_list']:
            try:
                salary = Salary.objects.filter(member_id=member).get(month=month)
            except Salary.DoesNotExist:
                creator = Member.objects.get(pk=self.request.session.get('user'))
                salary = new_salary(creator, month, member)
            
            salary_list.append(salary)

            ###########
            temp_add = []
            additionals = AdditionalSalary.objects.filter(member_id=member).filter(salary_id=salary)
            for additional in additionals:
                temp_add.append({
                    'price': additional.price,
                    'remark': additional.remark,
                    'id': additional.id,
                })
            additional_list.append(temp_add)

            temp_ded = []    
            deductions = DeductionSalary.objects.filter(member_id=member).filter(salary_id=salary)
            for deduction in deductions:
                temp_ded.append({
                    'price': deduction.price,
                    'remark': deduction.remark,
                    'id': deduction.id,
                })
            deduction_list.append(temp_ded)

        context['additional_list'] = additional_list
        context['deduction_list'] = deduction_list
        context['salary_list'] = salary_list
        
        context['month'] = month
        context['name'] = name

        return context
## 확인 필요
# month의 출근 퇴근 일반 요금 계산해서 Salary 생성
def new_salary(creator, month, member):
    last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
    attendance = DispatchRegularlyConnect.objects.filter(work_type='출근').filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))
    leave = DispatchRegularlyConnect.objects.filter(work_type='퇴근').filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))
    order = DispatchOrderConnect.objects.filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))

    attendance_price = 0
    leave_price = 0
    order_price = 0

    base = 0
    service_allowance = 0
    position_allowance = 0

    if TODAY[:7] <= month:
        base = int(member.base)
        service_allowance = int(member.service_allowance)
        position_allowance = int(member.position_allowance)

    # if salary:
    #     base = salary.base
    #     service_allowance = salary.service_allowance
    #     position_allowance = salary.position_allowance

    if attendance['driver_allowance__sum']:
        attendance_price = int(attendance['driver_allowance__sum'])
    if leave['driver_allowance__sum']:
        leave_price = int(leave['driver_allowance__sum'])
    if order['driver_allowance__sum']:
        order_price = int(order['driver_allowance__sum'])

    salary = Salary(
        member_id = member,
        base = base,
        service_allowance = service_allowance,
        position_allowance = position_allowance,
        attendance = attendance_price,
        leave = leave_price,
        order = order_price,
        total = attendance_price + leave_price + order_price + base + service_allowance + position_allowance,
        month = month,
        creator = creator
    )
    salary.save()
    return salary

def salary_detail(request):
    member_id_list = request.GET.get('driver').split(',')
    month = request.GET.get('date')
    
    member_list = []
    for member_id in member_id_list:
        member = get_object_or_404(Member, id=member_id)

        last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)[8:10]
        
        attendance_list = [''] * int(last_date)
        leave_list = [''] * int(last_date)
        order_list = [''] * int(last_date)
        order_price_list = [0] * int(last_date)
        attendance_price_list = [0] * int(last_date)
        leave_price_list = [0] * int(last_date)
        week_list = []
        
        
        total_list = [0] * int(last_date)
        work_cnt = 0
        

        salary = Salary.objects.filter(member_id=member).get(month=month)
        additional = salary.additional_salary.all()
        deduction = salary.deduction_salary.all()

        connects = DispatchOrderConnect.objects.filter(departure_date__range=(f'{month}-01', {month}-{last_date})).filter(driver_id=member)
        order_price = 0
        for connect in connects:
            c_date = int(connect.departure_date[8:10]) - 1
            if not order_list[c_date]:
                order_list[c_date] = []
            order_list[c_date].append([connect.order_id.departure, connect.order_id.arrival])
            order_price += int(connect.driver_allowance)
        if connects:
            order_price_list[c_date] = order_price
            total_list[c_date] += order_price

        attendances = DispatchRegularlyConnect.objects.filter(departure_date__range=(f'{month}-01', {month}-{last_date})).filter(work_type='출근').filter(driver_id=member)
        attendance_price = 0
        for attendance in attendances:
            c_date = int(attendance.departure_date[8:10]) - 1
            if not attendance_list[c_date]:
                attendance_list[c_date] = []
            attendance_list[c_date].append([attendance.regularly_id.departure, attendance.regularly_id.arrival])
            attendance_price += int(attendance.driver_allowance)
        if attendances:
            attendance_price_list[c_date] = attendance_price
            total_list[c_date] += attendance_price

        leaves = DispatchRegularlyConnect.objects.filter(departure_date__range=(f'{month}-01', {month}-{last_date})).filter(work_type='퇴근').filter(driver_id=member)
        leave_price = 0
        for leave in leaves:
            c_date = int(leave.departure_date[8:10]) - 1
            if not leave_list[c_date]:
                leave_list[c_date] = []
            leave_list[c_date].append([leave.regularly_id.departure, leave.regularly_id.arrival])
            leave_price += int(leave.driver_allowance)
        if leaves:
            leave_price_list[c_date] = leave_price
            total_list[c_date] += leave_price


        for i in range(int(last_date)):
            check = 0

            if i + 1 < 10:
                date = f'{month}-0{i+1}'
            else:
                date = f'{month}-{i+1}'

            week_list.append(WEEK[datetime.strptime(date, FORMAT).weekday()])

            if check == 1:
                work_cnt += 1

        
        member_list.append({
            'order_list': order_list,
            'attendance_list': attendance_list,
            'leave_list': leave_list,
            'order_price_list': order_price_list,
            'attendance_price_list': attendance_price_list,
            'leave_price_list': leave_price_list,
            'salary': salary,
            'member': member,
            'week_list': week_list,
            'total_list': total_list,
            'work_cnt': work_cnt,
            'additional': additional,
            'deduction': deduction,
        })
        
    context = {
        'member_list': member_list,
        'month': month
    }
    return render(request, 'HR/salary_detail.html', context)


def salary_edit(request):
    if request.method == 'POST':
        base_list = request.POST.getlist('base')
        service_list = request.POST.getlist('service')
        position_list = request.POST.getlist('position')
        id_list = request.POST.getlist('id')
        month = request.POST.get('month')

        for base, service, position, id in zip(base_list, service_list, position_list, id_list):
            member = get_object_or_404(Member, id=id)
            base = int(base.replace(',',''))
            service = int(service.replace(',',''))
            position = int(position.replace(',',''))

            salary = Salary.objects.filter(member_id=member).get(month=month)
            salary.base = base
            salary.service_allowance = service
            salary.position_allowance = position
            salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.base) + int(salary.service_allowance) + int(salary.position_allowance) + int(salary.additional) - int(salary.deduction)
            salary.save()

            if TODAY[:7] <= month:
                member.base = base
                member.service_allowance = service
                member.position_allowance = position
                member.save()

                edit_salary_list = Salary.objects.filter(month__gt=month).filter(member_id=member)
                for e_salary in edit_salary_list:
                    e_salary.base = base
                    e_salary.service_allowance = service
                    e_salary.position_allowance = position
                    e_salary.total = int(e_salary.attendance) + int(e_salary.leave) + int(e_salary.order) + int(e_salary.base) + int(e_salary.service_allowance) + int(e_salary.position_allowance) + int(e_salary.additional) - int(e_salary.deduction)
                    e_salary.save()



        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def salary_additional_create(request):
    if request.method == 'POST':
        member_id = request.POST.get('id', '')
        price = request.POST.get('price')
        remark = request.POST.get('remark')
        month = request.POST.get('month')
        creator = Member.objects.get(pk=request.session.get('user'))

        member = get_object_or_404(Member, id=member_id)
        salary = Salary.objects.filter(member_id=member).get(month=month)

        additional = AdditionalSalary(
            salary_id = salary,
            member_id = member,
            price = price,
            remark = remark,
            creator = creator,
        )
        additional.save()
        salary.additional = int(salary.additional) + int(price)
        salary.total = int(salary.total) + int(price)
        salary.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_additional_delete(request):
    if request.method == 'POST':
        id_list = request.POST.getlist('id')
        for id in id_list:
            additional = get_object_or_404(AdditionalSalary, id=id)
            
            salary = additional.salary_id
            salary.additional = int(salary.additional) - int(additional.price)
            salary.total = int(salary.total) - int(additional.price)
            salary.save()
            
            additional.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def salary_deduction_create(request):
    if request.method == 'POST':
        member_id = request.POST.get('id', '')
        price = request.POST.get('price')
        remark = request.POST.get('remark')
        month = request.POST.get('month')
        creator = Member.objects.get(pk=request.session.get('user'))

        member = get_object_or_404(Member, id=member_id)
        salary = Salary.objects.filter(member_id=member).get(month=month)

        deduction = DeductionSalary(
            salary_id = salary,
            member_id = member,
            price = price,
            remark = remark,
            creator = creator,
        )
        deduction.save()
        salary.deduction = int(salary.deduction) + int(price)
        salary.total = int(salary.total) - int(price)
        salary.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_deduction_delete(request):
    if request.method == 'POST':
        id_list = request.POST.getlist('id')
        for id in id_list:
            deduction = get_object_or_404(DeductionSalary, id=id)
            
            salary = deduction.salary_id
            salary.deduction = int(salary.deduction) - int(deduction.price)
            salary.total = int(salary.total) + int(deduction.price)
            salary.save()
            
            deduction.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])
