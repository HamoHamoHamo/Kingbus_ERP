import json
import math
import pandas as pd
import re
import urllib
import os
import mimetypes
import requests

from config.settings import MEDIA_ROOT
from django.db.models import Q, Sum
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .commons import get_date_connect_list, get_multi_date_connect_list
from .forms import OrderForm, ConnectForm, RegularlyDataForm, StationForm, RegularlyForm
from .models import DispatchRegularlyRouteKnow, DispatchCheck, DispatchRegularlyData, DispatchRegularlyWaypoint, Schedule, DispatchOrderConnect, DispatchOrder, DispatchRegularly, RegularlyGroup, DispatchRegularlyConnect, DispatchOrderStation, ConnectRefusal, MorningChecklist, EveningChecklist, DrivingHistory, BusinessEntity, Station, DispatchRegularlyDataStation, DispatchRegularlyStation
from .selectors import DispatchSelector
from assignment.models import AssignmentConnect
from accounting.models import Collect, TotalPrice
from crudmember.models import Category, Client
from humanresource.models import Member, Salary, Team
from humanresource.views import send_message
from itertools import chain
from vehicle.models import Vehicle

from datetime import datetime, timedelta, date
# from utill.decorator import option_year_deco
from common.constant import TODAY, FORMAT, WEEK, WEEK2
from common.datetime import get_hour_minute, get_next_monday, get_mid_time, get_minute_from_colon_time, get_hour_minute_with_colon, calculate_time_with_minutes
from my_settings import KAKAO_KEY
from config.custom_logging import logger

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

class DrivingList(generic.ListView):
    template_name = 'dispatch/driving.html'
    context_object_name = 'member_list'
    model = Member

    def get_queryset(self):
        role = self.request.GET.get('role', None)
        name = self.request.GET.get('name', None)

        member_list = Member.objects.filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')|Q(role='임시')).filter(use='사용').order_by('name')

        if role:
            member_list = member_list.filter(role=role)
        if name:
            member_list = member_list.filter(name__contains=name)
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)
        
        morning_list = []
        morning_check_list = []
        morning_id_list = []
        evening_list = []
        evening_check_list = []
        evening_id_list = []
        driving_list = []
        driving_connect_list = []
        driving_check_connect_list = []

        for member in context['member_list']:
            morning = member.morning_checklist_member.filter(date=date).first()
            if morning:
                morning_list.append(morning)
                morning_check_list.append(morning.submit_check)
                morning_id_list.append(morning.id)
            else:
                morning_list.append('')
                morning_check_list.append('')
                morning_id_list.append('')

            evening = member.evening_checklist_member.filter(date=date).first()
            if evening:
                evening_list.append(evening)
                evening_check_list.append(evening.submit_check)
                evening_id_list.append(evening.id)
            else:
                evening_list.append('')
                evening_check_list.append('')
                evening_id_list.append('')

            connect_cnt = member.info_driver_id.filter(departure_date__startswith=date).count() + member.info_regularly_driver_id.filter(departure_date__startswith=date).count()
            if connect_cnt:
                driving_connect_list.append(connect_cnt)
            else:
                driving_connect_list.append(0)

            driving_list.append(member.driving_history_member.filter(date=date))
            check_connect_cnt = member.driving_history_member.filter(date=date).filter(submit_check=True).count()
            if check_connect_cnt:
                driving_check_connect_list.append(check_connect_cnt)
            else:
                driving_check_connect_list.append(0)
    
        context['morning_list'] = morning_list
        context['evening_list'] = evening_list
        context['morning_check_list'] = morning_check_list
        context['evening_check_list'] = evening_check_list
        context['morning_id_list'] = morning_id_list
        context['evening_id_list'] = evening_id_list
        context['driving_list'] = driving_list
        context['driving_connect_list'] = driving_connect_list
        context['driving_check_connect_list'] = driving_check_connect_list
        context['date'] = date
        context['role'] = self.request.GET.get('role', '')
        context['name'] = self.request.GET.get('name', '')
        return context

def driving_history(request):
    date = request.GET.get('date')
    member_id = request.GET.get('member_id')

    try:
        datetime.strptime(date, FORMAT)
    except:
        return JsonResponse({'result': 'false', 'message': 'dateformat'})

    try:
        member = Member.objects.get(id=member_id)
    except:
        return JsonResponse({'result': 'false', 'message': 'member_id'})

    driving_history_list = member.driving_history_member.filter(date=date)
    driving_history_values = list(driving_history_list.values())

    connect_data_list = []
    for driving in driving_history_list:
        connect_data_list.append(driving.get_connect_data())

    response = {
        'result' : 'true',
        'driving_history_values' : driving_history_values,
        'connect_data_list' : connect_data_list,
    }
    return JsonResponse(response)
    
    

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

        dispatch_selector = DispatchSelector()
        daily_connect_list = dispatch_selector.get_daily_connect_list(date)
        schedule_list = []

        for driver in context['driver_list']:
            connect_list = list(filter(lambda item: item['driver'] == driver.name, daily_connect_list))
            try:
                vehicle = driver.vehicle.vehicle_num
            except Vehicle.DoesNotExist:
                vehicle = ''

            for connect in connect_list:
                connect['driver_vehicle'] = vehicle

                departure_time = datetime.strptime(connect['departure_date'], "%Y-%m-%d %H:%M")
                check_time1 = datetime.strftime(departure_time - timedelta(hours=1.5), "%H:%M")
                check_time2 = datetime.strftime(departure_time - timedelta(hours=1), "%H:%M")
                check_time3 = datetime.strftime(departure_time - timedelta(minutes=20), "%H:%M")

                if date == TODAY:
                    if timeline > check_time1 and not connect['wake_t']:
                        connect['check'] = 'x'
                    elif timeline > check_time2 and not connect['drive_t']:
                        connect['check'] = 'x'
                    elif timeline > check_time3 and not connect['departure_t']:
                        connect['check'] = 'x'
            if len(connect_list) != 0:
                schedule_list.append(connect_list)

        context['schedule_list'] = schedule_list
        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')
        context['date'] = date
        return context

class ScheduleList2(generic.ListView):
    template_name = 'dispatch/schedule2.html'
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

        dispatch_selector = DispatchSelector()
        daily_connect_list = dispatch_selector.get_daily_connect_list(date)
        schedule_list = []

        for driver in context['driver_list']:
            connect_list = list(filter(lambda item: item['driver'] == driver.name, daily_connect_list))
            try:
                vehicle = driver.vehicle.vehicle_num
            except Vehicle.DoesNotExist:
                vehicle = ''

            for connect in connect_list:
                connect['driver_vehicle'] = vehicle

                departure_time = datetime.strptime(connect['departure_date'], "%Y-%m-%d %H:%M")
                check_time1 = datetime.strftime(departure_time - timedelta(hours=1.5), "%H:%M")
                check_time2 = datetime.strftime(departure_time - timedelta(hours=1), "%H:%M")
                check_time3 = datetime.strftime(departure_time - timedelta(minutes=20), "%H:%M")

                if date == TODAY:
                    if timeline > check_time1 and not connect['wake_t']:
                        connect['check'] = 'x'
                    elif timeline > check_time2 and not connect['drive_t']:
                        connect['check'] = 'x'
                    elif timeline > check_time3 and not connect['departure_t']:
                        connect['check'] = 'x'

                # 노선에 있는 order_time, time_list로 공차시간 계산
                if connect['time_list']:
                    time_list = connect['time_list'].split(",")
                    connect['departure_time'] = int(connect['departure_date'][11:13]) * 60 + int(connect['departure_date'][14:16])
                    connect['empty_start_time'] = connect['departure_time'] - int(time_list[0])
                    connect['arrival_time'] = connect['departure_time'] + int(connect['order_time']) - int(time_list[0]) - int(time_list[len(time_list) - 1])
                    connect['empty_end_time'] = connect['arrival_time'] + int(time_list[len(time_list) - 1])
                else:
                    connect['departure_time'] = ''
                    connect['empty_start_time'] = ''
                    connect['arrival_time'] = ''
                    connect['empty_end_time'] = ''

            connect_list.sort(key = lambda x:x['departure_date'])
            if len(connect_list) != 0:
                schedule_list.append(connect_list)

            


        context['schedule_list'] = schedule_list
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
        
        if search:
            regularly_list = DispatchRegularlyData.objects.filter(route__contains=search).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
        else:
            if group_id:
                group = RegularlyGroup.objects.get(id=group_id)
                regularly_list = DispatchRegularlyData.objects.filter(group=group).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
            else:
                regularly_list = DispatchRegularlyData.objects.filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')            

        dispatch_list = []
        for regularly in regularly_list:
            # first 확인필요
            dispatch = regularly.monthly.select_related('regularly_id', 'group').filter(edit_date__lte=date).order_by('-edit_date').first()
            if not dispatch:
                dispatch = regularly.monthly.select_related('regularly_id', 'group').filter(edit_date__gte=date).order_by('edit_date').first()
                

            if dispatch.use == '사용':
                dispatch_list.append(dispatch)
        # print("TEST", len(dispatch_list))
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

        driver_list = Member.objects.filter(Q(role='운전원')|Q(role='팀장')|Q(role='관리자')).filter(use='사용').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]
        outsourcing_list = Member.objects.filter(Q(role='용역')|Q(role='임시')).filter(use='사용').values_list('id', 'name')
        context['outsourcing_dict'] = {}
        for outsourcing in outsourcing_list:
            context['outsourcing_dict'][outsourcing[0]] = outsourcing[1]

        context['dispatch_list'] = get_date_connect_list(date)
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
            order_allowance = order.outsourcing_allowance
            driver = get_object_or_404(Member, id=outsourcing_id)
        else:
            outsourcing = 'n'
            driver = get_object_or_404(Member, id=driver_id)
            if driver.allowance_type == '기사수당(변경)':
                order_allowance = order.driver_allowance2
            else:
                order_allowance = order.driver_allowance
            
        date = request.POST.get('date', None)
        vehicle = get_object_or_404(Vehicle, id=bus)

        try:
            old_connect = order.info_regularly.get(departure_date__startswith=date)
            if old_connect.price == order.price and old_connect.driver_allowance == order_allowance:
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
            driver_allowance = order_allowance,
            price = order.price,
            outsourcing = outsourcing,
            creator = creator,
        )
        r_connect.same_accounting = same_accounting
        r_connect.save()
        try:
            send_message('배차를 확인해 주세요', f'{order.route}\n{r_connect.departure_date} ~ {r_connect.arrival_date}', driver.token, None)
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
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
            if old_connect.outsourcing == 'y':
                allowance = regularly_list[i].outsourcing_allowance
            else:
                if old_connect.driver_id.allowance_type == '기사수당(변경)':
                    allowance = regularly_list[i].driver_allowance2
                else:
                    allowance = regularly_list[i].driver_allowance

            if bus_list[i] and old_connect.price == regularly_list[i].price and old_connect.driver_allowance == allowance:
                same_accounting = True
            else:
                same_accounting = False
            old_connect.same_accounting = same_accounting
            old_connect.delete()
        except Exception as e:
            print("ERROR : ", e)
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
                driver_allowance = regularly_id.driver_allowance2 if driver_list[i].allowance_type == '기사수당(변경)' else regularly_id.driver_allowance,
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

class RegularlyRouteTimeList(generic.ListView):
    template_name = 'dispatch/regularly_route_time.html'
    context_object_name = 'order_list'
    # paginate_by = 10
    model = DispatchRegularlyData

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        order_list = DispatchRegularlyData.objects.filter(use="사용").order_by("departure_time")

        return order_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station_list'] = []
        context['weekday_list'] = []
        for order in context['order_list']:
            stations = ['' for i in range(6)]
            week = ['X' for i in range(7)]
            
            # 요일
            for weekday in order.week.split(" "):
                if weekday == "월":
                    week[0] = "O"
                if weekday == "화":
                    week[1] = "O"
                if weekday == "수":
                    week[2] = "O"
                if weekday == "목":
                    week[3] = "O"
                if weekday == "금":
                    week[4] = "O"
                if weekday == "토":
                    week[5] = "O"
                if weekday == "일":
                    week[6] = "O"
            context['weekday_list'].append(week)
            # 정류장시간
            time_list = list(order.monthly.order_by('-edit_date').first().regularly_station.order_by('index').values('time'))
            if not time_list:
                context['station_list'].append([])
                continue
            length = len(time_list)
            # stations[0] = time_list[0]['time']
            # stations[1] = calculate_time_with_minutes(time_list[1]['time'], -10)
            # stations[2] = time_list[1]['time']

            # stations[3] = time_list[length - 2]['time']
            # stations[4] = calculate_time_with_minutes(time_list[length - 2]['time'], 10)
            # stations[5] = time_list[length - 1]['time']

            stations[0] = time_list[0]['time']
            if order.work_type == '출근':
                stations[1] = time_list[1]['time']
                stations[2] = time_list[2]['time']
            else:
                stations[1] = calculate_time_with_minutes(time_list[1]['time'], -10)
                stations[2] = time_list[1]['time']

            stations[3] = time_list[length - 2]['time']
            stations[4] = time_list[length - 1]['time']
            stations[5] = calculate_time_with_minutes(time_list[length - 1]['time'], 5)

            context['station_list'].append(stations)
            if order.id == 332:
                print(len(context['station_list']), context['station_list'])

        return context

def regularly_route_time_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    datalist = list(DispatchRegularlyData.objects.exclude(use='삭제').order_by('group__number', 'group__name', 'num1', 'number1', 'num2', 'number2').values_list('id', 'group_id__name', 'route', 'departure', 'arrival', 'number1', 'number2', 'departure_time', 'arrival_time', 'work_type', 'location', 'week', 'distance', 'detailed_route', 'maplink', 'price', 'driver_allowance', 'driver_allowance2', 'outsourcing_allowance', 'references', 'use'))
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
        data.insert(17, '')
        datalist[i] = data
        i = i+1
    try:
        df = pd.DataFrame(datalist, columns=['id', '그룹', '노선명', '출발지', '도착지', '순번1', '순번2', '출발시간', '도착시간', '출/퇴근', '위치', '운행요일', '거리', '상세노선', '카카오맵', '경유지', '금액', '기사수당(현재)', '기사수당(변경)', '용역수당', '기준일', '참조사항', '사용'])
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
            context['station_list'] = list(context['detail'].monthly.order_by('-edit_date').first().regularly_station.values('index', 'station__name', 'station_type', 'time', 'station__references', 'station__id', 'regularly__distance_list', 'regularly__time_list').order_by('index'))
            context['waypoint_number'] = len(context['station_list']) - 4
            # context['station_list'] = list(DispatchRegularlyDataStation.objects.filter(regularly_data=context['detail']).values('index', 'station__name', 'station_type', 'time', 'station__references', 'station__id', 'regularly_data__distance_list', 'regularly_data__time_list').order_by('index'))
            # context['waypoint_number'] = DispatchRegularlyDataStation.objects.filter(regularly_data=context['detail']).filter(station_type='정류장').count()
            
            context['station_distance_time_list'] = []
            for i in range(len(context['station_list']) - 1):
                station_data = context['station_list'][i]
                next_station_data = context['station_list'][i + 1]

                try:
                    distance = round(int(station_data['regularly__distance_list'].split(",")[i]) / 1000, 2)
                    duration = get_hour_minute(int(station_data['regularly__time_list'].split(",")[i]))
                except:
                    distance = '에러'
                    duration = '에러'
                context['station_distance_time_list'].append({
                    'station_type': f"{station_data['station_type']} ▶ \n{next_station_data['station_type']}",
                    'station_name': f"{station_data['station__name']} ▶ \n{next_station_data['station__name']}",
                    'station_time': f"{station_data['time']} ▶ \n{next_station_data['time']}",
                    'distance': distance,
                    'duration': duration,
                })

        context['group_list'] = RegularlyGroup.objects.all().order_by('number', 'name')
        group_id = self.request.GET.get('group', '')
        if group_id:
            context['group'] = get_object_or_404(RegularlyGroup, id=group_id)
        elif not self.request.GET.get('new'):
            context['group'] = RegularlyGroup.objects.order_by('number').first()
        
        return context

def create_dispatch_regularly_stations(request, regularly, creator):
    # 정류장 등록
    stationIndex_list = request.POST.getlist('station_index', '')
    stationType_list = request.POST.getlist('station_type', '')
    stationTime_list = request.POST.getlist('station_time', '')
    stationId_list = request.POST.getlist('station_id', '')

    logger.info(f"{stationIndex_list} {stationType_list} {stationTime_list} {stationId_list}")

    for index, type, time, id in zip(stationIndex_list, stationType_list, stationTime_list, stationId_list):
        station = get_object_or_404(Station, id=id)
        # DispatchRegularlyDataStation.objects.create(
        #     regularly_data = regularly_data,
        #     station = station,
        #     index = index,
        #     station_type = type,
        #     time = time,
        #     creator = creator
        # )
        DispatchRegularlyStation.objects.create(
            regularly = regularly,
            station = station,
            index = index,
            station_type = type,
            time = time,
            creator = creator
        )

def kakao_api_exception(current_address, next_address, data, regularly_data, regularly):
    logger.error(f"ERROR {current_address} > {next_address}")
    # API 호출 실패 처리

    regularly_data.time = 0
    regularly_data.time_list = ''
    regularly_data.distance = 0
    regularly_data.distance_list = ''
    regularly_data.save()

    regularly.time = 0
    regularly.time_list = ''
    regularly.distance = 0
    regularly.distance_list = ''
    regularly.save()
    raise BadRequest(f"kakao api error {current_address} > {next_address}\n{data}")
    

def get_distance_and_time_from_kakao(origin, destination, departure_time):
    api_url = 'https://apis-navi.kakaomobility.com/v1/future/directions'
    headers = {
        'Authorization': f"KakaoAK {KAKAO_KEY}"
    }

    # departure time = 202406181530
    try:
        datetime.strptime(departure_time, "%Y%m%d%H%M")
    except:
        raise BadRequest("api departure_time 양식에 안 맞음")
    
    params = {
        'departure_time': departure_time,
        'origin': origin,
        'destination': destination,
        'car_type': 3  # 대형차량
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    data = response.json()
    
    if response.status_code == 200:
        if data['routes'][0]['result_code'] == 104:
            logger.info(f"출발지와 도착지가 5 m 이내로 설정된 경우 경로를 탐색할 수 없음 {origin} > {destination}")
            return 0, 0, data
        else:
            try:
                distance = data['routes'][0]['summary']['distance']
                duration = data['routes'][0]['summary']['duration']
                logger.info(f"kakao 길찾기 api success {origin} > {destination} departure_time : {departure_time}")
                return distance, duration, data
            except Exception as e:
                logger.error(f"kakao api fail exception: {e}")
                return None, None, data
    else:
        logger.error(f"response error {response.status_code}")
        return None, None, data


def get_regularly_distance_and_time(regularly_data, regularly):
    data_list = list(regularly.regularly_station.order_by('index').values('index', 'station__longitude', 'station__latitude', 'station__address', 'time'))
    distance_list = []
    time_list = []
    total_distance = 0
    total_time = 0
    
    for i in range(len(data_list) - 1):
        current_data = data_list[i]
        next_data = data_list[i + 1]
        
        origin = f"{current_data['station__longitude']},{current_data['station__latitude']}"
        destination = f"{next_data['station__longitude']},{next_data['station__latitude']}"
        
        next_monday = get_next_monday(TODAY)
        departure_time = next_monday + get_mid_time(regularly_data.departure_time, regularly_data.arrival_time)

        distance, duration, api_data = get_distance_and_time_from_kakao(origin, destination, departure_time)
        
        if distance is None or duration is None:
            logger.error(f"ERROR {current_data['station__address']} > {next_data['station__address']}")
            # API 호출 실패 처리

            regularly_data.time = 0
            regularly_data.time_list = ''
            regularly_data.distance = 0
            regularly_data.distance_list = ''
            regularly_data.save()

            regularly.time = 0
            regularly.time_list = ''
            regularly.distance = 0
            regularly.distance_list = ''
            regularly.save()
            raise BadRequest(f"kakao api error {current_data['station__address']} > {next_data['station__address']}\n{api_data}")
        
        
        distance_list.append(str(distance))
        duration = get_minute_from_colon_time(next_data['time']) - get_minute_from_colon_time(current_data['time']) if next_data['time'] >= current_data['time'] else 24 * 60 - get_minute_from_colon_time(next_data['time']) - get_minute_from_colon_time(current_data['time'])
        logger.info(f"DURATION {duration}")
        time_list.append(str(duration))
        
        total_distance += distance
        total_time += duration
        logger.info(f"DURATION2 {duration}")
    
    regularly_data.time = total_time
    regularly_data.time_list = ','.join(time_list)
    regularly_data.distance = round(total_distance / 1000, 2)
    regularly_data.distance_list = ','.join(distance_list)
    regularly_data.save()
    
    regularly.time = total_time
    regularly.time_list = ','.join(time_list)
    regularly.distance = round(total_distance / 1000, 2)
    regularly.distance_list = ','.join(distance_list)
    regularly.save()
    
    return


def get_regularly_distance_and_time_from_kakao(regularly_data, regularly):
    data_list = list(regularly_data.regularly_data_station.order_by('index').values('index', 'station__longitude', 'station__latitude', 'station__address'))
    distance_list = []
    time_list = []
    total_distance = 0
    total_time = 0
    
    for i in range(len(data_list) - 1):
        current_data = data_list[i]
        next_data = data_list[i + 1]
        
        origin = f"{current_data['station__longitude']},{current_data['station__latitude']}"
        destination = f"{next_data['station__longitude']},{next_data['station__latitude']}"
        
        next_monday = get_next_monday(TODAY)
        departure_time = next_monday + get_mid_time(regularly_data.departure_time, regularly_data.arrival_time)

        distance, duration, api_data = get_distance_and_time_from_kakao(origin, destination, departure_time)
        
        if distance is None or duration is None:
            logger.error(f"ERROR {current_data['station__address']} > {next_data['station__address']}")
            # API 호출 실패 처리

            regularly_data.time = 0
            regularly_data.time_list = ''
            regularly_data.distance = 0
            regularly_data.distance_list = ''
            regularly_data.save()

            regularly.time = 0
            regularly.time_list = ''
            regularly.distance = 0
            regularly.distance_list = ''
            regularly.save()
            raise BadRequest(f"kakao api error {current_data['station__address']} > {next_data['station__address']}\n{api_data}")
        
        if distance == 0 and duration == 0:
            distance_list.append('0')
            time_list.append('0')
        else:
            distance_list.append(str(distance))
            time_list.append(str(round(duration / 60)))
        
        total_distance += distance
        total_time += duration
    
    regularly_data.time = round(total_time / 60)
    regularly_data.time_list = ','.join(time_list)
    regularly_data.distance = round(total_distance / 1000, 2)
    regularly_data.distance_list = ','.join(distance_list)
    regularly_data.save()
    
    regularly.time = round(total_time / 60)
    regularly.time_list = ','.join(time_list)
    regularly.distance = round(total_distance / 1000, 2)
    regularly.distance_list = ','.join(distance_list)
    regularly.save()
    
    return
    
def regularly_order_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        regularly_data_form = RegularlyDataForm(request.POST)
        if regularly_data_form.is_valid():
            post_group = request.POST.get('group', None)
            try:
                regularly_group = RegularlyGroup.objects.get(pk=post_group)
            except RegularlyGroup.DoesNotExist:
                regularly_group = None

            regularly_data = regularly_data_form.save(commit=False)
            regularly_data.creator = creator
            regularly_data.group = regularly_group
            regularly_data.save()

            regularly_form = RegularlyForm(request.POST)
            if regularly_form.is_valid():
                post_group = request.POST.get('group', None)
                
                regularly = regularly_form.save(commit=False)
                regularly.creator = creator
                regularly.group = regularly_group
                regularly.regularly_id = regularly_data
                regularly.edit_date = TODAY
                regularly.save()
            else:
                raise BadRequest("valid error ", f'{regularly_form.errors}')

            # 정류장 등록
            create_dispatch_regularly_stations(request, regularly, creator)
            # 시간은 DispatchRegularlyStation time으로 계산해서, 거리는 카카오api로 저장하기
            get_regularly_distance_and_time(regularly_data, regularly)
            # 카카오api로 거리, 시간 저장하기
            # get_regularly_distance_and_time_from_kakao(regularly_data, regularly)
            

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest("valid error ", f'{regularly_data_form.errors}')
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
        departure_date = f'{date} {post_departure_date}'
        arrival_date = f'{date} {post_arrival_date}'
        
        r_connect_bus = DispatchRegularlyConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=departure_date).exclude(departure_date__gt=arrival_date).exclude(id__in=connect_list)
        if r_connect_bus:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_bus[0].regularly_id.route,
                'driver': r_connect_bus[0].driver_id.name,
                'bus': r_connect_bus[0].bus_id.vehicle_num,
                'arrival_date': r_connect_bus[0].arrival_date,
                'departure_date': r_connect_bus[0].departure_date,
            })
        r_connect_driver = DispatchRegularlyConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=departure_date).exclude(departure_date__gt=arrival_date).exclude(id__in=connect_list)
        if r_connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': r_connect_driver[0].regularly_id.route,
                'driver': r_connect_driver[0].driver_id.name,
                'bus': r_connect_driver[0].bus_id.vehicle_num,
                'arrival_date': r_connect_driver[0].arrival_date,
                'departure_date': r_connect_driver[0].departure_date,
            })
        
        connect_bus = DispatchOrderConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=departure_date).exclude(departure_date__gt=arrival_date)
        if connect_bus:
            return JsonResponse({
                "status": "fail",
                'route': connect_bus[0].order_id.route,
                'driver': connect_bus[0].driver_id.name,
                'bus': connect_bus[0].bus_id.vehicle_num,
                'arrival_date': connect_bus[0].arrival_date,
                'departure_date': connect_bus[0].departure_date,
            })
        connect_driver = DispatchOrderConnect.objects.filter(driver_id=driver).exclude(arrival_date__lt=departure_date).exclude(departure_date__gt=arrival_date)
        if connect_driver:
            return JsonResponse({
                "status": "fail",
                'route': connect_driver[0].order_id.route,
                'driver': connect_driver[0].driver_id.name,
                'bus': connect_driver[0].bus_id.vehicle_num,
                'arrival_date': connect_driver[0].arrival_date,
                'departure_date': connect_driver[0].departure_date,
            })
        
        a_connect = AssignmentConnect.objects.filter(assignment_id__use_vehicle='사용').filter(bus_id=bus).exclude(end_date__lt=departure_date).exclude(start_date__gt=arrival_date)
        if a_connect:
            return JsonResponse({
                "status": "fail",
                'route': a_connect[0].assignment_id.assignment,
                'driver': a_connect[0].member_id.name,
                'bus': a_connect[0].bus_id.vehicle_num,
                'departure_date': a_connect[0].start_date,
                'arrival_date': a_connect[0].end_date,
            })
        a_connect_driver = AssignmentConnect.objects.filter(member_id=driver).exclude(end_date__lt=departure_date).exclude(start_date__gt=arrival_date)
        if a_connect_driver:
            vehicle_num = a_connect_driver[0].bus_id.vehicle_num if a_connect_driver[0].assignment_id.use_vehicle == '사용' else ''
            return JsonResponse({
                "status": "fail",
                'route': a_connect_driver[0].assignment_id.assignment,
                'driver': a_connect_driver[0].member_id.name,
                'bus': vehicle_num,
                'departure_date': a_connect_driver[0].start_date,
                'arrival_date': a_connect_driver[0].end_date,
            })
        
    
    return JsonResponse({'status': 'success'})

def edit_station_time(recent_regularly, stations):
    time_list = recent_regularly.time_list.split(",")
    departure_minute = get_minute_from_colon_time(recent_regularly.departure_time)
    cnt = 0
    for station in stations:
        if station.index == 1:
            time = departure_minute - int(time_list[0])
        elif station.index == 2:
            time = departure_minute
        else:
            time = get_minute_from_colon_time(stations[cnt - 1].time) + int(time_list[cnt - 1])

        station.time = get_hour_minute_with_colon(time)
        station.save()
        cnt += 1

def time_data(request):
    creator = get_object_or_404(Member, pk=request.session.get('user'))
    station_edit_date = '2024-05-01'


    all_regularly_data = DispatchRegularlyData.objects.exclude(time='').exclude(time='0')
    for regularly_data in all_regularly_data:
        recent_regularly = regularly_data.monthly.order_by("-edit_date").first()
        stations = recent_regularly.regularly_station.order_by('index')
        # stations time 수정
        edit_station_time(recent_regularly, stations)
        
        # 기준일에 데이터 없으면 새로 생성
        try:
            DispatchRegularly.objects.get(regularly_id=regularly_data, edit_date=station_edit_date)
        except DispatchRegularly.DoesNotExist:
            edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__lte=station_edit_date).order_by('-edit_date').first()
            edit_date_regularly_data = model_to_dict(edit_date_regularly)
            edit_date_regularly_data.pop('id')
            edit_date_regularly_data.pop('station')
            

            edit_date_regularly_data['regularly_id'] = regularly_data
            edit_date_regularly_data['edit_date'] = station_edit_date
            edit_date_regularly_data['group'] = RegularlyGroup.objects.get(id=edit_date_regularly_data['group'])
            edit_date_regularly_data['creator'] = creator
            edit_date_r = DispatchRegularly(**edit_date_regularly_data)
            edit_date_r.save()

            # 기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 불러서 regularly_id 변경
            recent_regularly_edit_date = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('edit_date').first().edit_date

            connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__gte=station_edit_date).filter(departure_date__lt=recent_regularly_edit_date)
            logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 기존 데이터 {connects.values('regularly_id', 'id', 'departure_date')}")
            for connect in connects:
                connect.regularly_id = edit_date_r
                connect.save()
            logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 변경 데이터 {connects.values('regularly_id', 'id', 'departure_date')}")



        regularly_list = regularly_data.monthly.exclude(time="").exclude(time="0").exclude(id=recent_regularly.id)
        for regularly in regularly_list:
            regularly.time_list = recent_regularly.time_list
            regularly.time = recent_regularly.time
            regularly.distance_list = recent_regularly.distance_list
            regularly.distance = recent_regularly.distance
            regularly.save()

            regularly.regularly_station.all().delete()
            for station in stations:
                station_data = model_to_dict(station)
                station_data.pop('id')
                station_data['regularly'] = regularly
                station_data['station'] = station.station
                station_data['creator'] = station.creator
                new_station = DispatchRegularlyStation(**station_data)
                new_station.save()







    return JsonResponse({"result": "aa"})

def regularly_order_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    if request.method == 'POST':
        id = request.POST.get('id', None)
        regularly_data = get_object_or_404(DispatchRegularlyData, pk=id)
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        station_edit_date = request.POST.get('station_edit_date')
        regularly_data_form = RegularlyDataForm(request.POST, instance=regularly_data)
        if regularly_data_form.is_valid():
            group = get_object_or_404(RegularlyGroup, pk=request.POST.get('group'))
            regularly_data = regularly_data_form.save(commit=False)
            regularly_data.group = group
            regularly_data.creator = creator
            regularly_data.save()

            try:
                regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data).get(edit_date=TODAY)
                regularly_form = RegularlyForm(request.POST, instance=regularly)
                
            except DispatchRegularly.DoesNotExist:
                regularly_form = RegularlyForm(request.POST)

            if regularly_form.is_valid():
                regularly = regularly_form.save(commit=False)
                regularly.regularly_id = regularly_data
                regularly.edit_date = TODAY
                regularly.group = group
                regularly.creator = creator
                regularly.save()
            else:
                raise BadRequest("valid error ", f'{regularly_form.errors}')
            
            # 등록된 정류장 삭제
            # DispatchRegularlyDataStation.objects.filter(regularly_data=regularly_data).delete()
            DispatchRegularlyStation.objects.filter(regularly=regularly).delete()
            # 정류장 등록
            create_dispatch_regularly_stations(request, regularly, creator)

            #### 금액, 기사수당 수정 시 입력한 월 이후 배차들 금액, 기사수당 수정
            price = regularly_data.price
            driver_allowance = regularly_data.driver_allowance
            driver_allowance2 = regularly_data.driver_allowance2
            outsourcing_allowance = regularly_data.outsourcing_allowance

            post_month = request.POST.get('month')
            if post_month:
                day = regularly_data.group.settlement_date
                day = day if int(day) > 9 else f'0{day}'
                connect_list = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__gte=f'{post_month}-{day} 00:00').order_by('departure_date')
                for connect in connect_list:
                    month = connect.departure_date[:7]
                    member = connect.driver_id

                    if connect.outsourcing == 'y':
                        allowance = outsourcing_allowance
                    else:
                        if connect.driver_id.allowance_type == '기사수당(변경)':
                            allowance = driver_allowance2
                        else:
                            allowance = driver_allowance

                    salary = Salary.objects.filter(member_id=member).get(month=month)
                    if connect.work_type == '출근':
                        salary.attendance = int(salary.attendance) + int(allowance) - int(connect.driver_allowance)
                    elif connect.work_type == '퇴근':
                        salary.leave = int(salary.leave) + int(allowance) - int(connect.driver_allowance)
                    salary.total = int(salary.total) + int(allowance) - int(connect.driver_allowance)
                    salary.save()

                    total = TotalPrice.objects.filter(group_id=group).get(month=month)
                    # connect.price = '' 이면 0으로 넣어주기
                    if not connect.price:
                        connect.price = 0
                    total.total_price = int(total.total_price) + price + math.floor(price * 0.1 + 0.5) - (int(connect.price) + math.floor(int(connect.price) * 0.1 + 0.5))

                    total.save()

                    connect.price = price
                    connect.driver_allowance = allowance
                    connect.save()

                    # if c_regularly != connect.regularly_id:
                    #     connect.regularly_id.price = price
                    #     connect.regularly_id.driver_allowance = driver_allowance
                    #     connect.regularly_id.driver_allowance2 = driver_allowance2
                    #     connect.regularly_id.save()
                    #     c_regularly = connect.regularly_id
                    
                # post_month 기간의 DispatchRegularly 수정
                old_regularly_list = DispatchRegularly.objects.filter(regularly_id=regularly_data).filter(edit_date__gte=f'{post_month}-{day} 00:00')
                for old_regularly in old_regularly_list:
                    old_regularly.price = price
                    old_regularly.driver_allowance = driver_allowance
                    old_regularly.driver_allowance2 = driver_allowance2
                    old_regularly.outsourcing_allowance = outsourcing_allowance
                    old_regularly.save()
                
                    
            connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__gte=f'{TODAY} 00:00')
            for connect in connects:
                connect.regularly_id = regularly
                connect.departure_date = f'{connect.departure_date[:10]} {regularly.departure_time}'
                connect.arrival_date = f'{connect.departure_date[:10]} {regularly.arrival_time}'
                connect.work_type = regularly.work_type
                connect.price = regularly.price
                if connect.outsourcing == 'y':
                    connect.driver_allowance = regularly.outsourcing_allowance
                else:
                    if connect.driver_id.allowance_type == '기사수당(변경)':
                        connect.driver_allowance = regularly.driver_allowance2
                    else:
                        connect.driver_allowance = regularly.driver_allowance
                connect.save()

            

            # 기준일에 데이터 없으면 새로 생성
            if station_edit_date:
                # 시간은 DispatchRegularlyStation time으로 계산해서, 거리는 카카오api로 저장하기
                get_regularly_distance_and_time(regularly_data, regularly)
                # 카카오api로 거리, 시간 저장하기
                # get_regularly_distance_and_time_from_kakao(regularly_data, regularly)
                try:
                    logger.info(f"regularly_data.id {regularly_data.id} station_edit_date {station_edit_date}")
                    DispatchRegularly.objects.get(regularly_id=regularly_data, edit_date=station_edit_date)
                except DispatchRegularly.DoesNotExist:
                    edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__lte=station_edit_date).order_by('-edit_date').first()
                    if not edit_date_regularly:
                        edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('-edit_date').last()
                    edit_date_regularly_data = model_to_dict(edit_date_regularly)
                    edit_date_regularly_data.pop('id')
                    edit_date_regularly_data.pop('station')
                    

                    edit_date_regularly_data['regularly_id'] = regularly_data
                    edit_date_regularly_data['edit_date'] = station_edit_date
                    edit_date_regularly_data['group'] = RegularlyGroup.objects.get(id=edit_date_regularly_data['group'])
                    edit_date_regularly_data['creator'] = creator
                    edit_date_r = DispatchRegularly(**edit_date_regularly_data)
                    edit_date_r.save()

                    logger.info(f"기준일에 데이터 없으면 생성하는 부분 확인 : 기존 데이터 {DispatchRegularly.objects.filter(id=edit_date_regularly.id).values()}")
                    logger.info(f"기준일에 데이터 없으면 생성하는 부분 확인 : 생성한 데이터 {DispatchRegularly.objects.filter(id=edit_date_r.id).values()}")

                    # 기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 불러서 regularly_id 변경
                    recent_regularly_edit_date = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('edit_date').first().edit_date

                    connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__gte=station_edit_date).filter(departure_date__lt=recent_regularly_edit_date)
                    logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 기존 데이터 {connects.values('regularly_id')}")
                    for connect in connects:
                        connect.regularly_id = edit_date_r
                        connect.save()
                    logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 변경 데이터 {connects.values('regularly_id')}")

                # 기준일 이후 노선들 정류장 새로 등록
                new_station_list = regularly.regularly_station.all()
                edit_station_regularly_list = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gte=station_edit_date).exclude(id=regularly.id)
                logger.info(f"edit_station_regularly_list {edit_station_regularly_list}")
                for old_regularly in edit_station_regularly_list:
                    old_regularly.time = regularly.time
                    old_regularly.time_list = regularly.time_list
                    old_regularly.distance = regularly.distance
                    old_regularly.distance_list = regularly.distance_list
                    old_regularly.save()

                    old_regularly.regularly_station.all().delete()
                    
                    for station in new_station_list:
                        station_data = model_to_dict(station)
                        station_data.pop('id')
                        station_data['regularly'] = old_regularly
                        station_data['station'] = station.station
                        station_data['creator'] = station.creator
                        new_station = DispatchRegularlyStation(**station_data)
                        new_station.save()
                        logger.info(f"old_regularly{old_regularly} new_station {new_station}")
                
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else: 
            raise BadRequest("valid error ", f'{regularly_data_form.errors}')
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
            if data['group'] and data['route'] and data['departure'] and data['arrival'] and data['number1'] and data['number2'] and data['departure_time'] and data['arrival_time'] and data['work_type'] and data['week'] and data['price'] and data['driver_allowance'] and data['driver_allowance2'] and data['outsourcing_allowance'] and data['use']:
                pass
        except:
            return JsonResponse({'error': 'required', 'line': count})
        
        if data['id']:
            try:
                DispatchRegularlyData.objects.get(id=data['id'])
            except DispatchRegularlyData.DoesNotExist:
                return JsonResponse({'error': 'id', 'line': count})
        count += 1

    count = 0
    #try:
    for data in post_data:
        group = get_object_or_404(RegularlyGroup, name=data['group'])
        if data['id']:
            try:
                regularly_data = DispatchRegularlyData.objects.get(id=data['id'])
            except DispatchRegularlyData.DoesNotExist:
                return JsonResponse({'error': 'id', 'line': count + 1})
            regularly_data.group = group
            regularly_data.references = data['references']
            regularly_data.departure = data['departure']
            regularly_data.arrival = data['arrival']
            regularly_data.departure_time = data['departure_time']
            regularly_data.arrival_time = data['arrival_time']
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
            regularly_data.distance = data['distance']
            regularly_data.creator = creator

            if (data['month']):
                regularly_data.price = data['price']
                regularly_data.driver_allowance = data['driver_allowance']
                regularly_data.driver_allowance2 = data['driver_allowance2']
                regularly_data.outsourcing_allowance = data['outsourcing_allowance']

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
                driver_allowance2 = data['driver_allowance2'],
                outsourcing_allowance = data['outsourcing_allowance'],
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
                distance = data['distance'],
                creator = creator,
            )
        regularly_data.save()

        old_waypoints = DispatchRegularlyWaypoint.objects.filter(regularly_id=regularly_data)
        old_waypoints.delete()
        # 경유지 생성
        if data['waypoint']:
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
            regularly.distance = data['distance']
            regularly.creator = creator

            regularly.price = regularly_data.price
            regularly.driver_allowance = regularly_data.driver_allowance
            regularly.driver_allowance2 = regularly_data.driver_allowance2
            regularly.outsourcing_allowance = regularly_data.outsourcing_allowance
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
                distance = data['distance'],
                creator = creator,
                price = regularly_data.price,
                driver_allowance = regularly_data.driver_allowance,
                driver_allowance2 = regularly_data.driver_allowance2,
                outsourcing_allowance = regularly_data.outsourcing_allowance,
            )
        regularly.save()

        order = regularly_data
        driver_allowance = data['driver_allowance']
        driver_allowance2 = data['driver_allowance2']
        outsourcing_allowance = data['outsourcing_allowance']
        price = data['price']
        post_month = data['month']
        if post_month and data['id']:
            day = order.group.settlement_date
            day = day if int(day) > 9 else f'0{day}'
            connect_list = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=order).filter(departure_date__gte=f'{post_month}-{day} 00:00').order_by('departure_date')
            c_regularly = ''
            for connect in connect_list:
                month = connect.departure_date[:7]
                member = connect.driver_id

                if connect.outsourcing == 'y':
                    allowance = outsourcing_allowance
                else:
                    if connect.driver_id.allowance_type == '기사수당(변경)':
                        allowance = driver_allowance2
                    else:
                        allowance = driver_allowance

                salary = Salary.objects.filter(member_id=member).get(month=month)
                if connect.work_type == '출근':
                    salary.attendance = int(salary.attendance) + int(allowance) - int(connect.driver_allowance)
                elif connect.work_type == '퇴근':
                    salary.leave = int(salary.leave) + int(allowance) - int(connect.driver_allowance)
                salary.total = int(salary.total) + int(allowance) - int(connect.driver_allowance)
                salary.save()

                total = TotalPrice.objects.filter(group_id=group).get(month=month)
                # connect.price = '' 이면 0으로 넣어주기
                if not connect.price:
                    connect.price = 0
                total.total_price = int(total.total_price) + price + math.floor(price * 0.1 + 0.5) - (int(connect.price) + math.floor(int(connect.price) * 0.1 + 0.5))

                total.save()

                connect.price = price
                connect.driver_allowance = allowance
                connect.save()

            # post_month 기간의 DispatchRegularly 수정
            old_regularly_list = DispatchRegularly.objects.filter(edit_date__gte=f'{post_month}-{day} 00:00')
            for old_regularly in old_regularly_list:
                old_regularly.price = price
                old_regularly.driver_allowance = driver_allowance
                old_regularly.driver_allowance2 = driver_allowance2
                old_regularly.outsourcing_allowance = outsourcing_allowance
                old_regularly.save()

        connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=order).filter(departure_date__gte=f'{TODAY} 00:00')
        for connect in connects:
            connect.regularly_id = regularly
            connect.departure_date = f'{connect.departure_date[:10]} {regularly.departure_time}'
            connect.arrival_date = f'{connect.departure_date[:10]} {regularly.arrival_time}'
            connect.work_type = regularly.work_type
            connect.price = regularly.price
            if connect.outsourcing == 'y':
                connect.driver_allowance = regularly.outsourcing_allowance
            else:
                if connect.driver_id.allowance_type == '기사수당(변경)':
                    connect.driver_allowance = regularly.driver_allowance2
                else:
                    connect.driver_allowance = regularly.driver_allowance
                
            connect.save()

        count += 1
    return JsonResponse({'status': 'success', 'count': count})
    #except Exception as e:
    #    return JsonResponse({'status': 'fail', 'count': count, 'error': f'{e}'})

def regularly_order_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    datalist = list(DispatchRegularlyData.objects.exclude(use='삭제').order_by('group__number', 'group__name', 'num1', 'number1', 'num2', 'number2').values_list('id', 'group_id__name', 'route', 'departure', 'arrival', 'number1', 'number2', 'departure_time', 'arrival_time', 'work_type', 'location', 'week', 'distance', 'detailed_route', 'maplink', 'price', 'driver_allowance', 'driver_allowance2', 'outsourcing_allowance', 'references', 'use'))
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
        data.insert(17, '')
        datalist[i] = data
        i = i+1
    try:
        df = pd.DataFrame(datalist, columns=['id', '그룹', '노선명', '출발지', '도착지', '순번1', '순번2', '출발시간', '도착시간', '출/퇴근', '위치', '운행요일', '거리', '상세노선', '카카오맵', '경유지', '금액', '기사수당(현재)', '기사수당(변경)', '용역수당', '기준일', '참조사항', '사용'])
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
                regularly.driver_allowance2 = order.driver_allowance2
                regularly.outsourcing_allowance = order.outsourcing_allowance
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
                regularly.distance = order.distance
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
                    driver_allowance2 = order.driver_allowance2,
                    outsourcing_allowance = order.outsourcing_allowance,
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
                    distance = order.distance,
                    creator = order.creator
                )
            regularly.save()

            # 오늘부터 미래의 배차 전부 삭제
            connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=order).filter(departure_date__gte=f'{TODAY} 00:00')
            for connect in connects:
                connect.delete()

        return redirect(reverse('dispatch:regularly_route') + f'?group={group}')
    else:
        return HttpResponseNotAllowed(['post'])

class RegularlyRouteKnowList(generic.ListView):
    template_name = 'dispatch/regularly_route_know.html'
    context_object_name = 'order_list'
    model = DispatchRegularlyRouteKnow

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        group_id = self.request.GET.get('group', '')
        search = self.request.GET.get('search', '')
        search_type = self.request.GET.get('type', '')
        if not group_id:
            group = RegularlyGroup.objects.order_by('number').first()
        else:
            group = get_object_or_404(RegularlyGroup, id=group_id)
        if search:
            if search_type == '운전원':
                return DispatchRegularlyData.objects.prefetch_related('regularly_route_know').filter(use='사용').filter(group=group).filter(regularly_route_know__driver_id__name__contains=search).order_by('num1', 'number1', 'num2', 'number2')
            else:
                return DispatchRegularlyData.objects.prefetch_related('regularly_route_know').filter(use='사용').filter(group=group).filter(Q(route__contains=search) | Q(departure__contains=search) | Q(arrival__contains=search)).order_by('num1', 'number1', 'num2', 'number2')
        else:
            return DispatchRegularlyData.objects.prefetch_related('regularly_route_know').filter(use='사용').filter(group=group).order_by('num1', 'number1', 'num2', 'number2')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['type'] = self.request.GET.get('type', '')

        context['group_list'] = RegularlyGroup.objects.all().order_by('number', 'name')
        group_id = self.request.GET.get('group', '')
        if group_id:
            context['group'] = get_object_or_404(RegularlyGroup, id=group_id)
        else:
            context['group'] = RegularlyGroup.objects.order_by('number').first()
        
        context['driver_list'] = Member.objects.filter(use='사용').filter(Q(role='운전원')|Q(role='팀장')).values('id', 'name').order_by('name')
        context['knows'] = {}
        for order in context['order_list']:
            know = order.regularly_route_know.all()
            if know:
                context['knows'][order.id] = list(know.values('id', 'driver_id__id', 'driver_id__name', 'driver_id__role').order_by('driver_id__name'))
            else:
                context['knows'][order.id] = ''
        return context

def regularly_route_know_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    
    if request.method == "POST":        
        regularly = get_object_or_404(DispatchRegularlyData, id=request.POST.get('regularly_id'))
        driver = get_object_or_404(Member, id=request.POST.get('driver_id'))

        if DispatchRegularlyRouteKnow.objects.filter(driver_id=driver).filter(regularly_id=regularly).exists():
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        route_know = DispatchRegularlyRouteKnow(
            regularly_id = regularly,
            driver_id = driver,
            creator = get_object_or_404(Member, pk=request.session['user'])
        )
        route_know.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_route_know_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    
    if request.method == "POST":        
        id_list = request.POST.getlist('id')
        for pk in id_list:
            DispatchRegularlyRouteKnow.objects.get(id=pk).delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

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

        if not group.regularly.exclude(use='삭제').exists():
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

class RegularlyConnectList(generic.ListView):
    template_name = 'dispatch/regularly_connect_list.html'
    context_object_name = 'connect_list'
    model = DispatchRegularly

    def get(self, request, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        group_list = self.request.GET.getlist('group_id', '')
        team_list = self.request.GET.getlist('team', '')
        time_list = self.request.GET.getlist('time', '')
        no_team = self.request.GET.get('no_team', '')
        search = self.request.GET.get('search', '')
        date = self.request.GET.get('date', TODAY)

        connect_list = DispatchRegularlyConnect.objects.filter(driver_id__team__id__in=team_list)
        if no_team:
            connect_list = connect_list | DispatchRegularlyConnect.objects.filter(driver_id__team=None)

        connect_list = connect_list.filter(regularly_id__group__id__in=group_list).filter(departure_date__startswith=date).order_by('regularly_id__num1', 'regularly_id__number1', 'regularly_id__num2', 'regularly_id__number2')
        q_objects = Q()
        for time_value in time_list:
            min_time = f'{date} {time_value}:00'
            max_time = f'{date} {time_value}:59'
            q_objects |= (Q(departure_date__lte=max_time) & Q(departure_date__gte=min_time))

        connect_list = connect_list.filter(q_objects)

        if search:
            connect_list = connect_list.filter(regularly_id__route__contains=search)

        return connect_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        business_list = BusinessEntity.objects.all().order_by('number')
        business_group_data = {}
        for business in business_list:
            business_group_data[business.id] = [*business.regularly_groups.values('id', 'name')]

        time_list = []
        count = 5
        for i in range(19):
            if count < 10:
                time_list.append(f"0{count}")
            else:
                time_list.append(f"{count}")
            count += 1

        context['time_list'] = time_list
        context['business_group_data'] = business_group_data
        context['business_list'] = business_list
        context['group_list'] = RegularlyGroup.objects.all().order_by('number')
        context['team_list'] = Team.objects.order_by('name')

        context['search_group_list'] = self.request.GET.getlist('group_id', [])
        context['search_team_list'] = self.request.GET.getlist('team', [])
        context['search_time_list'] = self.request.GET.getlist('time', [])
        context['no_team'] = self.request.GET.get('no_team', '')
        context['search'] = self.request.GET.get('search', '')
        context['date'] = self.request.GET.get('date', TODAY)
        return context


def business_edit(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        
        business_id = request.POST.get('business_id', '')
        name = request.POST.get('business_name', '')
        number = request.POST.get('business_number', '')
        if not name:
            raise Http404
        
        if business_id:
            business = get_object_or_404(BusinessEntity, id=business_id)
            business.name = name
            business.number = number
            business.creator = creator
            business.save()
        else:
            business = BusinessEntity.objects.create(name=name, number=number, creator=creator)
        
        group_id_list = request.POST.getlist('group_id', '')
        group_list = []
        for group_id in group_id_list:
            group_list.append(get_object_or_404(RegularlyGroup, id=group_id))

        business.regularly_groups.clear()
        business.regularly_groups.add(*group_list)

        return redirect('dispatch:regularly_connect')
    else:
        return HttpResponseNotAllowed(['post'])

class RegularlyConnectPrintList(generic.ListView):
    template_name = 'dispatch/regularly_connect_print.html'
    context_object_name = 'connect_list'
    model = DispatchRegularlyData

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        group_list = self.request.GET.getlist('group_id', '')
        team_list = self.request.GET.getlist('team', '')
        time_list = self.request.GET.getlist('time', '')
        no_team = self.request.GET.get('no_team', '')
        search = self.request.GET.get('search', '')
        date = self.request.GET.get('date', TODAY)

        connect_list = DispatchRegularlyConnect.objects.filter(driver_id__team__id__in=team_list)
        if no_team:
            connect_list = connect_list | DispatchRegularlyConnect.objects.filter(driver_id__team=None)

        connect_list = connect_list.filter(regularly_id__group__id__in=group_list).filter(departure_date__startswith=date).order_by('regularly_id__num1', 'regularly_id__number1', 'regularly_id__num2', 'regularly_id__number2')
        q_objects = Q()
        for time_value in time_list:
            min_time = f'{date} {time_value}:00'
            max_time = f'{date} {time_value}:59'
            q_objects |= (Q(departure_date__lte=max_time) & Q(departure_date__gte=min_time))

        connect_list = connect_list.filter(q_objects)

        if search:
            connect_list = connect_list.filter(regularly_id__route__contains=search)

        return connect_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)
        context['date'] = date
        context['weekday'] = WEEK[datetime.strptime(date, FORMAT).weekday()]

        return context

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

            # 정류장
            context['station_list'] = list(DispatchOrderStation.objects.filter(order_id=context['detail']).values('station_name', 'time', 'order_id__distance_list', 'order_id__time_list'))
            
            context['station_distance_time_list'] = []
            for i in range(len(context['station_list']) - 1):
                station_data = context['station_list'][i]
                next_station_data = context['station_list'][i + 1]

                try:
                    distance = round(int(station_data['order_id__distance_list'].split(",")[i]) / 1000, 2)
                    duration = get_hour_minute(int(station_data['order_id__time_list'].split(",")[i]))
                except:
                    distance = '에러'
                    duration = '에러'
                context['station_distance_time_list'].append({
                    'station_name': f"{station_data['station_name']} ▶ \n{next_station_data['station_name']}",
                    'station_time': f"{station_data['time']} ▶ \n{next_station_data['time']}",
                    'distance': distance,
                    'duration': duration,
                })

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
            try:
                send_message('배차를 확인해 주세요', f'{order.route}\n{order.departure_date} ~ {order.arrival_date}', driver.token, None)
            except Exception as e:
                print(e)
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponseNotAllowed(['post'])

def get_order_distance_and_time(order):
    data_list = list(order.station.order_by('pub_date').values('longitude', 'latitude', 'address'))
    distance_list = []
    time_list = []
    total_distance = 0
    total_time = 0
    
    for i in range(len(data_list) - 1):
        current_data = data_list[i]
        next_data = data_list[i + 1]
        
        origin = f"{current_data['longitude']},{current_data['latitude']}"
        destination = f"{next_data['longitude']},{next_data['latitude']}"
        
        next_monday = get_next_monday(TODAY)
        departure_time = next_monday + get_mid_time(order.departure_date[11:], order.arrival_date[11:])

        distance, duration, api_data = get_distance_and_time_from_kakao(origin, destination, departure_time)
        
        if distance is None or duration is None:
            logger.error(f"ERROR 일반 {current_data['address']} > {next_data['address']}")
            # API 호출 실패 처리

            order.time = 0
            order.time_list = ''
            order.distance = 0
            order.distance_list = ''
            order.save()

            raise BadRequest(f"kakao api error {current_data['address']} > {next_data['address']}\n{api_data}")
        
        if distance == 0 and duration == 0:
            distance_list.append('0')
            time_list.append('0')
        else:
            distance_list.append(str(distance))
            time_list.append(str(round(duration / 60)))
        
        total_distance += distance
        total_time += duration
    
    order.time = round(total_time / 60)
    order.time_list = ','.join(time_list)
    order.distance = round(total_distance / 1000, 2)
    order.distance_list = ','.join(distance_list)
    order.save()
    return

def order_create(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')

    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
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
            
            try:
                create_order_stations(request, order, creator)
            except Exception as e:
                raise BadRequest("정류장 정보를 잘못 입력하셨습니다.", e)

            # 노선의 정류장에서 정류장 사이의 거리, 시간 측정해서 저장
            get_order_distance_and_time(order)

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
        o_connect = DispatchOrderConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date).exclude(id__in=connects)
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
        r_connect = DispatchRegularlyConnect.objects.filter(bus_id=bus).exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date)
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

        a_connect = AssignmentConnect.objects.filter(assignment_id__use_vehicle='사용').filter(bus_id=bus).exclude(end_date__lt=post_departure_date).exclude(start_date__gt=post_arrival_date)
        if a_connect:
            return JsonResponse({
                "status": "fail",
                'route': a_connect[0].assignment_id.assignment,
                'driver': a_connect[0].member_id.name,
                'bus': a_connect[0].bus_id.vehicle_num,
                'departure_date': a_connect[0].start_date,
                'arrival_date': a_connect[0].end_date,
            })
        a_connect_driver = AssignmentConnect.objects.filter(member_id=driver).exclude(end_date__lt=post_departure_date).exclude(start_date__gt=post_arrival_date)
        if a_connect_driver:
            vehicle_num = a_connect_driver[0].bus_id.vehicle_num if a_connect_driver[0].assignment_id.use_vehicle == '사용' else ''
            return JsonResponse({
                "status": "fail",
                'route': a_connect_driver[0].assignment_id.assignment,
                'driver': a_connect_driver[0].member_id.name,
                'bus': vehicle_num,
                'departure_date': a_connect_driver[0].start_date,
                'arrival_date': a_connect_driver[0].end_date,
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
            # route를 옵션 넣은 departure, arrival로 해야되나?
            order.route = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            order.creator = creator
            order.save()

            # 경유지 처리
            old_stations = order.station.all()
            old_stations.delete()
            try:
                create_order_stations(request, order, creator)
            except Exception as e:
                raise BadRequest("정류장 정보를 잘못 입력하셨습니다.", e)
            
            # 노선의 정류장에서 정류장 사이의 거리, 시간 측정해서 저장
            get_order_distance_and_time(order)

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def create_order_stations(request, order, creator):
    station_list = request.POST.getlist('station_name')
    station_time_list = request.POST.getlist('station_time')
    delegate_list = request.POST.getlist('delegate')
    delegate_phone_list = request.POST.getlist('delegate_phone')
    place_name_list = request.POST.getlist('place_name')
    address_list = request.POST.getlist('address')
    longitude_list = request.POST.getlist('longitude')
    latitude_list = request.POST.getlist('latitude')

    if (len(station_time_list) == len(station_list) and
    len(delegate_list) == len(station_list) and
    len(delegate_phone_list) == len(station_list) and
    len(place_name_list) == len(station_list) and
    len(address_list) == len(station_list) and
    len(longitude_list) == len(station_list) and
    len(latitude_list) == len(station_list)):
        for i in range(len(station_list)):
            station = DispatchOrderStation(
                order_id=order,
                station_name=station_list[i],
                place_name=place_name_list[i],
                address=address_list[i],
                longitude=longitude_list[i],
                latitude=latitude_list[i],
                time=station_time_list[i],
                delegate=delegate_list[i],
                delegate_phone=delegate_phone_list[i],
                creator=creator,
            )
            station.save()
    else:
        raise Exception("정류장 데이터 개수 다름", 
            len(station_time_list),
            len(delegate_list),
            len(delegate_phone_list),
            len(place_name_list),
            len(address_list),
            len(longitude_list),
            len(latitude_list), len(station_list)
        )

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

def order_upload(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    creator = get_object_or_404(Member, pk=request.session['user'])
    post_data = json.loads(request.body)

    count = 1
    for data in post_data:
        # 딕셔너리에 없는 키 넣으면 에러나서 try 씀
        try:
            if data['departure'] and data['arrival'] and data['departure_date'] and data['arrival_date'] and data['bus_cnt'] and data['customer'] and data['customer_phone'] and data['operation_type'] and data['price'] and data['driver_allowance']:
                pass
        except:
            return JsonResponse({'error': 'required', 'line': count})
    

        data_str = data['stations'].strip("[]")
        station_list = re.findall(r"\('(.*?)', '(.*?)', '(.*?)', '(.*?)'\)", data_str)

        if data['stations'] and not station_list:
            return JsonResponse({'error': 'stations', 'line': count})
        for i in range(len(station_list)):
            if not station_list[i][0]:
                return JsonResponse({'error': 'required', 'line': count})
        if not(data['bus_cnt'].isdigit() and data['price'].isdigit() and data['driver_allowance'].isdigit()):
            return JsonResponse({'error': 'digit', 'line': count, 'data' : [data['bus_cnt'], data['price'], data['driver_allowance']]})
        
        if data['id']:
            try:
                DispatchOrder.objects.get(id=data['id'])
            except DispatchOrder.DoesNotExist:
                return JsonResponse({'error': 'id', 'line': count})
        #항목 체크
        if not Category.objects.filter(category=data['bus_type']).exists():
            return JsonResponse({'error': 'category', 'line': count, 'data': '차량종류'})
        if not Category.objects.filter(category=data['operation_type']).exists():
            return JsonResponse({'error': 'category', 'line': count, 'data': '운행종류'})
        if not Category.objects.filter(category=data['order_type']).exists():
            return JsonResponse({'error': 'category', 'line': count, 'data': '유형'})
        if not Category.objects.filter(category=data['bill_place']).exists():
            return JsonResponse({'error': 'category', 'line': count, 'data': '계산서'})
        if not Category.objects.filter(category=data['reservation_company']).exists():
            return JsonResponse({'error': 'category', 'line': count, 'data': '예약회사'})
        if not Category.objects.filter(category=data['operating_company']).exists():
            return JsonResponse({'error': 'category', 'line': count, 'data': '운행회사'})

        count += 1

    count = 1
    for data in post_data:
        VAT = data['VAT'] if data['VAT'] == 'y' else 'n'
        option = data['option']
        departure = data['departure']
        if '카드기' in option and (not '<카드기>' in departure):
            departure = '<카드기>' + departure
        elif not '카드기' in option and '<카드기>' in departure:
            departure = departure.replace('<카드기>','')

        if '카시트' in option and (not '<카시트>' in departure):
            departure = '<카시트>' + departure
        elif not '카시트' in option and '<카시트>' in departure:
            departure = departure.replace('<카시트>','')

        if '음향' in option and (not '<음향>' in departure):
            departure = '<음향>' + departure
        elif not '음향' in option and '<음향>' in departure:
            departure = departure.replace('<음향>','')

        if data['id']:
            try:
                order = DispatchOrder.objects.get(id=data['id'])
            except DispatchOrder.DoesNotExist:
                return JsonResponse({'error': 'id', 'line': count})
            
            order.operation_type = data['operation_type']
            order.references = data['references']
            order.departure = departure
            order.arrival = data['arrival']
            order.departure_date = data['departure_date']
            order.arrival_date = data['arrival_date']
            order.bus_type = data['bus_type']
            order.bus_cnt = data['bus_cnt']
            order.price = data['price']
            order.driver_allowance = data['driver_allowance']
            order.contract_status = data['contract_status']
            order.cost_type = data['cost_type']
            order.option = option
            order.customer = data['customer']
            order.customer_phone = data['customer_phone']
            order.bill_place = data['bill_place']
            order.ticketing_info = data['ticketing_info']
            order.order_type = data['order_type']
            order.operating_company = data['operating_company']
            order.reservation_company = data['reservation_company']
            order.driver_lease = data['driver_lease']
            order.vehicle_lease = data['vehicle_lease']
            order.collection_type = data['collection_type']
            order.payment_method = data['payment_method']
            order.VAT = VAT
            order.route = data['departure'] + " ▶ " + data['arrival']

            connects = order.info_order.all()
            if data['contract_status'] == '취소':
                connects.delete()
            else:
                for connect in connects:
                    connect.departure_date = data['departure_date']
                    connect.arrival_date = data['arrival_date']
                    connect.price = data['price']
                    connect.driver_allowance = data['driver_allowance']
                    connect.save()
        else:
            order = DispatchOrder(
                operation_type = data['operation_type'],
                references = data['references'],
                departure = departure,
                arrival = data['arrival'],
                departure_date = data['departure_date'],
                arrival_date = data['arrival_date'],
                bus_type = data['bus_type'],
                bus_cnt = data['bus_cnt'],
                price = data['price'],
                driver_allowance = data['driver_allowance'],
                contract_status = data['contract_status'],
                cost_type = data['cost_type'],
                option = option,
                customer = data['customer'],
                customer_phone = data['customer_phone'],
                bill_place = data['bill_place'],
                ticketing_info = data['ticketing_info'],
                order_type = data['order_type'],
                operating_company = data['operating_company'],
                reservation_company = data['reservation_company'],
                driver_lease = data['driver_lease'],
                vehicle_lease = data['vehicle_lease'],
                collection_type = data['collection_type'],
                payment_method = data['payment_method'],
                VAT = VAT,
                route = data['departure'] + " ▶ " + data['arrival'],
                creator = creator,
            )

        order.save()
        order.station.all().delete()

        data_str = data['stations'].strip("[]")
        station_list = re.findall(r"\('(.*?)', '(.*?)', '(.*?)', '(.*?)'\)", data_str)

        for i in range(len(station_list)):
            station = DispatchOrderStation(
                order_id=order,
                station=station_list[i][0],
                time=station_list[i][1],
                delegate=station_list[i][2],
                delegate_phone=station_list[i][3],
                creator=creator,
            )
            station.save()
        
        count = count + 1
    return JsonResponse({'status': 'success', 'count': count - 1})


def order_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    start_date = request.GET.get('date1', TODAY)
    end_date = request.GET.get('date2', TODAY)
    datalist = list(DispatchOrder.objects.exclude(arrival_date__lt=f'{start_date} 00:00').exclude(departure_date__gt=f'{end_date} 24:00').order_by('departure_date').values_list(
        'id',
        'departure',
        'arrival',
        'departure_date',
        'arrival_date',
        'bus_cnt',
        'bus_type',
        'customer',
        'customer_phone',
        'contract_status',
        'operation_type',
        'reservation_company',
        'operating_company',
        'price',
        'driver_allowance',
        'option',
        'cost_type',
        'bill_place',
        'collection_type',
        'payment_method',
        'VAT',
        'ticketing_info',
        'order_type',
        'references',
        'driver_lease',
        'vehicle_lease',
    ))
    i = 0
    # 경유지 일단 빼고 함 2024-08-01
    # for data in datalist:
    #     data = list(data)
    #     stations = list(DispatchOrderStation.objects.filter(order_id__id=data[0]).values_list('station', 'time', 'delegate', 'delegate_phone'))
    #     if stations:
    #         data.insert(9, stations)
    #     else:
    #         data.insert(9, '')
    #     datalist[i] = data
    #     i = i + 1
    try:
        df = pd.DataFrame(datalist, columns=[
            'id',
            '출발지',
            '도착지',
            '출발날짜',
            '복귀날짜',
            '차량대수',
            '차량종류',
            '예약자',
            '예약자 전화번호',
            # '경유지 정보',
            '계약현황',
            '운행종류',
            '예약회사',
            '운행회사',
            '계약금액',
            '상여금',
            '버스옵션',
            '비용구분',
            '계산서 발행처',
            '수금구분',
            '결제방법',
            'VAT포함여부',
            '표찰정보',
            '유형',
            '참조사항',
            '인력임대차',
            '차량임대차',
        ])
        url = f'{MEDIA_ROOT}/dispatch/dispatchOrderList.xlsx'
        df.to_excel(url, index=False)

        if os.path.exists(url):
            with open(url, 'rb') as fh:
                quote_file_url = urllib.parse.quote('일반배차.xlsx'.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
    except Exception as e:
        print(e)
        #return JsonResponse({'status': 'fail', 'e': e})
        raise Http404
    
def get_place_info_from_kakao(query, page):
    api_url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {
        'Authorization': f"KakaoAK {KAKAO_KEY}"
    }

    params = {
        'query': query,
        'page': page,
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    data = response.json()
    
    if response.status_code == 200:
        try:
            address = data['documents'][0]['address_name']
            place_name = data['documents'][0]['place_name']
            latitude = data['documents'][0]['y']
            longitude = data['documents'][0]['x']
            pageable_count = data['meta']['pageable_count']
            return data, 'true'
        except Exception as e:
            logger.error(f"kakao 장소 검색 api fail exception: {e} response : {data}")
            return data, 'false'
    else:
        logger.error(f"kakao 장소 검색 api response code error {response.status_code} response : {data}")
        return data, 'false'

def order_station_search(request):
    if request.session.get('authority') > 2:
        return render(request, 'authority.html')
    
    if request.method == "POST":
        post_data = json.loads(request.body)
        query = post_data.get('query', '')
        page = post_data.get('page', 1)
        data, result = get_place_info_from_kakao(query, page)
        return JsonResponse({'data': data, 'result': result, 'page': page})
    else:
        return HttpResponseNotAllowed(['POST'])

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
        member_list = Member.objects.filter(authority__gte=1)
    
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

def print_estimate(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    
    order_id = request.GET.get('id')




    return render(request, 'dispatch/estimate_print.html')

class RegularlyStationList(generic.ListView):
    template_name = 'dispatch/regularly_station.html'
    context_object_name = 'station_list'
    model = Station

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
        
    def get_queryset(self):
        search_type = self.request.GET.get('search_type', '')
        value = self.request.GET.get('value', '')


        if search_type == '정류장명' and value:
            station_list = Station.objects.filter(name__contains=value).order_by('address')
        elif search_type == '주소' and value:
            station_list = Station.objects.filter(address__contains=value).order_by('address')
        elif search_type == '참조사항' and value:
            station_list = Station.objects.filter(references__contains=value).order_by('address')
        else:
            station_list = Station.objects.all().order_by('address')
        return station_list
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = self.request.GET.get('value', '')
        context['search_type'] = self.request.GET.get('search_type', '')
        
        return context

def regularly_station_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        station_form = StationForm(request.POST)
        types_list = request.POST.getlist('types', [])
        if station_form.is_valid():
            creator = get_object_or_404(Member, id=request.session.get('user'))
            station = station_form.save(commit=False)
            station.creator = creator
            station.set_types(types_list)
            station.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_station_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        id = request.POST.get('id', None)
        station = Station.objects.get(id=id)
        types_list = request.POST.getlist('station_type', [])
        station_form = StationForm(request.POST, initial={'station_type': types_list}, instance=station)
        if station_form.is_valid():
            station = station_form.save(commit=False)
            station.set_types(types_list)
            station.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_station_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        id_list = request.POST.getlist('id', None)
        for id in id_list:
            station = Station.objects.get(id=id)
            station.delete()
            
        return redirect('dispatch:regularly_station')
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_station(request, id):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "GET":
        station = Station.objects.get(id=id)
        data = {
            'name' : station.name,
            'address' : station.address,
            'latitude' : station.latitude,
            'longitude' : station.longitude,
            'references' : station.references,
            'station_type' : station.get_types(),
        }

        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(['GET'])


def regularly_station_list(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "GET":
        type = request.GET.get('type', '')
        name = request.GET.get('name', '')

        queryset = Station.objects.all()

        if type:
            queryset = queryset.filter(station_type__contains=type)
        if name:
            queryset = queryset.filter(name__contains=name)

        station_list = queryset.values()
        data = []
        for station in station_list:
            data.append({
                'id' : station['id'],
                'station_type' : station['station_type'],
                'name' : station['name'],
                'latitude' : station['latitude'],
                'longitude' : station['longitude'],
                'address' : station['address'],
                'references' : station['references'],
            })

        return JsonResponse({'data' : data})
    else:
        return HttpResponseNotAllowed(['GET'])
    
def regularly_station_upload(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    creator = get_object_or_404(Member, pk=request.session['user'])
    post_data = json.loads(request.body)

    count = 1
    for data in post_data:
        # 딕셔너리에 없는 키 넣으면 에러나서 try 씀
        try:
            if data['name'] and data['address'] and data['latitude'] and data['longitude']:
                pass
        except:
            return JsonResponse({'error': 'required', 'line': count})
    
        if data['id']:
            try:
                Station.objects.get(id=data['id'])
            except Station.DoesNotExist:
                return JsonResponse({'error': 'id', 'line': count})
        count += 1

    count = 1
    for data in post_data:
        if data['id']:
            try:
                station = Station.objects.get(id=data['id'])
            except Station.DoesNotExist:
                return JsonResponse({'error': 'id', 'line': count})
            
            station.name = data['name']
            station.address = data['address']
            station.latitude = data['latitude']
            station.longitude = data['longitude']
            station.references = data['references']
            station.station_type = data['station_type']
            
            
        else:
            station = Station(
                name = data['name'],
                address = data['address'],
                latitude = data['latitude'],
                longitude = data['longitude'],
                references = data['references'],
                station_type = data['station_type'],
                creator = creator
            )
        station.save()
        count = count + 1
    return JsonResponse({'status': 'success', 'count': count - 1})


def regularly_station_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    datalist = list(Station.objects.values_list(
        'id',
        'name',
        'address',
        'latitude',
        'longitude',
        'references',
        'station_type',
    ))
    i = 0
    try:
        df = pd.DataFrame(datalist, columns=[
            'id',
            '정류장명',
            '주소',
            '위도',
            '경도',
            '참조사항',
            '종류',
        ])
        url = f'{MEDIA_ROOT}/dispatch/regularlyStationList.xlsx'
        df.to_excel(url, index=False)

        if os.path.exists(url):
            with open(url, 'rb') as fh:
                quote_file_url = urllib.parse.quote('정류장.xlsx'.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
    except Exception as e:
        print(e)
        #return JsonResponse({'status': 'fail', 'e': e})
        raise Http404
    