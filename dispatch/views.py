import json
import math
import pandas as pd
import re
import urllib
import os
import mimetypes

from config.settings import MEDIA_ROOT
from django.db.models import Q, Sum
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm, ConnectForm, RegularlyDataForm
from .models import DispatchCheck, DispatchRegularlyData, DispatchRegularlyWaypoint, Schedule, DispatchOrderConnect, DispatchOrder, DispatchRegularly, RegularlyGroup, DispatchRegularlyConnect, DispatchOrderWaypoint, ConnectRefusal
from accounting.models import Collect, TotalPrice
from crudmember.models import Category, Client
from humanresource.models import Member, Salary
from itertools import chain
from vehicle.models import Vehicle

from datetime import datetime, timedelta, date
# from utill.decorator import option_year_deco



TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]
WEEK2 = ['월', '화', '수', '목', '금', '토', '일', ]

class RegularlyPrintList(generic.ListView):
    template_name = 'dispatch/regularly_print.html'
    context_object_name = 'order_list'
    model = DispatchRegularlyData

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        
        date = self.request.GET.get('date', TODAY)
        group_id = self.request.GET.get('group', '')

        weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        
        if group_id:
            group = RegularlyGroup.objects.get(id=group_id)
        else:
            group = RegularlyGroup.objects.order_by('number','name').first()

        regularly_list = DispatchRegularlyData.objects.filter(group=group).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
        temp = []
        dispatch_list = []
        for regularly in regularly_list:
            # first 확인필요
            dispatch = regularly.monthly.filter(edit_date__lte=date).order_by('-edit_date').first()
            if not dispatch:
                dispatch = regularly.monthly.filter(edit_date__gte=date).order_by('edit_date').first()
                

            if dispatch.use == '사용':
                dispatch_list.append(dispatch)
        return dispatch_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)
        context['date'] = date
        context['weekday'] = WEEK[datetime.strptime(date, FORMAT).weekday()]
        context['group'] = get_object_or_404(RegularlyGroup, id=self.request.GET.get('group', ''))
        
        group_bus_list = []
        group_driver_list = []
        group_outsourcing_list = []
        departure_time_list = []
        arrival_time_list = []
        for order in context['order_list']:
            connect = order.info_regularly.filter(departure_date__contains=date)
            if connect:
                connect = connect[0]
                c_bus = connect.bus_id
                c_outsourcing = ''
                c_driver = ''
                if connect.outsourcing == 'y':
                    c_outsourcing = connect.driver_id
                else:
                    c_driver = connect.driver_id
                
                departure_time_list.append(connect.departure_date[11:])
                arrival_time_list.append(connect.arrival_date[11:])
                group_bus_list.append(c_bus)
                group_driver_list.append(c_driver)
                group_outsourcing_list.append(c_outsourcing)
            else:
                departure_time_list.append('')
                arrival_time_list.append('')
                group_bus_list.append('')
                group_driver_list.append('')
                group_outsourcing_list.append('')
        
        context['departure_time_list'] = departure_time_list
        context['arrival_time_list'] = arrival_time_list
        context['group_bus_list'] = group_bus_list
        context['group_driver_list'] = group_driver_list
        context['group_outsourcing_list'] = group_outsourcing_list
        return context


def order_print(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    date1 = request.GET.get('date1', TODAY)
    date2 = request.GET.get('date2', TODAY)
    order_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{date1} 00:00').exclude(departure_date__gt=f'{date2} 24:00').order_by('departure_date').exclude(contract_status='취소')
    
    collect_list = []
    outstanding_list = []

    for order in order_list:
        total_price = int(TotalPrice.objects.get(order_id=order).total_price)

        collect_amount = Collect.objects.filter(order_id=order).aggregate(Sum('price'))['price__sum']
        if collect_amount:
            collect_list.append(int(collect_amount))
            outstanding_list.append(total_price - int(collect_amount))
        else:
            outstanding_list.append(0)
            collect_list.append(0)
    context = {
        'date1': date1,
        'date2': date2,
        'order_list': order_list,
        'collect_list': collect_list,
        'outstanding_list': outstanding_list,
        
    }
    return render(request, 'dispatch/order_print.html', context)

def calendar_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        date = request.POST.get('date', None)
        try:
            check = DispatchCheck.objects.get(date=date)
            check.creator = creator
            
        except DispatchCheck.DoesNotExist:
            check = DispatchCheck(
                date = date,
                creator = creator,
            )
        check.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def calendar_delete(request):
    if request.method == "POST":
        date = request.POST.get('date', None)
        check = get_object_or_404(DispatchCheck, date=date)
        check.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def schedule_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        date = request.POST.get('date', None)
        content = request.POST.get('content', None)
        creator = get_object_or_404(Member, id=request.session.get('user'))
        schedule = Schedule(
            date=date,
            content=content,
            creator=creator
        )
        schedule.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])
def schedule_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        check_list = request.POST.getlist('check')

        for check in check_list:
            schedule = get_object_or_404(Schedule, id=check)
            schedule.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


class ScheduleList(generic.ListView):
    template_name = 'dispatch/schedule.html'
    context_object_name = 'driver_list'
    model = Member

    def get_queryset(self):
        select = self.request.GET.get('select', None)
        search = self.request.GET.get('search', None)

        if select == 'driver' and search:
            driver_list = Member.objects.prefetch_related('info_driver_id', 'info_regularly_driver_id').filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')|Q(role='임시')).filter(name__contains=search).filter(use='사용').order_by('name')
        elif select == 'vehicle' and search:
            driver_list = Member.objects.prefetch_related('info_driver_id', 'info_regularly_driver_id').filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')|Q(role='임시')).filter(vehicle__vehicle_num__contains=search).filter(vehicle__use='사용').order_by('name')
        else:
            driver_list = Member.objects.prefetch_related('info_driver_id', 'info_regularly_driver_id').filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')|Q(role='임시')).filter(use='사용').order_by('name')
        return driver_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)
        timeline = datetime.strftime(datetime.now(), "%H:%M")
        if date == TODAY:
            context['timeline'] = (int(timeline[:2]) * 60 + int(timeline[3:])) * 0.058
        schedule_list = []

        for driver in context['driver_list']:
            temp = []
            order_list = driver.info_driver_id.exclude(arrival_date__lte=f'{date} 00:00').exclude(departure_date__gte=f'{date} 24:00')
            regulary_list = driver.info_regularly_driver_id.exclude(arrival_date__lte=f'{date} 00:00').exclude(departure_date__gte=f'{date} 24:00')
            
            for o in order_list:
                driver_check = o.check_order_connect
                try:
                    vehicle = o.driver_id.vehicle.vehicle_num
                except Vehicle.DoesNotExist:
                    vehicle = ''
                temp_dict = {
                    'driver': o.driver_id.name,
                    'driver_vehicle': vehicle,
                    'driver_phone_num': o.driver_id.phone_num,
                    'work_type': '일반',
                    'bus': o.bus_id.vehicle_num,
                    'departure_date': o.departure_date,
                    'arrival_date': o.arrival_date,
                    'departure': o.order_id.departure,
                    'arrival': o.order_id.arrival,
                    'wake_t': driver_check.wake_time,
                    'drive_t': driver_check.drive_time,
                    'departure_t': driver_check.departure_time,
                    'check': '',
                    'connect_check': driver_check.connect_check,
                }
                departure_time = datetime.strptime(o.departure_date, "%Y-%m-%d %H:%M")
                check_time1 = datetime.strftime(departure_time - timedelta(hours=1.5), "%H:%M")
                check_time2 = datetime.strftime(departure_time - timedelta(hours=1), "%H:%M")
                check_time3 = datetime.strftime(departure_time - timedelta(minutes=20), "%H:%M")

                if date == TODAY:
                    if timeline > check_time1 and not driver_check.wake_time:
                        temp_dict['check'] = 'x'
                    elif timeline > check_time2 and not driver_check.drive_time:
                        temp_dict['check'] = 'x'
                    elif timeline > check_time3 and not driver_check.departure_time:
                        temp_dict['check'] = 'x'

                temp.append(temp_dict)
            for regularly in regulary_list:
                driver_check = regularly.check_regularly_connect
                try:
                    vehicle = regularly.driver_id.vehicle.vehicle_num
                except ObjectDoesNotExist:
                    vehicle = ''
                temp_dict = {
                    'driver': regularly.driver_id.name,
                    'driver_vehicle': vehicle,
                    'driver_phone_num': regularly.driver_id.phone_num,
                    'departure_date': regularly.departure_date,
                    'bus': regularly.bus_id.vehicle_num,
                    'arrival_date': regularly.arrival_date,
                    'departure': regularly.regularly_id.departure,
                    'arrival': regularly.regularly_id.arrival,
                    'wake_t': driver_check.wake_time,
                    'drive_t': driver_check.drive_time,
                    'departure_t': driver_check.departure_time,
                    'check': '',
                    'connect_check': driver_check.connect_check,
                }
                temp_dict['work_type'] = regularly.work_type

                departure_time = datetime.strptime(regularly.departure_date, "%Y-%m-%d %H:%M")
                check_time1 = datetime.strftime(departure_time - timedelta(hours=1.5), "%H:%M")
                check_time2 = datetime.strftime(departure_time - timedelta(hours=1), "%H:%M")
                check_time3 = datetime.strftime(departure_time - timedelta(minutes=20), "%H:%M")

                if date == TODAY:
                    if timeline > check_time1 and not driver_check.wake_time:
                        temp_dict['check'] = 'x'
                    elif timeline > check_time2 and not driver_check.drive_time:
                        temp_dict['check'] = 'x'
                    elif timeline > check_time3 and not driver_check.departure_time:
                        temp_dict['check'] = 'x'

                temp.append(temp_dict)
            temp.sort(key = lambda x:x['departure_date']) # departure_date를 기준으로 정렬
            if len(temp) != 0:
                schedule_list.append(temp)
        
        sorted_data = sorted(schedule_list, key=lambda x: any(item["connect_check"] == "0" for item in x), reverse=True)
        context['schedule_list'] = sorted_data
        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')
        context['date'] = date
        return context
    
class RefusalList(generic.ListView):
    template_name = 'dispatch/refusal.html'
    context_object_name = 'refusal_list'
    model = ConnectRefusal
    paginate_by = 10

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)
        
    def get_queryset(self):
        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        name = self.request.GET.get('name')
        role = self.request.GET.get('role', '담당업무')

        if date1 > date2:
            raise Http404
        refusal_list = ConnectRefusal.objects.select_related('driver_id').filter(check_date__gte=date1).filter(check_date__lte=date2)

        if name:
            refusal_list = refusal_list.filter(driver_id__name=name)
        if role != '담당업무':
            refusal_list = refusal_list.filter(driver_id__role=role)
        self.num = refusal_list.count()
        return refusal_list

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

        context['num'] = self.num - (current_page - 1) * 10
        context['date1'] = self.request.GET.get('date1', TODAY)
        context['date2'] = self.request.GET.get('date2', TODAY)
        context['name'] = self.request.GET.get('name', '')
        context['role'] = self.request.GET.get('role', '담당업무')
        return context


def refusal_delete(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        del_list = request.POST.getlist('delete_check', '')
        
        for pk in del_list:
            refusal = get_object_or_404(ConnectRefusal, pk=pk)
            refusal.delete()
            # refusal만 삭제하면 되는지? 

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

class DocumentList(generic.ListView):
    template_name = 'dispatch/document.html'
    context_object_name = 'order_list'
    model = DispatchOrder
    paginate_by = 10

    def get_queryset(self):
        date = self.request.GET.get('date', TODAY)
        order_list = DispatchOrder.objects.prefetch_related('info_order').filter(departure_date__lte=f'{date} 24:00').filter(arrival_date__gte=f'{date} 00:00').exclude(contract_status='취소')
        return order_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departure_date = []
        time = []
        num_days = []

        for order in context['order_list']:
            d_y = order.departure_date[0:4]
            d_m = order.departure_date[5:7]
            d_d = order.departure_date[8:10]
            d_t = order.departure_date[11:16]
            d_date = date(int(d_y), int(d_m), int(d_d))
            d_w = WEEK[d_date.weekday()]
            d_y = d_y[2:4]

            a_y = order.arrival_date[0:4]
            a_m = order.arrival_date[5:7]
            a_d = order.arrival_date[8:10]
            a_t = order.arrival_date[11:16]
            a_date = date(int(a_y), int(a_m), int(a_d))
            a_w = WEEK[d_date.weekday()]
            a_y = a_y[2:4]
            
            date_diff = (a_date - d_date) + timedelta(days=1)
            if date_diff.days > 1:
                num_days.append(date_diff.days)
            else:
                num_days.append('')

            departure_date.append(f"{d_y}.{d_m}.{d_d} {d_w}")
            time.append(f"{d_t}~{a_t}")
            # arrival_date.append(f"{a_y}.{a_m}.{a_d} {a_w} {a_t}")

        connect_list = []
        for order in context['order_list']:
            connect_list.append(order.info_order.all())
        context['connect_list'] = connect_list
        context['departure_date'] = departure_date
        context['num_days'] = num_days
        context['time'] = time
        context['date'] = self.request.GET.get('date', TODAY)
        
        return context
    
class RegularlyDispatchList(generic.ListView):
    template_name = 'dispatch/regularly.html'
    context_object_name = 'order_list'
    model = DispatchRegularly

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        date = self.request.GET.get('date', TODAY)
        group_id = self.request.GET.get('group', '')

        weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        
        if group_id:
            group = RegularlyGroup.objects.get(id=group_id)
        else:
            group = RegularlyGroup.objects.order_by('number','name').first()

        if search:
            regularly_list = DispatchRegularlyData.objects.filter(route__contains=search).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
        else:
            regularly_list = DispatchRegularlyData.objects.filter(group=group).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')

        dispatch_list = []
        for regularly in regularly_list:
            # first 확인필요
            dispatch = regularly.monthly.select_related('regularly_id', 'group').filter(edit_date__lte=date).order_by('-edit_date').first()
            if not dispatch:
                dispatch = regularly.monthly.select_related('regularly_id', 'group').filter(edit_date__gte=date).order_by('edit_date').first()
                

            if dispatch.use == '사용':
                dispatch_list.append(dispatch)
        return dispatch_list


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        date = self.request.GET.get('date', TODAY)
        selected_group = self.request.GET.get('group', '')
        detail_id = self.request.GET.get('id')
        if detail_id:
            regularly_data = get_object_or_404(DispatchRegularlyData, id=detail_id)
            context['detail'] = regularly_data.monthly.filter(edit_date__lte=date).order_by('-edit_date').first()
            if not context['detail']:
                context['detail'] = regularly_data.monthly.filter(edit_date__gte=date).order_by('edit_date').first()

            # 지난 배차내역 불러오기
            date_type = datetime.strptime(date, FORMAT)
            int_start_date = date_type - timedelta(days=int(date_type.weekday()) + 8)
            int_start_date = int(date_type.weekday()) + 8
            start_date = date_type - timedelta(days=7) if int_start_date == 14 else date_type - timedelta(days=int_start_date)
            str_end_date = datetime.strftime(start_date + timedelta(days=13), FORMAT)

            str_start_date = datetime.strftime(start_date, FORMAT)
            
            history_list = [''] * 14
            date_list = []
            block_list = ['y'] * 14

            departure_date = f'{date} {context["detail"].departure_time}'
            arrival_date = f'{date} {context["detail"].arrival_time}'

            for i in range(14):
                
                list_date = datetime.strftime(start_date + timedelta(days=i), FORMAT)
                date_list.append(f'{list_date} {WEEK[datetime.strptime(list_date, FORMAT).weekday()]}')
            ##

            regularly_history_list = DispatchRegularlyData.objects.get(monthly=context['detail']).monthly.all()
            for reg in regularly_history_list:
                connect_history_list = reg.info_regularly.filter(departure_date__gte=str_start_date).filter(arrival_date__lte=str_end_date).order_by('departure_date')
                for connect_history in connect_history_list:
                    date_calculation = (datetime.strptime(connect_history.departure_date[:10], FORMAT) - start_date).days
                    history_list[date_calculation] = connect_history
                    # block_list[date_calculation] = ''

                    h_driver = connect_history.driver_id
                    h_bus = connect_history.bus_id

                    if DispatchRegularlyConnect.objects.filter(driver_id=h_driver).exclude(departure_date__gt=arrival_date).exclude(arrival_date__lt=departure_date).exists():
                        block_list[date_calculation] = 'y'
                    elif DispatchRegularlyConnect.objects.filter(bus_id=h_bus).exclude(departure_date__gt=arrival_date).exclude(arrival_date__lt=departure_date).exists():
                        block_list[date_calculation] = 'y'
                    else:
                        block_list[date_calculation] = ''
            
            context['history_list'] = history_list
            context['date_list'] = date_list
            context['block_list'] = block_list

        if selected_group:
            context['group'] = get_object_or_404(RegularlyGroup, id=selected_group)
        else:
            context['group'] = RegularlyGroup.objects.order_by('number','name').first()
        context['date'] = date

        driver_list = Member.objects.filter(Q(role='운전원')|Q(role='팀장')).filter(use='사용').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]
        outsourcing_list = Member.objects.filter(Q(role='용역')|Q(role='임시')).filter(use='사용').values_list('id', 'name')
        context['outsourcing_dict'] = {}
        for outsourcing in outsourcing_list:
            context['outsourcing_dict'][outsourcing[0]] = outsourcing[1]

        r_connect_list = DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        dispatch_list = []
        for rc in r_connect_list:
            dispatch = rc.regularly_id
            data = {
                'work_type': dispatch.work_type,
                'departure_date': rc.departure_date,
                'arrival_date': rc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': rc.week,
                'bus_id': rc.bus_id.id,
                'bus_num': rc.bus_id.vehicle_num,
                'driver_id': rc.driver_id.id,
                'driver_name': rc.driver_id.name,
                'outsourcing': rc.outsourcing,
            }
            dispatch_list.append(data)
        connect_list = DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        for cc in connect_list:
            dispatch = cc.order_id
            data = {
                'work_type': '일반',
                'departure_date': cc.departure_date,
                'arrival_date': cc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': cc.week,
                'bus_id': cc.bus_id.id,
                'bus_num': cc.bus_id.vehicle_num,
                'driver_id': cc.driver_id.id,
                'driver_name': cc.driver_id.name,
                'outsourcing': cc.outsourcing,
            }
            dispatch_list.append(data)

        context['dispatch_list'] = dispatch_list
        #

        context['vehicles'] = Vehicle.objects.filter(use='사용').order_by('vehicle_num', 'driver_name')
        context['group_list'] = RegularlyGroup.objects.all().order_by('number')
        
        #
        group_bus_list = []
        group_driver_list = []
        group_outsourcing_list = []
        departure_time_list = []
        arrival_time_list = []
        for order in context['order_list']:
            connect = order.info_regularly.filter(departure_date__contains=date)
            if connect:
                connect = connect[0]
                c_bus = connect.bus_id
                c_outsourcing = ''
                c_driver = ''
                if connect.outsourcing == 'y':
                    c_outsourcing = connect.driver_id
                else:
                    c_driver = connect.driver_id
                
                departure_time_list.append(connect.departure_date[11:])
                arrival_time_list.append(connect.arrival_date[11:])
                group_bus_list.append(c_bus)
                group_driver_list.append(c_driver)
                group_outsourcing_list.append(c_outsourcing)
            else:
                departure_time_list.append('')
                arrival_time_list.append('')
                group_bus_list.append('')
                group_driver_list.append('')
                group_outsourcing_list.append('')
        
        context['departure_time_list'] = departure_time_list
        context['arrival_time_list'] = arrival_time_list
        context['group_bus_list'] = group_bus_list
        context['group_driver_list'] = group_driver_list
        context['group_outsourcing_list'] = group_outsourcing_list
        return context


def regularly_connect_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        pk = request.POST.get('id', None)
        order = get_object_or_404(DispatchRegularly, id=pk)
        bus = request.POST.get('bus')
        outsourcing_id = request.POST.get('outsourcing')
        driver_id = request.POST.get('driver')
        
        if outsourcing_id:
            outsourcing = 'y'
            driver = get_object_or_404(Member, id=outsourcing_id)
        else:
            outsourcing = 'n'
            driver = get_object_or_404(Member, id=driver_id)
            
        date = request.POST.get('date', None)
        vehicle = get_object_or_404(Vehicle, id=bus)

        try:
            old_connect = order.info_regularly.get(departure_date__startswith=date)
            if old_connect.price == order.price and old_connect.driver_allowance == order.driver_allowance:
                same_accounting = True
            else:
                same_accounting = False
            old_connect.same_accounting = same_accounting
            old_connect.delete()
        except:
            same_accounting = False

        r_connect = DispatchRegularlyConnect(
            regularly_id = order,
            bus_id = vehicle,
            driver_id = driver,
            departure_date = f'{date} {order.departure_time}',
            arrival_date = f'{date} {order.arrival_time}',
            work_type = order.work_type,
            driver_allowance = order.driver_allowance,
            price = order.price,
            outsourcing = outsourcing,
            creator = creator,
        )
        r_connect.same_accounting = same_accounting
        r_connect.save()
        group = request.POST.get('group')
        date = request.POST.get('date')
        return redirect(reverse('dispatch:regularly') + f'?id={order.regularly_id.id}&group={group}&date={date}')
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_connect_load(request, day):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    creator = get_object_or_404(Member, id=request.session.get('user'))
    check_list = request.POST.getlist('check', '')
    if not check_list:
        return JsonResponse({'status': 'check'})
    req_date = request.POST.get('date', TODAY)

    minus_week = day
    date = datetime.strftime(datetime.strptime(req_date, FORMAT) - timedelta(days=minus_week), FORMAT)

    bus_list = []
    driver_list = []
    outsourcing_list = []
    regularly_list = []
    for check in check_list:
        regularly_data = DispatchRegularly.objects.get(id=check).regularly_id

        regularly = regularly_data.monthly.filter(edit_date__lte=date).order_by('-edit_date').first()
        if not regularly:
            regularly = regularly_data.monthly.filter(edit_date__gte=date).order_by('edit_date').first()
                

        cur_connect = DispatchRegularlyConnect.objects.select_related('regularly_id', 'bus_id', 'driver_id').filter(regularly_id__regularly_id=regularly_data).filter(departure_date__startswith=req_date)
        if cur_connect.exists():
            cur_connect_id = cur_connect[0].id
        else:
            # 체크된 노선의 선택된 날짜에 배차가 없을 경우
            cur_connect_id = 0
        try:
            connect = DispatchRegularlyConnect.objects.select_related('regularly_id', 'bus_id', 'driver_id').filter(regularly_id__regularly_id=regularly_data).get(departure_date__startswith=date)
            bus = connect.bus_id
            driver = connect.driver_id
            outsourcing = connect.outsourcing
            
            order_arrival_time = f'{req_date} {regularly.arrival_time}'
            order_departure_time = f'{req_date} {regularly.departure_time}'
            ##################### 노선 정보가 수정됐을때는?
            if DispatchRegularlyConnect.objects.exclude(id=cur_connect_id).filter(driver_id=driver).exclude(departure_date__gt=order_arrival_time).exclude(arrival_date__lt=order_departure_time).exists():
                return JsonResponse({'status': 'overlap', 'route': f'{regularly.number1}-{regularly.number2} {regularly.route}'})

            if DispatchRegularlyConnect.objects.exclude(id=cur_connect_id).filter(bus_id=bus).exclude(departure_date__gt=order_arrival_time).exclude(arrival_date__lt=order_departure_time).exists():
                return JsonResponse({'status': 'overlap', 'route': f'{regularly.number1}-{regularly.number2} {regularly.route}'})
            bus_list.append(bus)
            driver_list.append(driver)
            outsourcing_list.append(outsourcing)
            regularly_list.append(regularly_data)

        except DispatchRegularlyConnect.DoesNotExist:
            bus_list.append('')
            driver_list.append('')
            outsourcing_list.append('')
            regularly_list.append(regularly_data)
            continue
        except MultipleObjectsReturned:
            raise Http404

    
    for i in range(len(check_list)):
        try:
            old_connect = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_list[i]).get(departure_date__startswith=req_date)
            if bus_list[i] and old_connect.price == regularly_list[i].price and old_connect.driver_allowance == regularly_list[i].driver_allowance:
                same_accounting = True
            else:
                same_accounting = False
            old_connect.same_accounting = same_accounting
            old_connect.delete()
        except:
            same_accounting = False

        regularly_id = DispatchRegularly.objects.get(id=check_list[i])
        if bus_list[i]:
            connect = DispatchRegularlyConnect(
                regularly_id = regularly_id,
                bus_id = bus_list[i],
                driver_id = driver_list[i],
                outsourcing = outsourcing_list[i],
                departure_date = f'{req_date} {regularly_list[i].departure_time}',
                arrival_date = f'{req_date} {regularly_list[i].arrival_time}',
                work_type = regularly_list[i].work_type,
                price = regularly_list[i].price,
                driver_allowance = regularly_list[i].driver_allowance,
                creator = creator
            )
            connect.same_accounting = same_accounting
            connect.save()


    return JsonResponse({'status': 'success'})



def regularly_connect_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    if request.method == "POST":
        check_list = request.POST.getlist('check')
        date = request.POST.get('date')

        for order_id in check_list:
            try:
                order = DispatchRegularly.objects.prefetch_related('info_regularly').get(id=order_id)

                regularly_data = order.regularly_id
                connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__startswith=date)
                connects.delete()
            
            except DispatchRegularlyConnect.DoesNotExist:
                continue

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


class RegularlyRouteList(generic.ListView):
    template_name = 'dispatch/regularly_route.html'
    context_object_name = 'order_list'
    # paginate_by = 10
    model = DispatchRegularlyData

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
        
    def get_queryset(self):
        group_id = self.request.GET.get('group', '')
        search = self.request.GET.get('search', '')
        search_use = self.request.GET.get('use', '')


        if not group_id:
            # if search:
            #     return DispatchRegularlyData.objects.filter(Q(departure__contains=search) | Q(arrival__contains=search)).order_by('num1', 'number1', 'num2', 'number2')
            group = RegularlyGroup.objects.order_by('number').first()
            return DispatchRegularlyData.objects.exclude(use='삭제').filter(group=group).order_by('num1', 'number1', 'num2', 'number2')
        else:
            group = get_object_or_404(RegularlyGroup, id=group_id)
            if search_use:
                return DispatchRegularlyData.objects.exclude(use='삭제').filter(use=search_use).filter(group=group).filter(Q(route__contains=search) | Q(departure__contains=search) | Q(arrival__contains=search)).order_by('num1', 'number1', 'num2', 'number2')
            else:
                return DispatchRegularlyData.objects.exclude(use='삭제').filter(group=group).filter(Q(route__contains=search) | Q(departure__contains=search) | Q(arrival__contains=search)).order_by('num1', 'number1', 'num2', 'number2')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        id = self.request.GET.get('id')
        context['search'] = self.request.GET.get('search', '')
        context['search_use'] = self.request.GET.get('use', '')

        if id:
            context['detail'] = get_object_or_404(DispatchRegularlyData, id=id)
            context['waypoint_list'] = DispatchRegularlyWaypoint.objects.filter(regularly_id=context['detail'])
        context['group_list'] = RegularlyGroup.objects.all().order_by('number', 'name')
        group_id = self.request.GET.get('group', '')
        if group_id:
            context['group'] = get_object_or_404(RegularlyGroup, id=group_id)
        elif not self.request.GET.get('new'):
            context['group'] = RegularlyGroup.objects.order_by('number').first()


        ## DispatchRegularlyData 생성하고 반영해야됨
        # dispatch_list = DispatchRegularly.objects.all()
        # for dispatch in dispatch_list:
        #     group = dispatch.group
        #     references = dispatch.references
        #     departure = dispatch.departure
        #     arrival = dispatch.arrival
        #     departure_time = dispatch.departure_time
        #     arrival_time = dispatch.arrival_time
        #     price = dispatch.price
        #     driver_allowance = dispatch.driver_allowance
        #     number1 = dispatch.number1
        #     number2 = dispatch.number2
        #     num1 = dispatch.num1
        #     num2 = dispatch.num2
        #     week = dispatch.week
        #     work_type = dispatch.work_type
        #     route = dispatch.route
        #     location = dispatch.location
        #     detailed_route = dispatch.detailed_route
        #     use = dispatch.use
        #     creator = dispatch.creator

        #     dispatch_data = DispatchRegularlyData(
        #         group = group,
        #         references = references,
        #         departure = departure,
        #         arrival = arrival,
        #         departure_time = departure_time,
        #         arrival_time = arrival_time,
        #         price = price,
        #         driver_allowance = driver_allowance,
        #         number1 = number1,
        #         number2 = number2,
        #         num1 = num1,
        #         num2 = num2,
        #         week = week,
        #         work_type = work_type,
        #         route = route,
        #         location = location,
        #         detailed_route = detailed_route,
        #         use = use,
        #         creator = creator,
        #     )
        #     dispatch_data.save()
        #     dispatch.regularly_id = dispatch_data
        #     dispatch.save()
        
        return context

def regularly_order_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = RegularlyDataForm(request.POST)
        if order_form.is_valid():
            # if datetime.strptime(request.POST.get('contract_start_date'), FORMAT) > datetime.strptime(request.POST.get('contract_end_date'), FORMAT):
            #     context = {}
            #     # context['order_list'] = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')
            #     context['group_list'] = RegularlyGroup.objects.all()
            #     # context['error'] = "출발일이 도착일보다 늦습니다"
            #     #raise BadRequest('출발일이 도착일보다 늦습니다.')
            #     #return render(request, 'dispatch/regularly_order_create.html', context)
            #     raise Http404
            post_group = request.POST.get('group', None)
            try:
                regularly_group = RegularlyGroup.objects.get(pk=post_group)
            except Exception as e:
                regularly_group = None

            week = ' '.join(request.POST.getlist('week', None))
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_driver_allowance = request.POST.get('driver_allowance')
            if post_driver_allowance:
                driver_allowance = int(post_driver_allowance.replace(',',''))
            else:
                driver_allowance = 0

            order = order_form.save(commit=False)
            
            order.num1 = re.sub(r'[^0-9]', '', order.number1)
            order.num2 = re.sub(r'[^0-9]', '', order.number2)
            order.price = price
            order.driver_allowance = driver_allowance
            order.departure_time = f'{departure_time1}:{departure_time2}'
            order.arrival_time = f'{arrival_time1}:{arrival_time2}'
            order.week = week
            order.creator = creator
            order.group = regularly_group
            order.save()
            
            regularly = DispatchRegularly(
                regularly_id = order,
                edit_date = TODAY,
                group = order.group,
                references = order.references,
                departure = order.departure,
                arrival = order.arrival,
                departure_time = order.departure_time,
                arrival_time = order.arrival_time,
                price = order.price,
                driver_allowance = order.driver_allowance,
                number1 = order.number1,
                number2 = order.number2,
                num1 = order.num1,
                num2 = order.num2,
                week = order.week,
                work_type = order.work_type,
                route = order.route,
                location = order.location,
                detailed_route = order.detailed_route,
                maplink = order.maplink,
                use = order.use,
                creator = order.creator
            )
            regularly.save()

            waypoint_list = request.POST.getlist('waypoint')
            for waypoint in waypoint_list:
                regularly_waypoint = DispatchRegularlyWaypoint(
                    regularly_id = order,
                    waypoint = waypoint,
                    creator = order.creator
                )
                regularly_waypoint.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_order_edit_check(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    pk = request.POST.get('id')
    order = get_object_or_404(DispatchRegularlyData, pk=pk)

    post_departure_date = request.POST.get('departure_date', None)
    post_arrival_date = request.POST.get('arrival_date', None)

    regularly = order.monthly.order_by('-edit_date').first()
    connect_list = regularly.info_regularly.filter(departure_date__gte=TODAY)

    for connect in connect_list:
        driver = connect.driver_id
        bus = connect.bus_id
        date = connect.departure_date[:10]
        
        r_connect_bus = DispatchRegularlyConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=f'{date} {post_departure_date}').exclude(departure_date__gt=f'{date} {post_arrival_date}').exclude(id__in=connect_list)
        if r_connect_bus:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_bus[0].regularly_id.route,
                'driver': r_connect_bus[0].driver_id.name,
                'bus': r_connect_bus[0].bus_id.vehicle_num,
                'arrival_date': r_connect_bus[0].arrival_date,
                'departure_date': r_connect_bus[0].departure_date,
            })
        r_connect_driver = DispatchRegularlyConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=f'{date} {post_departure_date}').exclude(departure_date__gt=f'{date} {post_arrival_date}').exclude(id__in=connect_list)
        if r_connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_driver[0].regularly_id.route,
                'driver': r_connect_driver[0].driver_id.name,
                'bus': r_connect_driver[0].bus_id.vehicle_num,
                'arrival_date': r_connect_driver[0].arrival_date,
                'departure_date': r_connect_driver[0].departure_date,
            })
        
        connect_bus = DispatchOrderConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=f'{date} {post_departure_date}').exclude(departure_date__gt=f'{date} {post_arrival_date}').exclude(id__in=connect_list)
        if connect_bus:
            return JsonResponse({
                "status": "fail",
                'route': connect_bus[0].order_id.route,
                'driver': connect_bus[0].driver_id.name,
                'bus': connect_bus[0].bus_id.vehicle_num,
                'arrival_date': connect_bus[0].arrival_date,
                'departure_date': connect_bus[0].departure_date,
            })
        connect_driver = DispatchOrderConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=f'{date} {post_departure_date}').exclude(departure_date__gt=f'{date} {post_arrival_date}').exclude(id__in=connect_list)
        if connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': connect_driver[0].order_id.route,
                'driver': connect_driver[0].driver_id.name,
                'bus': connect_driver[0].bus_id.vehicle_num,
                'arrival_date': connect_driver[0].arrival_date,
                'departure_date': connect_driver[0].departure_date,
            })
        
    
    return JsonResponse({'status': 'success'})

def regularly_order_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    id = request.POST.get('id', None)
    order = get_object_or_404(DispatchRegularlyData, pk=id)
    
    if request.method == 'POST':
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = RegularlyDataForm(request.POST)
        if order_form.is_valid():
            group = get_object_or_404(RegularlyGroup, pk=request.POST.get('group'))
            week = ' '.join(request.POST.getlist('week', None))
            
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_driver_allowance = request.POST.get('driver_allowance')
            if post_driver_allowance:
                driver_allowance = int(post_driver_allowance.replace(',',''))
            else:
                driver_allowance = 0

            order.references = order_form.cleaned_data['references']
            order.departure = order_form.cleaned_data['departure']
            order.arrival = order_form.cleaned_data['arrival']
            order.departure_time = f'{departure_time1}:{departure_time2}'
            order.arrival_time = f'{arrival_time1}:{arrival_time2}'
            if order.arrival_time < order.departure_time:
                #raise BadRequest('출발일이 도착일보다 늦습니다.')
                raise Http404

            order.price = price
            order.driver_allowance = driver_allowance
            order.number1 = order_form.cleaned_data['number1']
            order.number2 = order_form.cleaned_data['number2']
            order.num1 = re.sub(r'[^0-9]', '', order_form.cleaned_data['number1'])
            order.num2 = re.sub(r'[^0-9]', '', order_form.cleaned_data['number2'])
            
            order.work_type = order_form.cleaned_data['work_type']
            order.route = order_form.cleaned_data['route']
            order.location = order_form.cleaned_data['location']
            order.detailed_route = order_form.cleaned_data['detailed_route']
            order.maplink = order_form.cleaned_data['maplink']
            order.use = order_form.cleaned_data['use']
            
            order.week = week
            order.group = group
            order.creator = creator
            order.save()

            try:
                regularly = DispatchRegularly.objects.filter(regularly_id=order).get(edit_date=TODAY)

                regularly.regularly_id = order
                regularly.edit_date = TODAY
                regularly.group = order.group
                regularly.references = order.references
                regularly.departure = order.departure
                regularly.arrival = order.arrival
                regularly.departure_time = order.departure_time
                regularly.arrival_time = order.arrival_time
                regularly.price = order.price
                regularly.driver_allowance = order.driver_allowance
                regularly.number1 = order.number1
                regularly.number2 = order.number2
                regularly.num1 = order.num1
                regularly.num2 = order.num2
                regularly.week = order.week
                regularly.work_type = order.work_type
                regularly.route = order.route
                regularly.location = order.location
                regularly.detailed_route = order.detailed_route
                regularly.maplink = order.maplink
                regularly.use = order.use
                regularly.creator = order.creator
            except DispatchRegularly.DoesNotExist:
                regularly = DispatchRegularly(
                    regularly_id = order,
                    edit_date = TODAY,
                    group = order.group,
                    references = order.references,
                    departure = order.departure,
                    arrival = order.arrival,
                    departure_time = order.departure_time,
                    arrival_time = order.arrival_time,
                    price = order.price,
                    driver_allowance = order.driver_allowance,
                    number1 = order.number1,
                    number2 = order.number2,
                    num1 = order.num1,
                    num2 = order.num2,
                    week = order.week,
                    work_type = order.work_type,
                    route = order.route,
                    location = order.location,
                    detailed_route = order.detailed_route,
                    maplink = order.maplink,
                    use = order.use,
                    creator = order.creator
                )
            regularly.save()
            DispatchRegularlyWaypoint.objects.filter(regularly_id=order).delete()
            waypoint_list = request.POST.getlist('waypoint')
            for waypoint in waypoint_list:
                regularly_waypoint = DispatchRegularlyWaypoint(
                    regularly_id = order,
                    waypoint = waypoint,
                    creator = order.creator
                )
                regularly_waypoint.save()
            

            #### 금액, 기사수당 수정 시 입력한 월 이후 배차들 금액, 기사수당 수정
            post_month = request.POST.get('month')
            if post_month:
                day = order.group.settlement_date
                day = day if int(day) > 9 else f'0{day}'
                connect_list = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=order).filter(departure_date__gte=f'{post_month}-{day} 00:00').order_by('departure_date')
                c_regularly = ''
                for connect in connect_list:
                    month = connect.departure_date[:7]
                    member = connect.driver_id

                    salary = Salary.objects.filter(member_id=member).get(month=month)
                    if connect.work_type == '출근':
                        salary.attendance = int(salary.attendance) + int(driver_allowance) - int(connect.driver_allowance)
                    elif connect.work_type == '퇴근':
                        salary.leave = int(salary.leave) + int(driver_allowance) - int(connect.driver_allowance)
                    salary.total = int(salary.total) + int(driver_allowance) - int(connect.driver_allowance)
                    salary.save()

                    total = TotalPrice.objects.filter(group_id=group).get(month=month)
                    # connect.price = '' 이면 0으로 넣어주기
                    if not connect.price:
                        connect.price = 0
                    total.total_price = int(total.total_price) + price + math.floor(price * 0.1 + 0.5) - (int(connect.price) + math.floor(int(connect.price) * 0.1 + 0.5))

                    total.save()

                    connect.price = price
                    connect.driver_allowance = driver_allowance
                    connect.save()

                    if c_regularly != connect.regularly_id:
                        connect.regularly_id.price = price
                        connect.regularly_id.driver_allowance = driver_allowance
                        connect.regularly_id.save()
                        c_regularly = connect.regularly_id
                    
                    
            connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=order).filter(departure_date__gte=f'{TODAY} 00:00')
            for connect in connects:
                connect.regularly_id = regularly
                connect.departure_date = f'{connect.departure_date[:10]} {regularly.departure_time}'
                connect.arrival_date = f'{connect.departure_date[:10]} {regularly.arrival_time}'
                connect.work_type = regularly.work_type
                connect.price = regularly.price
                connect.driver_allowance = regularly.driver_allowance
                connect.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else: 
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_order_upload(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    # post_data = json.loads(request.body.decode("utf-8"))
    # post_data.get('excel')
    # count = 0
    # for data in post_data:
    #     count = count + 1
    creator = get_object_or_404(Member, pk=request.session['user'])
    post_data = json.loads(request.body)
    
    group_list = RegularlyGroup.objects.values('name')

    count = 1
    for data in post_data:
        overlap = False
        for group in group_list:
            if group['name'] == data['group']:
                overlap = True
            
        if overlap == False:
            return JsonResponse({'error': 'group', 'data': data['group'], 'line': count})
        try:
            if data['group'] and data['route'] and data['departure'] and data['arrival'] and data['number1'] and data['number2'] and data['departure_time'] and data['arrival_time'] and data['work_type'] and data['week'] and data['price'] and data['driver_allowance'] and data['use']:
                pass
        except:
            return JsonResponse({'error': 'required', 'line': count})
        
        count += 1

    count = 0
    #try:
    for data in post_data:
        group = get_object_or_404(RegularlyGroup, name=data['group'])
        if data['id']:
            try:
                regularly_data = DispatchRegularlyData.objects.get(id=data['id'])
            except DispatchRegularlyData.DoesNotExist:
                return JsonResponse({'status': 'fail', 'count': count})
            regularly_data.group = group
            regularly_data.references = data['references']
            regularly_data.departure = data['departure']
            regularly_data.arrival = data['arrival']
            regularly_data.departure_time = data['departure_time']
            regularly_data.arrival_time = data['arrival_time']
            regularly_data.price = data['price']
            regularly_data.driver_allowance = data['driver_allowance']
            regularly_data.number1 = f'{data["number1"]}'
            regularly_data.number2 = f"{data['number2']}"
            regularly_data.num1 = re.sub(r'[^0-9]', '', f'{data["number1"]}')
            regularly_data.num2 = re.sub(r'[^0-9]', '', f"{data['number2']}")
            regularly_data.week = data['week']
            regularly_data.work_type = data['work_type']
            regularly_data.route = data['route']
            regularly_data.location = data['location']
            regularly_data.detailed_route = data['detailed_route']
            regularly_data.maplink = data['maplink']
            regularly_data.use = data['use']
            regularly_data.creator = creator
        else:
            regularly_data = DispatchRegularlyData(
                group = group,
                references = data['references'],
                departure = data['departure'],
                arrival = data['arrival'],
                departure_time = data['departure_time'],
                arrival_time = data['arrival_time'],
                price = data['price'],
                driver_allowance = data['driver_allowance'],
                number1 = f'{data["number1"]}',
                number2 = f"{data['number2']}",
                num1 = re.sub(r'[^0-9]', '', f'{data["number1"]}'),
                num2 = re.sub(r'[^0-9]', '', f"{data['number2']}"),
                week = data['week'],
                work_type = data['work_type'],
                route = data['route'],
                location = data['location'],
                detailed_route = data['detailed_route'],
                maplink = data['maplink'],
                use = data['use'],
                creator = creator,
            )
        regularly_data.save()

        # 경유지 생성
        waypoint_list = data['waypoint'].split(", ")
        for waypoint in waypoint_list:
            DispatchRegularlyWaypoint.objects.create(
                regularly_id = regularly_data,
                waypoint = waypoint,
                creator = creator
            )

        try:
            regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data).get(edit_date=TODAY)
            regularly.regularly_id = regularly_data
            regularly.edit_date = TODAY
            regularly.group = group
            regularly.references = data['references']
            regularly.departure = data['departure']
            regularly.arrival = data['arrival']
            regularly.departure_time = data['departure_time']
            regularly.arrival_time = data['arrival_time']
            regularly.price = data['price']
            regularly.driver_allowance = data['driver_allowance']
            regularly.number1 = f'{data["number1"]}'
            regularly.number2 = f"{data['number2']}"
            regularly.num1 = re.sub(r'[^0-9]', '', f'{data["number1"]}')
            regularly.num2 = re.sub(r'[^0-9]', '', f"{data['number2']}")
            regularly.week = data['week']
            regularly.work_type = data['work_type']
            regularly.route = data['route']
            regularly.location = data['location']
            regularly.detailed_route = data['detailed_route']
            regularly.maplink = data['maplink']
            regularly.use = data['use']
            regularly.creator = creator
        except DispatchRegularly.DoesNotExist:
            regularly = DispatchRegularly(
                regularly_id = regularly_data,
                edit_date = TODAY,
                group = group,
                references = data['references'],
                departure = data['departure'],
                arrival = data['arrival'],
                departure_time = data['departure_time'],
                arrival_time = data['arrival_time'],
                price = data['price'],
                driver_allowance = data['driver_allowance'],
                number1 = f'{data["number1"]}',
                number2 = f"{data['number2']}",
                num1 = re.sub(r'[^0-9]', '', f'{data["number1"]}'),
                num2 = re.sub(r'[^0-9]', '', f"{data['number2']}"),
                week = data['week'],
                work_type = data['work_type'],
                route = data['route'],
                location = data['location'],
                detailed_route = data['detailed_route'],
                maplink = data['maplink'],
                use = data['use'],
                creator = creator
            )
        regularly.save()
        count += 1
    return JsonResponse({'status': 'success', 'count': count})
    #except Exception as e:
    #    return JsonResponse({'status': 'fail', 'count': count, 'error': f'{e}'})

def regularly_order_download(request):
    datalist = list(DispatchRegularlyData.objects.exclude(use='삭제').order_by('group__number', 'group__name', 'num1', 'number1', 'num2', 'number2').values_list('id', 'group_id__name', 'route', 'departure', 'arrival', 'number1', 'number2', 'departure_time', 'arrival_time', 'work_type', 'location', 'week', 'detailed_route', 'maplink', 'price', 'driver_allowance', 'references', 'use'))
    queryset = DispatchRegularlyWaypoint.objects.exclude(regularly_id__use='삭제').order_by('regularly_id__group__number', 'regularly_id__group__name', 'regularly_id__num1', 'regularly_id__number1', 'regularly_id__num2', 'regularly_id__number2').values_list('regularly_id__id', 'waypoint')
    waypoints = []
    previous_id = None
    for regularly_id, waypoint in queryset:
        if regularly_id != previous_id:
            waypoints.append((regularly_id, [waypoint]))
            previous_id = regularly_id
        else:
            waypoints[-1][1].append(waypoint)
    cnt = 0
    i = 0
    for data in datalist:
        data = list(data)
        if len(waypoints) > cnt and data[0] == waypoints[cnt][0]:
            data.insert(14, ', '.join(waypoints[cnt][1]))
            cnt = cnt + 1
        else:
            data.insert(14, '')
        datalist[i] = data
        i = i+1
    try:
        df = pd.DataFrame(datalist, columns=['id', '그룹', '노선명', '출발지', '도착지', '순번1', '순번2', '출발시간', '도착시간', '출/퇴근', '위치', '운행요일', '상세노선', '카카오맵', '경유지', '금액', '기사수당', '참조사항', '사용'])
        url = f'{MEDIA_ROOT}/dispatch/regularlyDataList.xlsx'
        df.to_excel(url, index=False)

        if os.path.exists(url):
            with open(url, 'rb') as fh:
                quote_file_url = urllib.parse.quote('출퇴근노선.xlsx'.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
    except Exception as e:

        return JsonResponse({'status': 'fail', 'e': e})
        raise Http404

def regularly_order_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    if request.method == "POST":
        id_list = request.POST.getlist("check")
        group = request.POST.get('group', '')
        
        for pk in id_list:
            order = get_object_or_404(DispatchRegularlyData, pk=pk)
            order.use = '삭제'
            order.save()


            try:
                regularly = DispatchRegularly.objects.filter(regularly_id=order).get(edit_date=TODAY)

                regularly.regularly_id = order
                regularly.edit_date = TODAY
                regularly.group = order.group
                regularly.references = order.references
                regularly.departure = order.departure
                regularly.arrival = order.arrival
                regularly.departure_time = order.departure_time
                regularly.arrival_time = order.arrival_time
                regularly.price = order.price
                regularly.driver_allowance = order.driver_allowance
                regularly.number1 = order.number1
                regularly.number2 = order.number2
                regularly.num1 = order.num1
                regularly.num2 = order.num2
                regularly.week = order.week
                regularly.work_type = order.work_type
                regularly.route = order.route
                regularly.location = order.location
                regularly.detailed_route = order.detailed_route
                regularly.use = order.use
                regularly.creator = order.creator
            except DispatchRegularly.DoesNotExist:
                regularly = DispatchRegularly(
                    regularly_id = order,
                    edit_date = TODAY,
                    group = order.group,
                    references = order.references,
                    departure = order.departure,
                    arrival = order.arrival,
                    departure_time = order.departure_time,
                    arrival_time = order.arrival_time,
                    price = order.price,
                    driver_allowance = order.driver_allowance,
                    number1 = order.number1,
                    number2 = order.number2,
                    num1 = order.num1,
                    num2 = order.num2,
                    week = order.week,
                    work_type = order.work_type,
                    route = order.route,
                    location = order.location,
                    detailed_route = order.detailed_route,
                    use = order.use,
                    creator = order.creator
                )
            regularly.save()

            # 오늘부터 미래의 배차 전부 삭제
            connects = DispatchRegularlyConnect.objects.filter(regularly_id=regularly).filter(departure_date__gte=f'{TODAY} 00:00')
            for connect in connects:
                connect.delete()

        return redirect(reverse('dispatch:regularly_route') + f'?group={group}')
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_group_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        group = RegularlyGroup(
            name = request.POST.get('name'),
            number = '999',
            settlement_date = request.POST.get('settlement_date'),
            creator = get_object_or_404(Member, pk=request.session['user'])
        )
        group.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        id = request.POST.get('id', None)
        name = request.POST.get('name', None)
        settlement_date = request.POST.get('settlement_date')
        group = get_object_or_404(RegularlyGroup, id=id)
        
        group.settlement_date = settlement_date
        group.name = name
        group.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        group = get_object_or_404(RegularlyGroup, id=request.POST.get('id', None))
        # for r_data in group.regularly.all():
        #     r_data.use = '삭제'
        #     r_data.save()
        
        # for regulalry in group.regularly_monthly.all():
        #     regulalry.use = '삭제'
        #     regulalry.save()

        if not group.regularly.exists():
            group.delete()
            
        return redirect('dispatch:regularly_route')
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_fix(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        
        post_data = json.loads(request.body.decode("utf-8"))

        group_list = post_data['order']
        fix = post_data['fix']
        
        try:
            for i in range(len(group_list)):
                id = group_list[i]
                group = get_object_or_404(RegularlyGroup, id=id)
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

class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_list'
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
        # customer = self.request.GET.get('customer')
        # self.next_week = (datetime.strptime(TODAY, FORMAT) + timedelta(days=7)).strftime(FORMAT)

        if start_date or end_date or search:
            
            dispatch_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{start_date} 00:00').exclude(departure_date__gt=f'{end_date} 24:00').order_by('departure_date')
            if search_type == 'customer' and search:
                dispatch_list = dispatch_list.filter(customer__contains=search).order_by('departure_date')
                    
            elif search_type == 'route' and search:
                dispatch_list = dispatch_list.filter(route__contains=search).order_by('departure_date')

            elif search_type == 'vehicle' and search:
                dispatch_list = dispatch_list.filter(info_order__bus_id__vehicle_num__contains=search).order_by('departure_date')

        else:            
            dispatch_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{TODAY} 00:00').exclude(departure_date__gt=f'{TODAY} 24:00').order_by('departure_date')
        
        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cancle_list = context['order_list'].filter(contract_status='취소')
        context['order_list'] = list(context['order_list'].exclude(contract_status='취소')) + list(cancle_list)

        context['date1'] = self.request.GET.get('date1')
        context['date2'] = self.request.GET.get('date2')

        context['search'] = self.request.GET.get('search', '')
        context['search_type'] = self.request.GET.get('type', '')
        date = self.request.GET.get('date1', TODAY)
        
        # date2 = self.request.GET.get('date2', TODAY)
        # weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        detail_id = self.request.GET.get('id')
        if detail_id:
            context['detail'] = get_object_or_404(DispatchOrder, id=detail_id)
            date = context['detail'].departure_date[:10]
            date2 = context['detail'].arrival_date[:10]
            context['detail_connect_list'] = context['detail'].info_order.all()
            context['detail_connect_cnt'] = int(context['detail'].bus_cnt) - int(context['detail_connect_list'].count())

        driver_list = Member.objects.filter(Q(role='운전원')|Q(role='팀장')).filter(use='사용').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]

        outsourcing_list = Member.objects.filter(Q(role='용역')|Q(role='임시')).filter(use='사용').values_list('id', 'name')
        context['outsourcing_dict'] = {}
        for outsourcing in outsourcing_list:
            context['outsourcing_dict'][outsourcing[0]] = outsourcing[1]
        #
        #출발일 ~ 도착일 범위로 한번만 돌면서 for문 안에서 현재 connect date 따라서 list에 appned
        if detail_id:
            r_connect_list = DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date2} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        else:
            r_connect_list = DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        dispatch_list = []
        dispatch_list2 = []
        dispatch_data_list = []
        for rc in r_connect_list:
            dispatch = rc.regularly_id
            data = {
                'work_type': dispatch.work_type,
                'departure_date': rc.departure_date,
                'arrival_date': rc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': rc.week,
                'bus_id': rc.bus_id.id,
                'bus_num': rc.bus_id.vehicle_num,
                'driver_id': rc.driver_id.id,
                'driver_name': rc.driver_id.name,
                'outsourcing': rc.outsourcing,
            }
            if detail_id:
                if context['detail'].departure_date[:10] in rc.arrival_date[:10]:
                    dispatch_list.append(data)
                elif context['detail'].arrival_date[:10] in rc.departure_date[:10]:
                    dispatch_list2.append(data)
                
            dispatch_data_list.append(data)
                
                
        if detail_id:
            connect_list = DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date2} 24:00').exclude(arrival_date__lt=f'{date} 00:00')    
        else:
            connect_list = DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')

        for cc in connect_list:
            dispatch = cc.order_id
            data = {
                'work_type': '일반',
                'departure_date': cc.departure_date,
                'arrival_date': cc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': cc.week,
                'bus_id': cc.bus_id.id,
                'bus_num': cc.bus_id.vehicle_num,
                'driver_id': cc.driver_id.id,
                'driver_name': cc.driver_id.name,
                'outsourcing': cc.outsourcing,
            }
            if detail_id:
                if context['detail'].departure_date[:10] in dispatch.arrival_date[:10]:
                    dispatch_list.append(data)
                elif context['detail'].arrival_date[:10] in dispatch.departure_date[:10]:
                    dispatch_list2.append(data)
            
            dispatch_data_list.append(data)

        context['dispatch_list'] = dispatch_list
        context['dispatch_list2'] = dispatch_list2
        context['dispatch_data_list'] = dispatch_data_list
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
        
        for order in context['order_list']:
            if order.contract_status != '취소':
                total['driver_allowance'] += int(order.driver_allowance) * int(order.bus_cnt)
                total['c_bus_cnt'] += int(order.info_order.count())
                total['bus_cnt'] += int(order.bus_cnt)
            try:
                tp = TotalPrice.objects.get(order_id=order)
                total_price = int(tp.total_price)
                if order.contract_status != '취소':
                    total['price'] += total_price
            # #################### total price 없으면 만들어주기 나중에 주석처리
            except TotalPrice.DoesNotExist:
                if order.VAT == 'y':
                    total_price = int(order.price) * int(order.bus_cnt)
                else:
                    total_price = int(order.price) * int(order.bus_cnt) + math.floor(int(order.price) * int(order.bus_cnt) * 0.1 + 0.5)
                total = TotalPrice(
                    order_id = order,
                    total_price = total_price,
                    month = order.departure_date[:7],
                    creator = order.creator
                )
                total.save()
                if order.contract_status != '취소':
                    total['price'] += total_price
            ####################################
            collect_amount = Collect.objects.filter(order_id=order).aggregate(Sum('price'))['price__sum']
            if collect_amount:
                total['collection_amount'] += int(collect_amount)
                total['outstanding_amount'] += total_price - int(collect_amount)
                collect_list.append(int(collect_amount))
                outstanding_list.append(total_price - int(collect_amount))
            else:
                outstanding_list.append(0)
                collect_list.append(0)
            
            
        context['total'] = total
        
        context['vehicles'] = Vehicle.objects.filter(use='사용').order_by('vehicle_num', 'driver_name')
        context['selected_date1'] = self.request.GET.get('date1')
        context['selected_date2'] = self.request.GET.get('date2')
        context['collect_list'] = collect_list
        context['outstanding_list'] = outstanding_list

        context['client'] = []
        for client in Client.objects.all().values('name', 'phone', 'note').order_by('name'):
            context['client'].append(client)

        
        
        context['vehicle_types'] = Category.objects.filter(type='차량종류')
        context['operation_types'] = Category.objects.filter(type='운행종류')
        context['order_types'] = Category.objects.filter(type='유형')
        context['bill_places'] = Category.objects.filter(type='계산서 발행처')
        context['reservations'] = Category.objects.filter(type='예약회사')
        context['operatings'] = Category.objects.filter(type='운행회사')
        
        return context

def order_connect_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        order = get_object_or_404(DispatchOrder, id=request.POST.get('id', None))
        if order.contract_status == '취소':
            raise Http404
        price = order.price
        outsourcing_list = []
        payment_method_list = []
        for i in range(int(order.bus_cnt)):
            outsourcing_id = request.POST.get(f'outsourcing{i}', '')
            outsourcing_list.append(outsourcing_id)

            post_payment_method = request.POST.get(f'payment_method{i}', '')
            payment_method_list.append(post_payment_method)
        

        bus_list = request.POST.getlist('bus')
        driver_list = request.POST.getlist('driver')
        driver_allowance_list = request.POST.getlist('driver_allowance')

        connect = order.info_order.all()
        connect.delete()
        count = 0
        for bus, driver_id in zip(bus_list, driver_list):
            if not bus:
                continue
            vehicle = Vehicle.objects.get(id=bus)
            if outsourcing_list[count]:
                driver = Member.objects.get(id=outsourcing_list[count])
                outsourcing = 'y'
            else:
                driver = Member.objects.get(id=driver_id)
                outsourcing = 'n'
            
            allowance = driver_allowance_list[count].replace(",","")
            
            payment_method = payment_method_list[count]
            if not payment_method:
                payment_method = 'n'
            
            connect = DispatchOrderConnect(
                order_id = order,
                bus_id = vehicle,
                driver_id = driver,
                payment_method = payment_method,
                outsourcing = outsourcing,
                departure_date = order.departure_date,
                arrival_date = order.arrival_date,
                driver_allowance = allowance,
                price = price,
                creator = creator,
            )
            connect.save()
            count = count + 1
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponseNotAllowed(['post'])


def order_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)
        waypoint_list = request.POST.getlist('waypoint')
        waypoint_time_list = request.POST.getlist('waypoint_time')
        delegate_list = request.POST.getlist('delegate')
        delegate_phone_list = request.POST.getlist('delegate_phone')

        if order_form.is_valid() and len(waypoint_list) == len(waypoint_time_list):
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'
            
            if request.POST.get('price'):
                price = int(request.POST.get('price').replace(',',''))
            else:
                price = 0
            if request.POST.get('driver_allowance'):
                driver_allowance = int(request.POST.get('driver_allowance').replace(',',''))
            else:
                driver_allowance = 0

            order = order_form.save(commit=False)
            order.price = price
            order.driver_allowance = driver_allowance
            order.VAT = request.POST.get('VAT', 'n')
            order.creator = creator

            # 현지수금(카드)
            post_collection_type = request.POST.get('collection_type')
            
            if post_collection_type:
                if post_collection_type == '계좌이체':
                    order.collection_type = '계좌이체'
                    order.payment_method = '계좌이체'
                else:
                    order.collection_type = post_collection_type.split('(')[0]
                    order.payment_method = post_collection_type.split('(')[1][:-1]
            

            order.cost_type = ' '.join(request.POST.getlist('cost_type'))
            option = ' '.join(request.POST.getlist('option'))
            order.option = option
            if '카드기' in option and (not '<카드기>' in order.departure):
                order.departure = '<카드기>' + order.departure
            if '카시트' in option and (not '<카시트>' in order.departure):
                order.departure = '<카시트>' + order.departure
            if '음향' in option and (not '<음향>' in order.departure):
                order.departure = '<음향>' + order.departure

            order.departure_date = f"{request.POST.get('departure_date')} {departure_time1}:{departure_time2}"
            order.arrival_date = f"{request.POST.get('arrival_date')} {arrival_time1}:{arrival_time2}"
            order.route = request.POST.get('departure') + " ▶ " + request.POST.get('arrival')
            order.save()

            for i in range(len(waypoint_list)):
                waypoint = DispatchOrderWaypoint(
                    order_id=order,
                    waypoint=waypoint_list[i],
                    time=waypoint_time_list[i],
                    delegate=delegate_list[i] if delegate_list[i] != " " else '',
                    delegate_phone=delegate_phone_list[i] if delegate_phone_list[i] != " " else '',
                    creator=creator,
                )
                waypoint.save()

            return redirect(reverse('dispatch:order') + f'?date1={request.POST.get("departure_date")}&date2={request.POST.get("arrival_date")}')
        else:
            raise BadRequest
    else:
        return HttpResponseNotAllowed(['post'])

def order_edit_check(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
        

    pk = request.POST.get('id')
    order = get_object_or_404(DispatchOrder, pk=pk)
    #
    connects = order.info_order.all()
    # r_connects = order.info_regularly.all()
    post_departure_date = request.POST.get('departure_date', None)
    post_arrival_date = request.POST.get('arrival_date', None)

    for connect in connects:
        bus = connect.bus_id
        driver = connect.driver_id
        # r_connects = bus.info_regularly_bus_id.all()

        format = '%Y-%m-%d %H:%M'
        if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
            raise Http404
        o_connect = bus.info_bus_id.exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date).exclude(id__in=connects)
        if o_connect:
            return JsonResponse({
                "status": "fail",
                'route': o_connect[0].order_id.route,
                'driver': o_connect[0].driver_id.name,
                'bus': o_connect[0].bus_id.vehicle_num,
                'arrival_date': o_connect[0].arrival_date,
                'departure_date': o_connect[0].departure_date,
            })
        o_connect_driver = DispatchOrderConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date).exclude(id__in=connects)
        if o_connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': o_connect_driver[0].order_id.route,
                'driver': o_connect_driver[0].driver_id.name,
                'bus': o_connect_driver[0].bus_id.vehicle_num,
                'arrival_date': o_connect_driver[0].arrival_date,
                'departure_date': o_connect_driver[0].departure_date,
            })
        r_connect = bus.info_regularly_bus_id.exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date)
        if r_connect:
            return JsonResponse({
                "status": "fail",
                'route': r_connect[0].regularly_id.route,
                'driver': r_connect[0].driver_id.name,
                'bus': r_connect[0].bus_id.vehicle_num,
                'arrival_date': r_connect[0].arrival_date,
                'departure_date': r_connect[0].departure_date,
                })
        r_connect_driver = DispatchRegularlyConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date)
        if r_connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_driver[0].regularly_id.route,
                'driver': r_connect_driver[0].driver_id.name,
                'bus': r_connect_driver[0].bus_id.vehicle_num,
                'arrival_date': r_connect_driver[0].arrival_date,
                'departure_date': r_connect_driver[0].departure_date,
                })
    
    return JsonResponse({'status': 'success', 'departure_date': post_departure_date, 'arrival_date': post_arrival_date})

def order_edit(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
        

    pk = request.POST.get('id')
    order = get_object_or_404(DispatchOrder, pk=pk)
    
    if request.method == 'POST':
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)

        waypoint_list = request.POST.getlist('waypoint')
        waypoint_time_list = request.POST.getlist('waypoint_time')
        delegate_list = request.POST.getlist('delegate')
        delegate_phone_list = request.POST.getlist('delegate_phone')


        if order_form.is_valid():
            post_departure_date = request.POST.get('departure_date', None)
            post_arrival_date = request.POST.get('arrival_date', None)
            
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'

            departure_date = f'{post_departure_date} {departure_time1}:{departure_time2}'
            arrival_date = f'{post_arrival_date} {arrival_time1}:{arrival_time2}'
            format = '%Y-%m-%d'
            if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
                raise Http404

            if request.POST.get('price'):
                price = int(request.POST.get('price').replace(',',''))
            else:
                price = 0
            if request.POST.get('driver_allowance'):
                driver_allowance = int(request.POST.get('driver_allowance').replace(',',''))
            else:
                driver_allowance = 0

            order.operation_type = order_form.cleaned_data['operation_type']
            order.references = order_form.cleaned_data['references']
            order.departure = order_form.cleaned_data['departure']
            order.arrival = order_form.cleaned_data['arrival']
            order.departure_date = departure_date
            order.arrival_date = arrival_date
            order.bus_type = order_form.cleaned_data['bus_type']
            order.bus_cnt = order_form.cleaned_data['bus_cnt']
            order.price = price
            order.driver_allowance = driver_allowance
            order.contract_status = order_form.cleaned_data['contract_status']
            order.cost_type = ' '.join(request.POST.getlist('cost_type'))
            
            connects = order.info_order.all()
            if order.contract_status == '취소':
                connects.delete()
            else:
                for connect in connects:
                    connect.departure_date = departure_date
                    connect.arrival_date = arrival_date
                    connect.price = order.price
                    connect.driver_allowance = order.driver_allowance
                    connect.save()

            option = ' '.join(request.POST.getlist('option'))
            order.option = option
            if '카드기' in option and (not '<카드기>' in order.departure):
                order.departure = '<카드기>' + order.departure
            elif not '카드기' in option and '<카드기>' in order.departure:
                order.departure = order.departure.replace('<카드기>','')

            if '카시트' in option and (not '<카시트>' in order.departure):
                order.departure = '<카시트>' + order.departure
            elif not '카시트' in option and '<카시트>' in order.departure:
                order.departure = order.departure.replace('<카시트>','')

            if '음향' in option and (not '<음향>' in order.departure):
                order.departure = '<음향>' + order.departure
            elif not '음향' in option and '<음향>' in order.departure:
                order.departure = order.departure.replace('<음향>','')

            order.customer = order_form.cleaned_data['customer']
            order.customer_phone = order_form.cleaned_data['customer_phone']
            order.bill_place = order_form.cleaned_data['bill_place']
            order.ticketing_info = order_form.cleaned_data['ticketing_info']
            order.order_type = order_form.cleaned_data['order_type']
            order.operating_company = order_form.cleaned_data['operating_company']
            order.reservation_company = order_form.cleaned_data['reservation_company']
            order.driver_lease = order_form.cleaned_data['driver_lease']
            order.vehicle_lease = order_form.cleaned_data['vehicle_lease']

            # 현지수금(카드)
            post_collection_type = request.POST.get('collection_type')
            if post_collection_type:
                if post_collection_type == '계좌이체':
                    order.collection_type = post_collection_type
                    order.payment_method = post_collection_type
                else:
                    order.collection_type = post_collection_type.split('(')[0]
                    order.payment_method = post_collection_type.split('(')[1][:-1]
            
            order.VAT = request.POST.get('VAT', 'n')
            order.route = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            order.creator = creator
            order.save()

            # 경유지 처리
            order.waypoint.all().delete()

            for i in range(len(waypoint_list)):
                waypoint = DispatchOrderWaypoint(
                    order_id=order,
                    waypoint=waypoint_list[i],
                    time=waypoint_time_list[i],
                    delegate=delegate_list[i] if delegate_list[i] != " " else '',
                    delegate_phone=delegate_phone_list[i] if delegate_phone_list[i] != " " else '',
                    creator=creator,
                )
                waypoint.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def order_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
        
    if request.method == "POST":
        id_list = request.POST.getlist('id', None)
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')

        for id in id_list:
            order = get_object_or_404(DispatchOrder, id=id)
            order.delete()

        return redirect(reverse('dispatch:order') + f'?date1={date1}&date2={date2}')
    else:
        return HttpResponseNotAllowed(['post'])

def line_print(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    context = {}
    date = request.GET.get('date')
    week = WEEK[datetime.strptime(date, FORMAT).weekday()][1]
    
    
    
    

    regularly_list = DispatchRegularly.objects.prefetch_related('info_regularly').exclude(info_regularly=None).filter(use='사용').filter(week__contains=week).order_by('group', 'num1', 'number1', 'num2', 'number2')
    
    # regularly_data_list를 regularly_list 대신에 쓸 수 있게 수정해야됨
    # info_regularly = none인것들 빼야됨
    regulalry_data_list = DispatchRegularlyData.objects.filter(use='사용').filter(week__contains=week).order_by('group','num1', 'number1', 'num2', 'number2')
    
    regularly_list = []
    no_list = []
    for regularly in regulalry_data_list:
        # first 확인필요
        dispatch = regularly.monthly.prefetch_related('info_regularly').filter(edit_date__lte=date).order_by('-edit_date').first()
        if not dispatch:
            dispatch = regularly.monthly.prefetch_related('info_regularly').filter(edit_date__gte=date).order_by('edit_date').first()
            
        dispatch_connect = dispatch.info_regularly.filter(departure_date__startswith=date).exists()
        if dispatch.use == '사용' and dispatch_connect:
            regularly_list.append(dispatch)

        # 미지정된 노선 목록
        if not dispatch_connect:
            no_list.append(dispatch)
    
    temp = []
    temp2 = []
    
    group = ''
    context['regularly_list'] = []
    context['connect_list'] = []
    for r in regularly_list:
        if r.group.name != group:
            group = r.group.name
            if r != regularly_list[0]:
                context['regularly_list'].append(temp)
                context['connect_list'].append(temp2)
                temp = []
                temp2 = []
        
        temp.append(r)
        regularly_connect = r.info_regularly.filter(departure_date__startswith=date)
        temp2.append(regularly_connect)

    if r == regularly_list[len(regularly_list)-1]:
        context['regularly_list'].append(temp)
        context['connect_list'].append(temp2)

    context['no_list'] = no_list

    return render(request, 'dispatch/line_print.html', context)

def bus_print(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    context = {}
    date = request.GET.get('date')

    vehicle_list = Vehicle.objects.filter(use='사용').order_by('vehicle_num')
    context['vehicle_list'] = vehicle_list
    
    connect_object = {}
    e_connect_object = {}
    c_connect_object = {}
    for vehicle in vehicle_list:
        connect_object[vehicle.id] = []
        e_connect_object[vehicle.id] = []
        c_connect_object[vehicle.id] = []

    r_connect_list = DispatchRegularlyConnect.objects.select_related('bus_id', 'regularly_id').filter(departure_date__startswith=date).order_by('departure_date')
    for connect in r_connect_list:
        if connect.work_type == "출근":
            e_connect_object[connect.bus_id.id].append(connect)
        elif connect.work_type == "퇴근":
            c_connect_object[connect.bus_id.id].append(connect)

    connect_list = DispatchOrderConnect.objects.select_related('bus_id', 'order_id').filter(departure_date__lte=f'{date} 24:00').filter(arrival_date__gte=f'{date} 00:00')
    for connect in connect_list:
        connect_object[connect.bus_id.id].append(connect)


    context['connect_object'] = connect_object
    context['e_connect_object'] = e_connect_object
    context['c_connect_object'] = c_connect_object
    return render(request, 'dispatch/bus_print.html', context)

def daily_driving_list(request):
    context = {}
    date = request.GET.get('date')

    if request.session.get('authority') > 3:
        member_list = Member.objects.filter(id=request.session.get('user'))
    else:
        # member_list = Member.objects.filter(use='사용').filter(authority__gte=3)
        member_list = Member.objects.filter(authority__gte=3)
    
    connect_object = {}
    e_connect_object = {}
    c_connect_object = {}
    for member in member_list:
        connect_object[member.id] = []
        e_connect_object[member.id] = []
        c_connect_object[member.id] = []
    
    if request.session.get('authority') > 3:
        r_connect_list = DispatchRegularlyConnect.objects.select_related('driver_id').filter(driver_id=member_list[0]).filter(departure_date__startswith=date).order_by('departure_date')
    else:
        r_connect_list = DispatchRegularlyConnect.objects.select_related('driver_id').filter(departure_date__startswith=date).order_by('departure_date')
    for connect in r_connect_list:
        if connect.work_type == "출근":
            e_connect_object[connect.driver_id.id].append(connect)
        elif connect.work_type == "퇴근":
            c_connect_object[connect.driver_id.id].append(connect)

    if request.session.get('authority') > 3:
        connect_list = DispatchOrderConnect.objects.select_related('bus_id', 'order_id').filter(driver_id=member_list[0]).filter(departure_date__lte=f'{date} 24:00').filter(arrival_date__gte=f'{date} 00:00')
    else:
        connect_list = DispatchOrderConnect.objects.select_related('bus_id', 'order_id').filter(departure_date__lte=f'{date} 24:00').filter(arrival_date__gte=f'{date} 00:00')
    for connect in connect_list:
        connect_object[connect.driver_id.id].append(connect)

    context['connect_object'] = connect_object
    context['e_connect_object'] = e_connect_object
    context['c_connect_object'] = c_connect_object
    context['member_list'] = member_list
    context['date'] = date
    return render(request, 'dispatch/daily_driving_list.html', context)

def daily_driving_print(request):
    if request.session.get('authority') > 3:
        id_list = [request.session.get('user')]
    else:
        id_list = request.GET.get('id').split(',')

    date = request.GET.get('date')
    context = {}
    context['member_list'] = []
    context['order_list'] = []
    context['e_order_list'] = []
    context['c_order_list'] = []
    context['accompany_list'] = []
    context['cnt'] = len(id_list)
    context['date'] = date

    for id in id_list:
        if id and date:
            member = get_object_or_404(Member, id=id)
            context['member_list'].append(member)
            context['e_order_list'].append(DispatchRegularlyConnect.objects.select_related('regularly_id').filter(departure_date__startswith=date).filter(work_type="출근").filter(driver_id=member).order_by('departure_date'))
            context['c_order_list'].append(DispatchRegularlyConnect.objects.select_related('regularly_id').filter(departure_date__startswith=date).filter(work_type="퇴근").filter(driver_id=member).order_by('departure_date'))
            order_list = DispatchOrderConnect.objects.select_related('order_id').filter(departure_date__lte=f'{date} 24:00').filter(arrival_date__gte=f'{date} 00:00').filter(driver_id=member).order_by('departure_date')
            context['order_list'].append(order_list)

            temp = []
            for order in order_list:
                connect_list = order.order_id.info_order.all()
                if connect_list.count() > 1:
                    temp.append(connect_list.values('departure_date', 'driver_id__name', 'bus_id__vehicle_num'))
                else:
                    temp.append('')

            context['accompany_list'].append(temp)


        else:
            raise Http404



    return render(request, 'dispatch/daily_driving_print.html', context)
    

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@