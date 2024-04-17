import json
import math
import re
from config.settings import MEDIA_ROOT
from django.shortcuts import render
from django.db.models import Q, Sum
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import AssignmentDataForm, AssignmentForm
from .models import Assignment, AssignmentData, AssignmentConnect, Group
from dispatch.models import DispatchRegularlyData, DispatchRegularlyWaypoint, DispatchOrderConnect, DispatchOrder, DispatchRegularly, RegularlyGroup, DispatchRegularlyConnect
from dispatch.commons import get_date_connect_list, get_multi_date_connect_list
from accounting.models import Collect, TotalPrice
from humanresource.models import Member, Salary, Team
from humanresource.views import send_message
from vehicle.models import Vehicle
from datetime import datetime, timedelta, date

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]
WEEK2 = ['월', '화', '수', '목', '금', '토', '일', ]

class AssignmentDataList(generic.ListView):
    template_name = 'assignment/assignment_data.html'
    context_object_name = 'assignment_list'
    model = AssignmentData

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
        
    def get_queryset(self):
        group_id = self.request.GET.get('group', '')
        search = self.request.GET.get('search', '')
        search_use = self.request.GET.get('use', '')

        if not group_id:
            group = Group.objects.order_by('number').first()
            return AssignmentData.objects.exclude(use='삭제').filter(group=group).order_by('num1', 'number1', 'num2', 'number2')
        else:
            group = get_object_or_404(Group, id=group_id)
            if search_use:
                return AssignmentData.objects.exclude(use='삭제').filter(use=search_use).filter(group=group).filter(Q(assignment__contains=search) | Q(location__contains=search)).order_by('num1', 'number1', 'num2', 'number2')
            else:
                return AssignmentData.objects.exclude(use='삭제').filter(group=group).filter(Q(assignment__contains=search) | Q(location__contains=search)).order_by('num1', 'number1', 'num2', 'number2')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        id = self.request.GET.get('id')
        context['search'] = self.request.GET.get('search', '')
        context['search_use'] = self.request.GET.get('use', '')

        if id:
            context['detail'] = get_object_or_404(AssignmentData, id=id)
        context['group_list'] = Group.objects.all().order_by('number', 'name')
        group_id = self.request.GET.get('group', '')
        if group_id:
            context['group'] = get_object_or_404(Group, id=group_id)
        elif not self.request.GET.get('new'):
            context['group'] = Group.objects.order_by('number').first()
        
        return context

class AssignmentList(generic.ListView):
    template_name = 'assignment/assignment.html'
    context_object_name = 'assignment_list'
    model = Assignment

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        date = self.request.GET.get('date', TODAY)
        group_id = self.request.GET.get('group', '')

        weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        
        if search:
            data_list = AssignmentData.objects.filter(assignment__contains=search).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
        else:
            if group_id:
                group = Group.objects.get(id=group_id)
                data_list = AssignmentData.objects.filter(group=group).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
            else:
                data_list = AssignmentData.objects.filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
        assignment_list = []
        for data in data_list:
            # first 확인필요
            assignment = data.assignment_id.filter(edit_date__lte=date).order_by('-edit_date').first()
            if not assignment:
                assignment = data.assignment_id.filter(edit_date__gte=date).order_by('edit_date').first()

            if assignment.use == '사용':
                assignment_list.append(assignment)
        return assignment_list


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        date = self.request.GET.get('date', TODAY)
        selected_group = self.request.GET.get('group', '')
        detail_id = self.request.GET.get('id')
        if detail_id:
            assignment_data = get_object_or_404(AssignmentData, id=detail_id)
            context['detail'] = assignment_data.assignment_id.filter(edit_date__lte=date).order_by('-edit_date').first()
            if not context['detail']:
                context['detail'] = assignment_data.assignment_id.filter(edit_date__gte=date).order_by('edit_date').first()
            context['detail_data_id'] = assignment_data.id
            # 지난 배차내역 불러오기
            # date_type = datetime.strptime(date, FORMAT)
            # int_start_date = date_type - timedelta(days=int(date_type.weekday()) + 8)
            # int_start_date = int(date_type.weekday()) + 8
            # start_date = date_type - timedelta(days=7) if int_start_date == 14 else date_type - timedelta(days=int_start_date)
            # str_end_date = datetime.strftime(start_date + timedelta(days=13), FORMAT)

            # str_start_date = datetime.strftime(start_date, FORMAT)
            
            # history_list = [''] * 14
            # date_list = []
            # block_list = ['y'] * 14

            # departure_date = f'{date} {context["detail"].start_time}'
            # arrival_date = f'{date} {context["detail"].end_time}'

            # for i in range(14):
                
            #     list_date = datetime.strftime(start_date + timedelta(days=i), FORMAT)
            #     date_list.append(f'{list_date} {WEEK[datetime.strptime(list_date, FORMAT).weekday()]}')
            # ##

            # regularly_history_list = DispatchRegularlyData.objects.get(monthly=context['detail']).monthly.all()
            # for reg in regularly_history_list:
            #     connect_history_list = reg.info_regularly.filter(departure_date__gte=str_start_date).filter(arrival_date__lte=str_end_date).order_by('departure_date')
            #     for connect_history in connect_history_list:
            #         date_calculation = (datetime.strptime(connect_history.departure_date[:10], FORMAT) - start_date).days
            #         history_list[date_calculation] = connect_history
            #         # block_list[date_calculation] = ''

            #         h_driver = connect_history.driver_id
            #         h_bus = connect_history.bus_id

            #         if DispatchRegularlyConnect.objects.filter(driver_id=h_driver).exclude(departure_date__gt=arrival_date).exclude(arrival_date__lt=departure_date).exists():
            #             block_list[date_calculation] = 'y'
            #         elif DispatchRegularlyConnect.objects.filter(bus_id=h_bus).exclude(departure_date__gt=arrival_date).exclude(arrival_date__lt=departure_date).exists():
            #             block_list[date_calculation] = 'y'
            #         else:
            #             block_list[date_calculation] = ''
            
            # context['history_list'] = history_list
            # context['date_list'] = date_list
            # context['block_list'] = block_list

        if selected_group:
            context['group'] = get_object_or_404(Group, id=selected_group)
        else:
            context['group'] = Group.objects.order_by('number','name').first()
        context['date'] = date

        driver_list = Member.objects.filter(Q(role='운전원')|Q(role='팀장')|Q(role='관리자')).filter(use='사용').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]

        

        context['dispatch_list'] = get_date_connect_list(date)
        context['vehicles'] = Vehicle.objects.filter(use='사용').order_by('vehicle_num', 'driver_name')
        context['members'] = Member.objects.exclude(role='최고관리자').filter(use='사용').order_by('name')
        context['group_list'] = Group.objects.all().order_by('number')
        
        
        group_bus_list = []
        group_member_list = []

        for assignment in context['assignment_list']:
            connect = assignment.assignment_connect.filter(start_date__contains=date).first()
            if connect:
                c_bus = connect.bus_id
                c_member = connect.member_id
                
                group_bus_list.append(c_bus)
                group_member_list.append(c_member)
            else:
                group_bus_list.append('')
                group_member_list.append('')
        
        context['group_bus_list'] = group_bus_list
        context['group_member_list'] = group_member_list

        return context


def assignment_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        assignment_data_form = AssignmentDataForm(request.POST)
        if assignment_data_form.is_valid():
            start_time1 = request.POST.get('start_time1')
            start_time2 = request.POST.get('start_time2')
            end_time1 = request.POST.get('end_time1')
            end_time2 = request.POST.get('end_time2')
            week = ' '.join(request.POST.getlist('week', None))

            post_group = request.POST.get('group', None)
            try:
                group = Group.objects.get(pk=post_group)
            except Exception as e:
                group = None

            if len(start_time1) < 2:
                start_time1 = f'0{start_time1}'
            if len(start_time2) < 2:
                start_time2 = f'0{start_time2}'
            if len(end_time1) < 2:
                end_time1 = f'0{end_time1}'
            if len(end_time2) < 2:
                end_time2 = f'0{end_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_allowance = request.POST.get('allowance')
            if post_allowance:
                allowance = int(post_allowance.replace(',',''))
            else:
                allowance = 0

            assignment_data = assignment_data_form.save(commit=False)
            
            num1 = re.sub(r'[^0-9]', '', assignment_data.number1)
            num2 = re.sub(r'[^0-9]', '', assignment_data.number2)
            if num1 == '': num1 = 0
            if num2 == '': num2 = 0
            assignment_data.num1 = num1
            assignment_data.num2 = num2
            assignment_data.week = week
            assignment_data.group = group
            assignment_data.price = price
            assignment_data.allowance = allowance
            assignment_data.start_time = f'{start_time1}:{start_time2}'
            assignment_data.end_time = f'{end_time1}:{end_time2}'
            if assignment_data.end_time < assignment_data.start_time:
                raise BadRequest('출발시간이 도착시간보다 늦습니다.')
            assignment_data.creator = creator
            assignment_data.save()

        assignment_form = AssignmentForm(request.POST)
        if assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.group = group
            assignment.assignment_id = assignment_data
            assignment.edit_date = TODAY
            assignment.num1 = num1
            assignment.num2 = num2
            assignment.price = price
            assignment.allowance = allowance
            assignment.start_time = f'{start_time1}:{start_time2}'
            assignment.end_time = f'{end_time1}:{end_time2}'
            assignment.week = week
            assignment.creator = creator
            assignment.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def assignment_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    if request.method == 'POST':
        id = request.POST.get('id', None)
        assignment_data = get_object_or_404(AssignmentData, pk=id)
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        assignment_form = AssignmentDataForm(request.POST)
        if assignment_form.is_valid():
            start_time1 = request.POST.get('start_time1')
            start_time2 = request.POST.get('start_time2')
            end_time1 = request.POST.get('end_time1')
            end_time2 = request.POST.get('end_time2')
            week = ' '.join(request.POST.getlist('week', None))

            post_group = request.POST.get('group', None)
            try:
                group = Group.objects.get(pk=post_group)
            except Exception as e:
                group = None

            if len(start_time1) < 2:
                start_time1 = f'0{start_time1}'
            if len(start_time2) < 2:
                start_time2 = f'0{start_time2}'
            if len(end_time1) < 2:
                end_time1 = f'0{end_time1}'
            if len(end_time2) < 2:
                end_time2 = f'0{end_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_allowance = request.POST.get('allowance')
            if post_allowance:
                allowance = int(post_allowance.replace(',',''))
            else:
                allowance = 0

            
            assignment_data.start_time = f'{start_time1}:{start_time2}'
            assignment_data.end_time = f'{end_time1}:{end_time2}'
            if assignment_data.end_time < assignment_data.start_time:
                raise BadRequest('출발시간이 도착시간보다 늦습니다.')
                # raise Http404

            assignment_data.week = week
            assignment_data.assignment = assignment_form.cleaned_data['assignment']
            assignment_data.references = assignment_form.cleaned_data['references']
            assignment_data.price = price
            assignment_data.allowance = allowance
            assignment_data.number1 = assignment_form.cleaned_data['number1']
            assignment_data.number2 = assignment_form.cleaned_data['number2']
            assignment_data.num1 = re.sub(r'[^0-9]', '', assignment_form.cleaned_data['number1'])
            assignment_data.num2 = re.sub(r'[^0-9]', '', assignment_form.cleaned_data['number2'])
            assignment_data.location = assignment_form.cleaned_data['location']
            assignment_data.use_vehicle = assignment_form.cleaned_data['use_vehicle']
            assignment_data.group = group
            assignment_data.use = assignment_form.cleaned_data['use']
            assignment_data.creator = creator
            assignment_data.save()

            try:
                assignment = Assignment.objects.filter(assignment_id=assignment_data).get(edit_date=TODAY)
                assignment.group = group
                assignment.edit_date = TODAY
                assignment.assignment = assignment_data.assignment
                assignment.references = assignment_data.references
                assignment.start_time = assignment_data.start_time
                assignment.end_time = assignment_data.end_time
                assignment.price = assignment_data.price
                assignment.allowance = assignment_data.allowance
                assignment.number1 = assignment_data.number1
                assignment.number2 = assignment_data.number2
                assignment.num1 = assignment_data.num1
                assignment.num2 = assignment_data.num2
                assignment.location = assignment_data.location
                assignment.use_vehicle = assignment_data.use_vehicle
                assignment.week = assignment_data.week
                assignment.use = assignment_data.use
                assignment.creator = assignment_data.creator
            except Assignment.DoesNotExist:
                assignment = Assignment(
                    group = group,
                    assignment_id = assignment_data,
                    assignment = assignment_data.assignment,
                    edit_date = TODAY,
                    references = assignment_data.references,
                    start_time = assignment_data.start_time,
                    end_time = assignment_data.end_time,
                    price = assignment_data.price,
                    allowance = assignment_data.allowance,
                    number1 = assignment_data.number1,
                    number2 = assignment_data.number2,
                    num1 = assignment_data.num1,
                    num2 = assignment_data.num2,
                    location = assignment_data.location,
                    use_vehicle = assignment_data.use_vehicle,
                    week = assignment_data.week,
                    type = assignment_data.type,
                    use = assignment_data.use,
                    creator = assignment_data.creator
                )
            assignment.save()
            
            #### 금액, 기사수당 수정 시 입력한 월 이후 배차들 금액, 기사수당 수정
            post_month = request.POST.get('month')
            if post_month:
                day = "01"
                connect_list = AssignmentConnect.objects.filter(assignment_id__assignment_id=assignment_data).filter(start_date__gte=f'{post_month}-{day} 00:00').order_by('start_date')
                for connect in connect_list:
                    month = connect.start_date[:7]
                    member = connect.member_id

                    salary = Salary.objects.filter(member_id=member).get(month=month)                    
                    salary.assignment = int(salary.assignment) + int(allowance) - int(connect.allowance)
                    salary.total = int(salary.total) + int(allowance) - int(connect.allowance)
                    salary.save()

                    # total = TotalPrice.objects.filter(group_id=group).get(month=month)
                    # connect.price = '' 이면 0으로 넣어주기
                    # if not connect.price:
                    #     connect.price = 0
                    # total.total_price = int(total.total_price) + price + math.floor(price * 0.1 + 0.5) - (int(connect.price) + math.floor(int(connect.price) * 0.1 + 0.5))

                    # total.save()

                    connect.price = price
                    connect.allowance = allowance
                    connect.save()

                # post_month 기간의 Assignment 수정
                old_assignment_list = Assignment.objects.filter(assignment_id=assignment_data).filter(edit_date__gte=f'{post_month}-{day} 00:00')
                for assignment in old_assignment_list:
                    assignment.price = price
                    assignment.allowance = allowance
                    assignment.save()
                
                    
            connects = AssignmentConnect.objects.filter(assignment_id__assignment_id=assignment_data).filter(start_date__gte=f'{TODAY} 00:00')
            for connect in connects:
                connect.assignment_id = assignment
                connect.start_date = f'{connect.start_date[:10]} {assignment.start_time}'
                connect.end_date = f'{connect.start_date[:10]} {assignment.end_time}'
                connect.price = assignment.price
                connect.allowance = assignment.allowance
                connect.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else: 
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def assignment_edit_check(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    post_start_time = request.POST.get('departure_time', None)
    post_end_time = request.POST.get('arrival_time', None)
    
    current_page = request.POST.get('current_page')
    pk = request.POST.get('id')
    # 일반업무
    if current_page == 'assignment_data':
        assignment_data = get_object_or_404(AssignmentData, pk=pk)
        assignment = assignment_data.assignment_id.order_by('-edit_date').first()
        connect_list = assignment.assignment_connect.filter(start_date__gte=TODAY)
    # 고정업무
    else:
        assignment = Assignment.objects.get(id=pk)
        connect_list = assignment.assignment_connect.all()

    for connect in connect_list:
        member = connect.member_id
        bus = connect.bus_id

        if current_page == 'assignment_data':
            start_date = f'{connect.start_date[:10]} {post_start_time}'
            end_date = f'{connect.end_date[:10]} {post_end_time}'
        else:
            start_date = post_start_time
            end_date = post_end_time

        if bus:
            connect_bus = AssignmentConnect.objects.filter(bus_id=bus).exclude(end_date__lt=start_date).exclude(start_date__gt=end_date).exclude(id__in=connect_list)
            if connect_bus:
                return JsonResponse({
                    "status": "fail",
                    'route': connect_bus[0].assignment_id.assignment,
                    'driver': connect_bus[0].member_id.name,
                    'bus': connect_bus[0].bus_id.vehicle_num,
                    'departure_date': connect_bus[0].start_date,
                    'arrival_date': connect_bus[0].end_date,
                })
            
        connect_member = AssignmentConnect.objects.filter(member_id=member).exclude(end_date__lt=start_date).exclude(start_date__gt=end_date).exclude(id__in=connect_list)
        if connect_member:
            vehicle_num = connect_member[0].bus_id.vehicle_num if connect_member[0].assignment_id.use_vehicle == '사용' else ''
            return JsonResponse({
                "status": "fail",
                'route': connect_member[0].assignment_id.assignment,
                'driver': connect_member[0].member_id.name,
                'bus': vehicle_num,
                'departure_date': connect_member[0].start_date,
                'arrival_date': connect_member[0].end_date,
            })


        driver = connect.member_id
        
        r_connect_bus = DispatchRegularlyConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=start_date).exclude(departure_date__gt=end_date)
        if r_connect_bus:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_bus[0].regularly_id.route,
                'driver': r_connect_bus[0].driver_id.name,
                'bus': r_connect_bus[0].bus_id.vehicle_num,
                'arrival_date': r_connect_bus[0].arrival_date,
                'departure_date': r_connect_bus[0].departure_date,
            })
        r_connect_driver = DispatchRegularlyConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=start_date).exclude(departure_date__gt=end_date)
        if r_connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_driver[0].regularly_id.route,
                'driver': r_connect_driver[0].driver_id.name,
                'bus': r_connect_driver[0].bus_id.vehicle_num,
                'arrival_date': r_connect_driver[0].arrival_date,
                'departure_date': r_connect_driver[0].departure_date,
            })
        
        o_connect_bus = DispatchOrderConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=start_date).exclude(departure_date__gt=end_date)
        if o_connect_bus:
            return JsonResponse({
                "status": "fail",
                'route': o_connect_bus[0].order_id.route,
                'driver': o_connect_bus[0].driver_id.name,
                'bus': o_connect_bus[0].bus_id.vehicle_num,
                'arrival_date': o_connect_bus[0].arrival_date,
                'departure_date': o_connect_bus[0].departure_date,
            })
        o_connect_driver = DispatchOrderConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=start_date).exclude(departure_date__gt=end_date)
        if o_connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': o_connect_driver[0].order_id.route,
                'driver': o_connect_driver[0].driver_id.name,
                'bus': o_connect_driver[0].bus_id.vehicle_num,
                'arrival_date': o_connect_driver[0].arrival_date,
                'departure_date': o_connect_driver[0].departure_date,
            })
    return JsonResponse({'status': 'success'})

def assignment_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    if request.method == "POST":
        id_list = request.POST.getlist("check")
        group_id = request.POST.get('group', '')
        group = Group.objects.get(id=group_id)
        
        for pk in id_list:
            assignment_data = get_object_or_404(AssignmentData, pk=pk)
            assignment_data.use = '삭제'
            assignment_data.save()

            try:
                assignment = Assignment.objects.filter(assignment_id=assignment_data).get(edit_date=TODAY)
                
                assignment.group = group
                assignment.edit_date = TODAY
                assignment.assignment = assignment_data.assignment
                assignment.references = assignment_data.references
                assignment.start_time = assignment_data.start_time
                assignment.end_time = assignment_data.end_time
                assignment.price = assignment_data.price
                assignment.allowance = assignment_data.allowance
                assignment.number1 = assignment_data.number1
                assignment.number2 = assignment_data.number2
                assignment.num1 = assignment_data.num1
                assignment.num2 = assignment_data.num2
                assignment.location = assignment_data.location
                assignment.use_vehicle = assignment_data.use_vehicle
                assignment.week = assignment_data.week
                assignment.use = assignment_data.use
                assignment.creator = assignment_data.creator
            except Assignment.DoesNotExist:
                assignment = Assignment(
                    group = group,
                    assignment_id = assignment_data,
                    assignment = assignment_data.assignment,
                    edit_date = TODAY,
                    references = assignment_data.references,
                    start_time = assignment_data.start_time,
                    end_time = assignment_data.end_time,
                    price = assignment_data.price,
                    allowance = assignment_data.allowance,
                    number1 = assignment_data.number1,
                    number2 = assignment_data.number2,
                    num1 = assignment_data.num1,
                    num2 = assignment_data.num2,
                    location = assignment_data.location,
                    use_vehicle = assignment_data.use_vehicle,
                    week = assignment_data.week,
                    type = assignment_data.type,
                    use = assignment_data.use,
                    creator = assignment_data.creator
                )
            assignment.save()

            # 오늘부터 미래의 배차 전부 삭제
            connects = AssignmentConnect.objects.filter(assignment_id__assignment_id=assignment_data).filter(start_date__gte=f'{TODAY} 00:00')
            for connect in connects:
                connect.delete()

        return redirect(reverse('assignment:assignment_data') + f'?group={group_id}')
    else:
        return HttpResponseNotAllowed(['post'])

def connect_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        assignment_type = request.POST.get('type', '고정업무')
        creator = get_object_or_404(Member, id=request.session.get('user'))
        pk = request.POST.get('id', None)
        assignment = get_object_or_404(Assignment, id=pk)
        bus = request.POST.get('bus')
        member_id = request.POST.get('member')
        
        member = get_object_or_404(Member, id=member_id)
        allowance = assignment.allowance
        
        date = request.POST.get('date', None)
        
        vehicle = get_object_or_404(Vehicle, id=bus) if bus else None


        try:
            old_connect = assignment.assignment_connect.get(start_date__startswith=date)
            if old_connect.price == assignment.price and old_connect.allowance == allowance:
                same_accounting = True
            else:
                same_accounting = False
            old_connect.same_accounting = same_accounting
            old_connect.delete()
        except:
            same_accounting = False

        start_date = f'{date} {assignment.start_time}' if assignment_type == '고정업무' else assignment.start_time
        end_date = f'{date} {assignment.end_time}' if assignment_type == '고정업무' else assignment.end_time

        connect = AssignmentConnect(
            assignment_id = assignment,
            member_id = member,
            bus_id = vehicle,
            start_date = start_date,
            end_date = end_date,
            price = assignment.price,
            allowance = allowance,
            type = assignment_type,
            creator = creator,
        )
        connect.same_accounting = same_accounting
        connect.save()
        try:
            send_message('업무를 확인해 주세요', f'{assignment.assignment}\n{connect.start_date} ~ {connect.end_date}', member.token, None)
        except Exception as e:
            print(e)
            
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def connect_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    if request.method == "POST":
        check_list = request.POST.getlist('check')
        date = request.POST.get('date')

        for order_id in check_list:
            try:
                order = Assignment.objects.prefetch_related('assignment_connect').get(id=order_id)

                assignment_data = order.assignment_id
                connects = AssignmentConnect.objects.filter(assignment_id__assignment_id=assignment_data).filter(start_date__startswith=date)
                connects.delete()
            
            except AssignmentConnect.DoesNotExist:
                continue

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def temporary_connect_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('date')

        assignment = Assignment.objects.prefetch_related('assignment_connect').get(id=id)
        connects = AssignmentConnect.objects.filter(assignment_id=assignment).filter(start_date__startswith=date)
        connects.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def group_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        group = Group(
            name = request.POST.get('name'),
            number = '999',
            creator = get_object_or_404(Member, pk=request.session['user'])
        )
        group.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def group_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        id = request.POST.get('id', None)
        name = request.POST.get('name', None)
        group = get_object_or_404(Group, id=id)
        group.name = name
        group.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def group_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        group = get_object_or_404(Group, id=request.POST.get('id', None))
        # for r_data in group.regularly.all():
        #     r_data.use = '삭제'
        #     r_data.save()
        
        # for regulalry in group.regularly_monthly.all():
        #     regulalry.use = '삭제'
        #     regulalry.save()

        if not group.assignment_data.exists():
            group.delete()
            
        return redirect('assignment:assignment_data')
    else:
        return HttpResponseNotAllowed(['POST'])

def group_fix(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        
        post_data = json.loads(request.body.decode("utf-8"))

        group_list = post_data['order']
        fix = post_data['fix']
        
        try:
            for i in range(len(group_list)):
                id = group_list[i]
                group = get_object_or_404(Group, id=id)
                group.number = i
                if i+1 > int(fix):
                    group.fix = 'n'
                else:
                    group.fix = 'y'
                
                group.save()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'fail'})
    else:
        return HttpResponseNotAllowed(['POST'])

class TemporaryAssignmentList(generic.ListView):
    template_name = 'assignment/temporary_assignment.html'
    context_object_name = 'assignment_list'
    model = DispatchOrder

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        start_date = self.request.GET.get('date1', TODAY)
        end_date = self.request.GET.get('date2', TODAY)
        search = self.request.GET.get('search')
        search_type = self.request.GET.get('type')

        if start_date or end_date or search:
            assignment_list = Assignment.objects.prefetch_related('assignment_connect').filter(type='일반업무').exclude(end_time__lt=f'{start_date} 00:00').exclude(start_time__gt=f'{end_date} 24:00').order_by('start_time')
            if search_type == 'assignment' and search:
                assignment_list = assignment_list.filter(assignment__contains=search).order_by('start_time')

            elif search_type == 'vehicle' and search:
                assignment_list = assignment_list.filter(assignment_connect__bus_id__vehicle_num__contains=search).order_by('start_time')

        else:            
            assignment_list = Assignment.objects.prefetch_related('assignment_connect').filter(type='일반업무').exclude(end_time__lt=f'{TODAY} 00:00').exclude(start_time__gt=f'{TODAY} 24:00').order_by('start_time')
        
        return assignment_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['date1'] = self.request.GET.get('date1')
        context['date2'] = self.request.GET.get('date2')

        context['search'] = self.request.GET.get('search', '')
        context['search_type'] = self.request.GET.get('type', '')
        date = self.request.GET.get('date1', TODAY)
        
        # date2 = self.request.GET.get('date2', TODAY)
        # weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        detail_id = self.request.GET.get('id')
        if detail_id:
            context['detail'] = get_object_or_404(Assignment, id=detail_id)
            date = context['detail'].start_time[:10]
            date2 = context['detail'].end_time[:10]
            context['detail_connect_list'] = context['detail'].assignment_connect.all()

        driver_list = Member.objects.filter(Q(role='운전원')|Q(role='팀장')|Q(role='관리자')).filter(use='사용').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]

        outsourcing_list = Member.objects.filter(Q(role='용역')|Q(role='임시')).filter(use='사용').values_list('id', 'name')
        context['outsourcing_dict'] = {}
        for outsourcing in outsourcing_list:
            context['outsourcing_dict'][outsourcing[0]] = outsourcing[1]
        #
        #출발일 ~ 도착일 범위로 한번만 돌면서 for문 안에서 현재 connect date 따라서 list에 appned
        filter_date1 = date
        if detail_id:
            filter_date2 = date2
        else:
            filter_date2 = date
        
        detail = context['detail'] if detail_id else ''
        connect_dict = get_multi_date_connect_list(filter_date1, filter_date2, detail)
        
        context['dispatch_list'] = connect_dict['dispatch_list']
        context['dispatch_list2'] = connect_dict['dispatch_list2']
        context['dispatch_data_list'] = connect_dict['dispatch_data_list']
        #
        collect_list = []
        outstanding_list = []

        total = {}
        total['c_bus_cnt'] = 0
        total['bus_cnt'] = 0
        total['driver_allowance'] = 0
        total['price'] = 0
        total['collection_amount'] = 0
        total['outstanding_amount'] = 0
        
        # for order in context['assignment_list']:
        #     total['driver_allowance'] += int(order.allowance)
        #     total['c_bus_cnt'] += int(order.info_order.count())
        #     total['bus_cnt'] += int(order.bus_cnt)
        #     try:
        #         tp = TotalPrice.objects.get(order_id=order)
        #         total_price = int(tp.total_price)
        #         if order.contract_status != '취소':
        #             total['price'] += total_price
        #     # #################### total price 없으면 만들어주기 나중에 주석처리
        #     except TotalPrice.DoesNotExist:
        #         if order.VAT == 'y':
        #             total_price = int(order.price)
        #         else:
        #             total_price = int(order.price) + math.floor(int(order.price) * 0.1 + 0.5)
        #         total = TotalPrice(
        #             order_id = order,
        #             total_price = total_price,
        #             month = order.departure_date[:7],
        #             creator = order.creator
        #         )
        #         total.save()
        #         if order.contract_status != '취소':
        #             total['price'] += total_price
        #     ####################################
        #     collect_amount = Collect.objects.filter(order_id=order).aggregate(Sum('price'))['price__sum']
        #     if collect_amount:
        #         total['collection_amount'] += int(collect_amount)
        #         total['outstanding_amount'] += total_price - int(collect_amount)
        #         collect_list.append(int(collect_amount))
        #         outstanding_list.append(total_price - int(collect_amount))
        #     else:
        #         outstanding_list.append(0)
        #         collect_list.append(0)
    
        group_bus_list = []
        group_member_list = []

        for assignment in context['assignment_list']:
            connect = assignment.assignment_connect.first()
            if connect:
                c_bus = connect.bus_id
                c_member = connect.member_id
                
                group_bus_list.append(c_bus)
                group_member_list.append(c_member)
            else:
                group_bus_list.append('')
                group_member_list.append('')
        
        context['group_bus_list'] = group_bus_list
        context['group_member_list'] = group_member_list
        
        context['vehicles'] = Vehicle.objects.filter(use='사용').order_by('vehicle_num', 'driver_name')
        context['members'] = Member.objects.exclude(role='최고관리자').filter(use='사용').order_by('name')
        context['selected_date1'] = self.request.GET.get('date1')
        context['selected_date2'] = self.request.GET.get('date2')
        return context

def temporary_assignment_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        assignment_form = AssignmentForm(request.POST)

        if assignment_form.is_valid():
            start_date = request.POST.get('start_date')
            start_time1 = request.POST.get('start_time1')
            start_time2 = request.POST.get('start_time2')
            end_date = request.POST.get('end_date')
            end_time1 = request.POST.get('end_time1')
            end_time2 = request.POST.get('end_time2')

            if len(start_time1) < 2:
                start_time1 = f'0{start_time1}'
            if len(start_time2) < 2:
                start_time2 = f'0{start_time2}'
            if len(end_time1) < 2:
                end_time1 = f'0{end_time1}'
            if len(end_time2) < 2:
                end_time2 = f'0{end_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_allowance = request.POST.get('allowance')
            if post_allowance:
                allowance = int(post_allowance.replace(',',''))
            else:
                allowance = 0

            assignment = assignment_form.save(commit=False)

            num1 = re.sub(r'[^0-9]', '', assignment.number1)
            num2 = re.sub(r'[^0-9]', '', assignment.number2)
            if num1 == '': num1 = 0
            if num2 == '': num2 = 0

            assignment.edit_date = TODAY
            assignment.num1 = num1
            assignment.num2 = num2
            assignment.price = price
            assignment.allowance = allowance
            assignment.start_time = f'{start_date} {start_time1}:{start_time2}'
            assignment.end_time = f'{end_date} {end_time1}:{end_time2}'
            assignment.creator = creator
            assignment.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def temporary_assignment_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        post_assignment = get_object_or_404(Assignment, id=request.POST.get('id'))
        assignment_form = AssignmentForm(request.POST, instance=post_assignment)

        if assignment_form.is_valid():
            start_date = request.POST.get('start_date')
            start_time1 = request.POST.get('start_time1')
            start_time2 = request.POST.get('start_time2')
            end_date = request.POST.get('end_date')
            end_time1 = request.POST.get('end_time1')
            end_time2 = request.POST.get('end_time2')

            if len(start_time1) < 2:
                start_time1 = f'0{start_time1}'
            if len(start_time2) < 2:
                start_time2 = f'0{start_time2}'
            if len(end_time1) < 2:
                end_time1 = f'0{end_time1}'
            if len(end_time2) < 2:
                end_time2 = f'0{end_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_allowance = request.POST.get('allowance')
            if post_allowance:
                allowance = int(post_allowance.replace(',',''))
            else:
                allowance = 0

            assignment = assignment_form.save(commit=False)
            print(assignment.id)

            num1 = re.sub(r'[^0-9]', '', assignment.number1)
            num2 = re.sub(r'[^0-9]', '', assignment.number2)
            if num1 == '': num1 = 0
            if num2 == '': num2 = 0

            start_date = f'{start_date} {start_time1}:{start_time2}'
            end_date = f'{end_date} {end_time1}:{end_time2}'

            assignment.edit_date = TODAY
            assignment.num1 = num1
            assignment.num2 = num2
            assignment.price = price
            assignment.allowance = allowance
            assignment.start_time = start_date
            assignment.end_time = end_date
            assignment.creator = creator
            assignment.save()

            connects = assignment.assignment_connect.all()
            for connect in connects:
                connect.start_date = start_date
                connect.end_date = end_date
                connect.price = price
                connect.allowance = allowance
                connect.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def temporary_assignment_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
        
    if request.method == "POST":
        id_list = request.POST.getlist('id', None)
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')

        for id in id_list:
            order = get_object_or_404(Assignment, id=id)
            order.delete()

        return redirect(reverse('assignment:temporary_assignment') + f'?date1={date1}&date2={date2}')
    else:
        return HttpResponseNotAllowed(['post'])
