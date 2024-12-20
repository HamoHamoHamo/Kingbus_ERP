import json
import math
import pandas as pd
import re
import urllib
import os
import mimetypes
import requests
import itertools

from config.settings.base import MEDIA_ROOT
from django.db.models import Q, Sum, Prefetch, Case, When, Value, IntegerField, Subquery, OuterRef, F, Count
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic, View

from .commons import get_date_connect_list, get_multi_date_connect_list
from .forms import OrderForm, ConnectForm, RegularlyDataForm, StationForm, RegularlyForm, TourForm, RouteTeamForm
from .models import DispatchRegularlyRouteKnow, DispatchCheck, DispatchRegularlyData, DispatchRegularlyWaypoint, Schedule, DispatchOrderConnect, DispatchOrder, DispatchRegularly, RegularlyGroup, DispatchRegularlyConnect, DispatchOrderStation, ConnectRefusal, MorningChecklist, EveningChecklist, DrivingHistory, BusinessEntity, Station, DispatchRegularlyDataStation, DispatchRegularlyStation, DispatchOrderTourCustomer, DispatchOrderTour, RouteTeam, StationArrivalTime, DriverCheck, ConnectStatusFieldMapping, ConnectStatus
from .selectors import DispatchSelector
from assignment.models import AssignmentConnect
from accounting.models import Collect, TotalPrice
from crudmember.models import Category, Client
from humanresource.models import Member, Salary, Team
from humanresource.views import send_message
from vehicle.models import Vehicle, DailyChecklist, Refueling

from firebase.rpa_p_firebase import RpaPFirebase, TOUR_PATH
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
    context_object_name = 'data_list'
    model = Member

    def get_queryset(self):
        select = self.request.GET.get('select', 'driver')
        search = self.request.GET.get('search', None)

        if select == 'driver':
            data_list = Member.objects.filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')|Q(role='임시')).filter(use="사용").order_by('name')
            if search:
                data_list = data_list.filter(name__contains=search)
        elif select == 'vehicle':
            data_list = Vehicle.objects.filter(use="사용").order_by('vehicle_num')
            if search:
                data_list = data_list.filter(vehicle_num__contains=search)
        else:
            raise BadRequest('검색 종류가 잘못됐습니다')
        
        return data_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)
        timeline = datetime.strftime(datetime.now(), "%H:%M")
        if date == TODAY:
            context['timeline'] = (int(timeline[:2]) * 60 + int(timeline[3:])) * 0.058

        dispatch_selector = DispatchSelector()
        # connect 데이터 가져옴
        daily_connect_list = dispatch_selector.get_daily_connect_list(date)


        context['select'] = self.request.GET.get('select', 'driver')
        # 기사 기준으로 데이터 불러오기
        if context['select'] == 'driver':
            connect_dict = self.get_schedule_list_by_driver(timeline, daily_connect_list, context['data_list'])
        # 차량 기준으로 데이터 불러오기
        elif context['select'] == 'vehicle':
            connect_dict = self.get_schedule_list_by_bus(timeline, daily_connect_list, context['data_list'])
        else:
            raise BadRequest('검색 종류가 잘못됐습니다')

        schedule_list = []
        for data in context['data_list']:
            # driver의 connect_list 가져오기
            connect_list = connect_dict.get(data.id, [])
            if connect_list:
                for connect in connect_list:
                    if connect['driver_vehicle'] == None:
                        connect['driver_vehicle'] = ''
                    if connect['vehicle_driver'] == None:
                        connect['vehicle_driver'] = ''
                    if connect['vehicle_driver_phone'] == None:
                        connect['vehicle_driver_phone'] = ''

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
                schedule_list.append(connect_list)

        context['schedule_list'] = schedule_list
        
        context['search'] = self.request.GET.get('search', '')
        context['date'] = date
        return context
    
    def get_schedule_list_by_bus(self, timeline, daily_connect_list, bus_list):
        connect_dict = {}
        # bus id로 dict 만들어서 해당 버스의 배차 넣기
        for connect in daily_connect_list:
            bus = connect['bus_id__id']
            if bus not in connect_dict:
                connect_dict[bus] = []
            connect_dict[bus].append(connect)
        return connect_dict

    def get_schedule_list_by_driver(self, timeline, daily_connect_list, driver_list):
        connect_dict = {}
        for connect in daily_connect_list:
            driver = connect['driver_id__id']
            if driver not in connect_dict:
                connect_dict[driver] = []
            connect_dict[driver].append(connect)
        return connect_dict
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

class RollCallList(generic.ListView):
    template_name = 'dispatch/roll_call.html'
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
        sorting = self.request.GET.get('sorting', '')
        

        if not team_list:
            connect_list = DispatchRegularlyConnect.objects.filter(departure_date__startswith=date)
        else:
            connect_list = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id__team__in=team_list).filter(departure_date__startswith=date)
        
        if no_team:
            connect_list = connect_list | DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id__team=None)

        if group_list:
            connect_list = connect_list.filter(regularly_id__group__id__in=group_list)
        q_objects = Q()
        for time_value in time_list:
            min_time = f'{date} {time_value}:00'
            max_time = f'{date} {time_value}:59'
            q_objects |= (Q(departure_date__lte=max_time) & Q(departure_date__gte=min_time))
        # 기본값 모두 체크
        if not time_list:
            min_time = f'{date} 04:00'
            max_time = f'{date} 24:59'
            q_objects |= (Q(departure_date__lte=max_time) & Q(departure_date__gte=min_time))

        connect_list = connect_list.filter(q_objects).order_by('departure_date')

        if sorting == '노선' and search:
            connect_list = connect_list.filter(regularly_id__route__contains=search)
        if sorting == '팀':
            if search:
                connect_list = connect_list.filter(regularly_id__regularly_id__team__name__contains=search)
            connect_list = connect_list.order_by('regularly_id__regularly_id__team', 'departure_date')
        elif sorting == '기사':
            if search:
                connect_list = connect_list.filter(driver_id__name__contains=search)
            connect_list = connect_list.order_by('driver_id__name', 'departure_date')
        elif sorting == '차량':
            if search:
                connect_list = connect_list.filter(bus_id__vehicle_num__contains=search)
            connect_list = connect_list.order_by('bus_id__vehicle_num', 'departure_date')

        return connect_list.annotate(
            total_drive_count=Subquery(
                DispatchRegularlyConnect.objects.filter(
                    driver_id=OuterRef('driver_id'),
                    regularly_id__regularly_id=OuterRef('regularly_id__regularly_id')
                ).values('driver_id').annotate(
                    total=Count('id')
                ).values('total')[:1]
            )
        ).values(
            'id',
            'regularly_id__route',
            'regularly_id__regularly_id__team__name',
            'driver_id__name',
            'driver_id__id',
            'bus_id__vehicle_num',
            'total_drive_count',
            'departure_date',
            'arrival_date',
            'check_regularly_connect__wake_time',
            'check_regularly_connect__drive_time',
            'check_regularly_connect__departure_time',
            'check_regularly_connect__connect_check'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        time_list = []
        count = 4
        for i in range(19):
            if count < 10:
                time_list.append(f"0{count}")
            else:
                time_list.append(f"{count}")
            count += 1

        context['time_list'] = time_list



        # 사업장
        business_list = BusinessEntity.objects.all().order_by('number')
        business_group_data = {}
        for business in business_list:
            business_group_data[business.id] = [*business.regularly_groups.values('id', 'name')]
        context['business_group_data'] = business_group_data
        context['business_list'] = business_list

        context['group_list'] = RegularlyGroup.objects.all().order_by('number')
        context['team_list'] = RouteTeam.objects.order_by('name')

        context['search_group_list'] = self.request.GET.getlist('group_id', [])
        context['search_team_list'] = self.request.GET.getlist('team', [])
        context['search_time_list'] = self.request.GET.getlist('time', [])
        context['no_team'] = self.request.GET.get('no_team', '')
        context['search'] = self.request.GET.get('search', '')
        context['date'] = self.request.GET.get('date', TODAY)
        context['sorting'] = self.request.GET.get('sorting', '')
        return context


def roll_call_route_status_data(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    
    if request.method == 'POST':
        return HttpResponseNotAllowed(['get'])

    id = request.GET.get('id')
    work_type = request.GET.get('work_type')
    if work_type == "출퇴근":
        connect = DispatchRegularlyConnect.objects.get(id=id)
        driver_check = DriverCheck.objects.get(regularly_id=id)
        arrival_time_list = list(StationArrivalTime.objects.filter(regularly_connect_id=id).order_by('arrival_time').values('arrival_time', 'station_id__index', 'has_issue'))
        driving_history = DrivingHistory.objects.get(regularly_connect_id=id)

        station_type_list = ['정류장', '사업장', '마지막 정류장']
        station_list = list(connect.regularly_id.regularly_station.filter(station_type__in=station_type_list).order_by('index').values('id', 'time', 'index', "station__name"))

        data = {
            'connect': {
                'route' : connect.regularly_id.route,
                'name': connect.driver_id.name,
                'phone': connect.driver_id.phone_num,
                'vehicle_num': connect.bus_id.vehicle_num,
                'departure_time': connect.departure_date[11:16],
                'arrival_time': connect.arrival_date[11:16],
                'id': connect.id,
            },
            'status': connect.status,
            
            'wake_time': driver_check.wake_time,
            'drive_time': driver_check.drive_time,
            'departure_time': driver_check.departure_time,
            'drive_start_time': driver_check.drive_start_time,
            'drive_end_time': driver_check.drive_end_time,
            'arrival_time_list': arrival_time_list,
            'station_list': station_list,
            'connect_check': driver_check.connect_check,
            'driving_history_time': driving_history.submit_time,
            'driving_history': driving_history.submit_check,
            'wake_time_has_issue': driver_check.wake_time_has_issue,
            'drive_time_has_issue': driver_check.drive_time_has_issue,
            'departure_time_has_issue': driver_check.departure_time_has_issue,
        }
    else:
        connect = DispatchOrderConnect.objects.get(id=id)
        driver_check = DriverCheck.objects.get(order_id=id)
        arrival_time_list = []
        driving_history = DrivingHistory.objects.get(order_connect_id=id)
        station_list = []

        data = {
        'connect': {
            'route' : connect.order_id.route,
            'name': connect.driver_id.name,
            'phone': connect.driver_id.phone_num,
            'vehicle_num': connect.bus_id.vehicle_num,
            'departure_time': connect.departure_date[11:16],
            'arrival_time': connect.arrival_date[11:16],
            'id': connect.id,
        },
        'status': connect.status,
        
        'wake_time': driver_check.wake_time,
        'drive_time': driver_check.drive_time,
        'departure_time': driver_check.departure_time,
        'drive_start_time': driver_check.drive_start_time,
        'drive_end_time': driver_check.drive_end_time,
        'arrival_time_list': arrival_time_list,
        'station_list': station_list,
        'connect_check': driver_check.connect_check,
        'driving_history_time': driving_history.submit_time,
        'driving_history': driving_history.submit_check,
        'wake_time_has_issue': driver_check.wake_time_has_issue,
        'drive_time_has_issue': driver_check.drive_time_has_issue,
        'departure_time_has_issue': driver_check.departure_time_has_issue,
    }
    

    return JsonResponse({
        'result' : True,
        'data' : data,
    })

class DispatchConnectService:
    # 현재 해야하는 배차 정보 불러오기
    @staticmethod
    def get_current_connect(connects):
        """
        운행 완료가 아닌 가장 첫 번째 배차를 찾습니다.
        
        Args:
            connects (list): 배차 정보가 담긴 리스트
            
        Returns:
            dict or None: 조건에 맞는 첫 번째 배차. 없으면 None 반환
        """
        
        for connect in connects:            
            # 상태가 '운행 완료'가 아닌 첫번째 배차정보 리턴
            if connect['status'] != ConnectStatus.COMPLETE:
                return connect
                
        return None 

    # 배차 데이터 불러오기
    @staticmethod
    def get_daily_connect_list(date, user):
        regularly_connects = DispatchRegularlyConnect.objects.filter(departure_date__startswith=date, driver_id=user).select_related('regularly_id', 'bus_id')
        order_connects = DispatchOrderConnect.objects.filter(departure_date__startswith=date, driver_id=user).select_related('order_id', 'bus_id')

        return regularly_connects, order_connects
        

class RollCallDriverStatus(View):
    DATE_FORMAT = '%Y-%m-%d'

    def get(self, request):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')

        date = request.GET.get('date', TODAY)
        user = Member.objects.get(id=request.GET.get('id'))

        try:
            datetime.strptime(date, self.DATE_FORMAT)
        except ValueError:
            return JsonResponse({
                'success': False,
                'code': '1',
                'data': {'error': 'Invalid date format'},
            }, status=400)

        tasks = self.get_connect_list(date, user)

        go_to_work = self.get_go_to_work_data(tasks)
        go_to_work['daily_checklist'] = self.get_daily_checklist(date, user)
        get_off_work = self.get_get_off_work_data(date, user)
        info = self.get_current_task(tasks, user)

        data = {
            # 'status': info['status'],
            'info': info,
            'go_to_work': go_to_work,
            'tasks': tasks,
            'get_off_work': get_off_work,
        }
        
        return JsonResponse({
            'result': True,
            'data': data,
        }, status=200)
    
    def get_daily_checklist(self, date, user):
        try:
            morning_checklist = MorningChecklist.objects.get(date=date, member=user)
        except MorningChecklist.DoesNotExist:
            morning_checklist = MorningChecklist.create_new(date, user)
        try:
            daily_checklist = DailyChecklist.objects.get(date=date, member=user)
        except DailyChecklist.DoesNotExist:
            daily_checklist = DailyChecklist.create_new(date, user)
            
        if morning_checklist.submit_check and daily_checklist.submit_check:
            status = "완료"
        else:
            status = "-"
        return {
            "status": status,
            "submit_time": daily_checklist.submit_time,
        }

    def get_connect_list(self, date, user):
        regularly_connects, order_connects = DispatchConnectService.get_daily_connect_list(date, user)
        # 정기 배차 데이터 변환
        regularly_data = []
        for connect in regularly_connects:
            try:
                driver_check = DriverCheck.objects.get(regularly_id=connect)
                status_info = []
                for status, field_name in ConnectStatusFieldMapping.DRIVER_CHECK_STATUS_FIELD_MAP.items():
                    completion_time = getattr(driver_check, field_name, '')
                    status_info.append({
                        'status_name': status.value,
                        'completion_time': completion_time
                    })
            except DriverCheck.DoesNotExist:
                status_info = []

            regularly_data.append({
                'dispatch_id': connect.id,
                'work_type': connect.work_type,
                'bus_id': connect.bus_id.id,
                'bus_num': connect.bus_id.vehicle_num,
                'departure_date': connect.departure_date[11:16],
                'arrival_date': connect.arrival_date[11:16],
                'status': connect.status,
                'has_issue': connect.has_issue,
                'status_info': status_info,
                'route': connect.regularly_id.route,
            })

        # 수시 배차 데이터 변환
        order_data = []
        for connect in order_connects:
            order_data.append({
                'dispatch_id': connect.id,
                'work_type': connect.work_type,
                'bus_num': connect.bus_id.vehicle_num,
                'departure_date': connect.departure_date[11:16],
                'arrival_date': connect.arrival_date[11:16],
                'status': connect.status,
                'status_info': '',
                'route': connect.order_id.route,
            })

        # 데이터 합치고 정렬
        combined_data = regularly_data + order_data
        return sorted(combined_data, key=lambda x: x['departure_date'])

    def get_current_task(self, tasks, user):
        current_connect = DispatchConnectService.get_current_connect(tasks)
        if current_connect:
            return {
                'route': current_connect['route'],
                'bus_num': current_connect['bus_num'],
                'name': user.name,
                'phone': user.phone_num,
            }
        
        return {
            'route': '',
            'bus_num': '',
            'name': user.name,
            'phone': user.phone_num,
        }

    # 출근 데이터 불러오기
    def get_go_to_work_data(self, tasks):
        if tasks:
            first = tasks[0]
            first_driver_check = DriverCheck.get_instance(first['dispatch_id'], first['work_type'])
            connect = first_driver_check.regularly_id if first_driver_check.regularly_id else first_driver_check.order_id

            return {
                "wake_time": first_driver_check.wake_time,
                'departure_time': connect.departure_date[11:16],
                'has_issue': first_driver_check.wake_time_has_issue,
            }
        else:
            return {
                "wake_time": "",
                'departure_time': "",
                'has_issue': "",
            }

    def get_get_off_work_data(self, date, user):
        try:
            evening_checklist = EveningChecklist.objects.get(date=date, member=user)
        except EveningChecklist.DoesNotExist:
            evening_checklist = EveningChecklist.create_new(date, user)
            
        return {
            'roll_call_time': evening_checklist.checklist_submit_time,
            'tomorrow_dispatch_check_time': evening_checklist.tomorrow_check_submit_time,
            'get_off_time': evening_checklist.get_off_submit_time,
        }

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

        # 조건 구성
        conditions = Q(week__contains=weekday)
        if search:
            conditions &= Q(route__contains=search)
        if group_id:
            conditions &= Q(group_id=group_id)
        conditions &= Q(use='사용')

        # monthly 관계에 대한 prefetch 구성
        monthly_queryset = DispatchRegularly.objects.filter(
            use='사용'
        ).select_related(
            'regularly_id', 
            'group'
        )

        # 한 번에 데이터 가져오기
        regularly_list = DispatchRegularlyData.objects.filter(
            conditions
        ).order_by(
            'num1', 'number1', 'num2', 'number2'
        ).prefetch_related(
            Prefetch(
                'monthly',
                queryset=monthly_queryset
            )
        )

        dispatch_list = []
        for regularly in regularly_list:
            # prefetch된 데이터에서 필터링
            dispatches = sorted(
                [d for d in regularly.monthly.all()],
                key=lambda x: x.edit_date,
                reverse=True
            )
            
            if dispatches:
                # edit_date__lte=date 조건에 맞는 항목 찾기
                dispatch = next(
                    (d for d in dispatches if d.edit_date <= date),
                    next(
                        (d for d in sorted(dispatches, key=lambda x: x.edit_date) if d.edit_date >= date),
                        None
                    )
                )
                if dispatch:
                    dispatch_list.append(dispatch)

        return dispatch_list

    # def get_queryset(self):
    #     search = self.request.GET.get('search', '')
    #     date = self.request.GET.get('date', TODAY)
    #     group_id = self.request.GET.get('group', '')

    #     weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]

    #     # 기본 필터링 조건 설정
    #     filters = {'week__contains': weekday}
    #     if search:
    #         filters['route__contains'] = search
    #     if group_id:
    #         filters['group_id'] = group_id

    #     # DispatchRegularlyData 필터링
    #     regularly_list = DispatchRegularlyData.objects.filter(**filters)

    #     connect_queryset = DispatchRegularlyConnect.objects.filter(departure_date__startswith=date)

    #     # prefetch_related로 monthly를 가져오되, 필요한 데이터를 필터링
    #     monthly_queryset = DispatchRegularly.objects.filter(edit_date__lte=date, use='사용').order_by('-edit_date').prefetch_related(
    #         Prefetch('info_regularly', queryset=connect_queryset),
    #     )
        

    #     # 'monthly'에 대한 prefetch
    #     regularly_list = regularly_list.prefetch_related(
    #         Prefetch('monthly', queryset=monthly_queryset),
    #     )

    #     dispatch_list = []
    #     for regularly in regularly_list:
    #         # prefetch된 monthly에서 첫 번째 항목을 찾기
    #         dispatch = regularly.monthly.first()

    #         if not dispatch:
    #             # 만약 매칭된 dispatch가 없다면, edit_date >= date인 항목 중 첫 번째를 가져옴
    #             dispatch = regularly.monthly.filter(edit_date__gte=date, use='사용').order_by('edit_date').first()

    #         if dispatch:
    #             dispatch_list.append(dispatch)

    #     return dispatch_list

    # def get_queryset(self):
    #     search = self.request.GET.get('search', '')
    #     date = self.request.GET.get('date', TODAY)
    #     group_id = self.request.GET.get('group', '')

    #     weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        
    #     if search:
    #         regularly_list = DispatchRegularlyData.objects.filter(route__contains=search).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
    #     else:
    #         if group_id:
    #             group = RegularlyGroup.objects.get(id=group_id)
    #             regularly_list = DispatchRegularlyData.objects.filter(group=group).filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')
    #         else:
    #             regularly_list = DispatchRegularlyData.objects.filter(week__contains=weekday).order_by('num1', 'number1', 'num2', 'number2')            

    #     dispatch_list = []
    #     for regularly in regularly_list:
    #         # first 확인필요
    #         dispatch = regularly.monthly.select_related('regularly_id', 'group').filter(edit_date__lte=date).order_by('-edit_date').first()
    #         if not dispatch:
    #             dispatch = regularly.monthly.select_related('regularly_id', 'group').filter(edit_date__gte=date).order_by('edit_date').first()
                

    #         if dispatch.use == '사용':
    #             dispatch_list.append(dispatch)
    #     return dispatch_list


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

            # 배차내역 2주치 불러오기
            connect_history_list = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data, departure_date__gte=str_start_date, arrival_date__lte=str_end_date).order_by('departure_date').values('departure_date', 'driver_id__id', 'bus_id__id', 'driver_id__name', 'bus_id__vehicle_num', 'outsourcing')
            for connect_history in connect_history_list:
                date_calculation = (datetime.strptime(connect_history['departure_date'][:10], FORMAT) - start_date).days
                history_list[date_calculation] = connect_history
                # block_list[date_calculation] = ''

                h_driver = connect_history['driver_id__id']
                h_bus = connect_history['bus_id__id']

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

        context['vehicles'] = list(Vehicle.objects.filter(use='사용').order_by('vehicle_num', 'driver__name').values('id', 'driver__id', 'driver__name', 'vehicle_num0', 'vehicle_num', 'model_year'))
        context['group_list'] = RegularlyGroup.objects.all().order_by('number')
        
        #
        group_bus_list = []
        group_driver_list = []
        group_outsourcing_list = []
        departure_time_list = []
        arrival_time_list = []
        for order in context['order_list']:
            connect = order.info_regularly.filter(departure_date__contains=date).last()
            if connect:
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
            context['station_list'] = list(context['detail'].monthly.order_by('-edit_date').first().regularly_station.values('index', 'station__name', 'station_type', 'time', 'station__references', 'station__id', 'regularly__distance_list', 'regularly__time_list').order_by('index'))
            #context['waypoint_number'] = len(context['station_list']) - 8 if context['detail'].work_type == '출근' else len(context['station_list']) - 9
            context['waypoint_number'] = 0
            for station in context['station_list']:
                if station['station_type'] == '정류장':
                    context['waypoint_number'] += 1
            #context['waypoint_number'] = DispatchRegularlyDataStation.objects.filter(regularly_data=context['detail']).filter(station_type='정류장').count()
            
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
        
        # 알림시간 값
        context['prepare_time1'] = f"{int(context['detail'].prepare_time / 60):02}" if id else "01"
        context['prepare_time2'] = f"{(context['detail'].prepare_time % 60):02}" if id else "30"
        context['boarding_time1'] = f"{int(context['detail'].boarding_time / 60):02}" if id else "01"
        context['boarding_time2'] = f"{(context['detail'].boarding_time % 60):02}" if id else "00"
        context['first_stop_time1'] = f"{int(context['detail'].first_stop_time / 60):02}" if id else "00"
        context['first_stop_time2'] = f"{(context['detail'].first_stop_time % 60):02}" if id else "20"

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

        # 카카오 api 사용 안 함, 나중에 필요하면 다시 사용
        # distance, duration, api_data = get_distance_and_time_from_kakao(origin, destination, departure_time)
        distance = 0
        duration = 0
        api_data = ""

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
        # duration 계산
        if next_data['time'] >= current_data['time'] :
            duration = get_minute_from_colon_time(next_data['time']) - get_minute_from_colon_time(current_data['time'])
        else:
            duration = 24 * 60 + get_minute_from_colon_time(next_data['time']) - get_minute_from_colon_time(current_data['time'])
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
            # try:
            #     regularly_group = RegularlyGroup.objects.get(pk=post_group)
            # except RegularlyGroup.DoesNotExist:
            #     regularly_group = None

            regularly_data = regularly_data_form.save(commit=False)
            regularly_data.creator = creator
            # regularly_data.group = regularly_group
            regularly_data.save()

            regularly_form = RegularlyForm(request.POST)
            if regularly_form.is_valid():
                post_group = request.POST.get('group', None)
                
                regularly = regularly_form.save(commit=False)
                regularly.creator = creator
                # regularly.group = regularly_group
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


def time_data(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    
    creator = get_object_or_404(Member, pk=request.session.get('user'))
    station_edit_date = '2024-07-29'

    count = 0
    all_regularly_data = DispatchRegularlyData.objects.filter(use="사용")
    all_regularly_data = all_regularly_data
    for regularly_data in all_regularly_data:
        count += 1
        regularly = regularly_data.monthly.order_by("edit_date").last()
        # recent_regularly = regularly
        # stations = recent_regularly.regularly_station.order_by('index')
        # 기준일에 데이터 없으면 새로 생성
        if station_edit_date:
            # 시간은 DispatchRegularlyStation time으로 계산해서, 거리는 카카오api로 저장하기
            # get_regularly_distance_and_time(regularly_data, regularly)
            # 카카오api로 거리, 시간 저장하기
            # get_regularly_distance_and_time_from_kakao(regularly_data, regularly)
            try:
                logger.info(f"regularly_data.id {regularly_data.id} station_edit_date {station_edit_date}")
                DispatchRegularly.objects.get(regularly_id=regularly_data, edit_date=station_edit_date)
            except DispatchRegularly.DoesNotExist:
                # 수정일이 기준일인 DispatchRegularly가 없을 경우 기준일에서 가장 가까운 데이터 가져옴 = edit_date_regularly
                edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__lte=station_edit_date).order_by('-edit_date').first()
                if not edit_date_regularly:
                    edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('edit_date').first()
                edit_date_regularly_data = model_to_dict(edit_date_regularly)
                edit_date_regularly_data.pop('id')
                edit_date_regularly_data.pop('station')
                

                edit_date_regularly_data['regularly_id'] = regularly_data
                edit_date_regularly_data['edit_date'] = station_edit_date
                edit_date_regularly_data['group'] = RegularlyGroup.objects.get(id=edit_date_regularly_data['group'])
                edit_date_regularly_data['creator'] = creator
                edit_date_r = DispatchRegularly(**edit_date_regularly_data)
                edit_date_r.save()

                logger.info(f"기준일에 데이터 없으면 생성하는 부분 확인 : 기존 데이터 {DispatchRegularly.objects.filter(id=edit_date_regularly.id).values('id')}")
                logger.info(f"기준일에 데이터 없으면 생성하는 부분 확인 : 생성한 데이터 {DispatchRegularly.objects.filter(id=edit_date_r.id).values('id')}")

                # 기준일 ~ 기준일 이후 첫번째 regularly 데이터 사이의 배차들 불러서 regularly_id 변경
                connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__gte=station_edit_date)
                logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 기존 데이터 {connects.values('regularly_id')}")

                # 기준일 이후 첫번째 regularly가 있으면 그 전까지의 배차만 가져오기
                first_regularly_from_edit_date = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('edit_date').first()
                if first_regularly_from_edit_date:
                    connects = connects.filter(departure_date__lt=first_regularly_from_edit_date.edit_date)
                

                
                for connect in connects:
                    connect.regularly_id = edit_date_r
                    connect.save()
                # logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 변경 데이터 {connects.values('regularly_id')}")

            # 기준일 이후 노선들 정류장 새로 등록
            new_station_list = regularly.regularly_station.select_related("station", "creator").all()
            # logger.info(f'new_station_list {new_station_list}')
            edit_station_regularly_list = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gte=station_edit_date).exclude(id=regularly.id)
            # logger.info(f"edit_station_regularly_list {edit_station_regularly_list}")
            regularly_time = regularly.time
            regularly_time_list = regularly.time_list
            for old_regularly in edit_station_regularly_list:
                old_regularly.time = regularly_time
                old_regularly.time_list = regularly_time_list
                # old_regularly.distance = regularly.distance
                # old_regularly.distance_list = regularly.distance_list
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
                    # logger.info(f"old_regularly{old_regularly} new_station {new_station}")

    # return render(request, 'dispatch/order_print.html', {})
    return JsonResponse({"result": count})

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
            regularly_data = regularly_data_form.save(commit=False)
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
                    # 수정일이 기준일인 DispatchRegularly가 없을 경우 기준일에서 가장 가까운 데이터 가져옴 = edit_date_regularly
                    edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__lte=station_edit_date).order_by('-edit_date').first()
                    if not edit_date_regularly:
                        edit_date_regularly = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('edit_date').first()
                    edit_date_regularly_data = model_to_dict(edit_date_regularly)
                    edit_date_regularly_data.pop('id')
                    edit_date_regularly_data.pop('station')
                    

                    edit_date_regularly_data['regularly_id'] = regularly_data
                    edit_date_regularly_data['edit_date'] = station_edit_date
                    edit_date_regularly_data['group'] = RegularlyGroup.objects.get(id=edit_date_regularly_data['group'])
                    edit_date_regularly_data['creator'] = creator
                    edit_date_r = DispatchRegularly(**edit_date_regularly_data)
                    edit_date_r.save()

                    logger.info(f"기준일에 데이터 없으면 생성하는 부분 확인 : 기존 데이터 {DispatchRegularly.objects.filter(id=edit_date_regularly.id).values('id')}")
                    logger.info(f"기준일에 데이터 없으면 생성하는 부분 확인 : 생성한 데이터 {DispatchRegularly.objects.filter(id=edit_date_r.id).values('id')}")

                    # 기준일 ~ 기준일 이후 첫번째 regularly 데이터 사이의 배차들 불러서 regularly_id 변경
                    connects = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__gte=station_edit_date)
                    logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 기존 데이터 {connects.values('regularly_id')}")

                    # 기준일 이후 첫번째 regularly가 있으면 그 전까지의 배차만 가져오기
                    first_regularly_from_edit_date = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gt=station_edit_date).order_by('edit_date').first()
                    if first_regularly_from_edit_date:
                        connects = connects.filter(departure_date__lt=first_regularly_from_edit_date.edit_date)
                    

                    
                    for connect in connects:
                        connect.regularly_id = edit_date_r
                        connect.save()
                    # logger.info(f"기준일 ~ 기준일 이후 첫번째 데이터 사이의 배차들 확인 : 변경 데이터 {connects.values('regularly_id')}")

                # 기준일 이후 노선들 정류장 새로 등록
                new_station_list = regularly.regularly_station.select_related("station", "creator").all()
                # logger.info(f'new_station_list {new_station_list}')
                edit_station_regularly_list = DispatchRegularly.objects.filter(regularly_id=regularly_data, edit_date__gte=station_edit_date).exclude(id=regularly.id)
                # logger.info(f"edit_station_regularly_list {edit_station_regularly_list}")
                regularly_time = regularly.time
                regularly_time_list = regularly.time_list
                for old_regularly in edit_station_regularly_list:
                    old_regularly.time = regularly_time
                    old_regularly.time_list = regularly_time_list
                    # old_regularly.distance = regularly.distance
                    # old_regularly.distance_list = regularly.distance_list
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
                        # logger.info(f"old_regularly{old_regularly} new_station {new_station}")
                
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

class RouteTeamList(generic.ListView):
    template_name = 'dispatch/route_team.html'
    context_object_name = 'regulary_data_list'
    model = DispatchRegularlyData

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        team = self.request.GET.get('team', '')
        team_none = self.request.GET.get('team_none', '')
        group = self.request.GET.get('group', '')
        name = self.request.GET.get('name', '')

        queryset = DispatchRegularlyData.objects.filter(use='사용')

        if group:
            queryset = queryset.filter(group__id=group)

        if team:
            queryset = queryset.filter(team__id=team)
        
        if team_none == "팀없음":
            queryset = queryset.filter(team=None)

        if name:
            queryset = queryset.filter(route__contains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team_id = self.request.GET.get('team', '')
        if team_id:
            team = get_object_or_404(RouteTeam, id=team_id)
        else:
            team = '전체'

        null = self.request.GET.get('team_none', '')
        if null == '팀없음':
            team = '팀없음'

        context['group'] = self.request.GET.get('group', '')
        if context['group']:
            context['group'] = int(context['group'])
        context['name'] = self.request.GET.get('name', '')
        context['group_list'] = RegularlyGroup.objects.all().order_by('number', 'name')
        context['team_leader'] = Member.objects.filter(role="팀장", use="사용").values('name', 'id')
        context['team_list'] = RouteTeam.objects.select_related('team_leader').order_by('name')
        context['team'] = team
        context['name'] = self.request.GET.get('name', '')
        context['use'] = self.request.GET.get('use', '사용')
        context['role'] = self.request.GET.get('role', '담당업무')
        return context

def route_team_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session['user'])
        team_form = RouteTeamForm(request.POST)
        if team_form.is_valid():
            team_form.save(creator=creator)

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        raise BadRequest(f"{team_form.errors}")
    else:
        return HttpResponseNotAllowed(['POST'])

def route_team_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        id = request.POST.get('id', None)

        team = get_object_or_404(RouteTeam, id=id)

        team_form = RouteTeamForm(request.POST, instance=team)
        if team_form.is_valid():
            team_form.save()
        else:
            raise BadRequest(f"{team_form.errors}")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def route_team_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        team = get_object_or_404(RouteTeam, id=request.POST.get('id', None))
        team.delete()
            
            
        return redirect('dispatch:route_team')
    else:
        return HttpResponseNotAllowed(['POST'])

def route_team_save(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        route_list = request.POST.getlist('id', None)
        team_list = request.POST.getlist('team_id', None)
        
        
        for index, route_id in enumerate(route_list):
            route = get_object_or_404(DispatchRegularlyData, id=route_id)
            team_id = team_list[index]
            if team_id == 'none':
                route.team = None
            else:
                team = get_object_or_404(RouteTeam, id=team_id)
                route.team = team
            route.save()
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
        # 4시부터
        count = 4
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

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
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
        values = self.request.GET.get('values', '')
        date = self.request.GET.get('date', TODAY)

        id_list = values.split(',')

        # id_list로 정렬, alcohol_test 값 가져오기
        queryset = DispatchRegularlyConnect.objects.filter(id__in=id_list).annotate(
            custom_ordering=Case(
                *[When(id=id, then=Value(index)) for index, id in enumerate(id_list)],
                output_field=IntegerField()
            ),
            alcohol_test=Subquery(
                MorningChecklist.objects.filter(
                    member=OuterRef('driver_id'),
                    date__startswith=date
                ).values('alcohol_test')[:1]
            )
        ).order_by('custom_ordering')

        return queryset.select_related('regularly_id')
    
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
            
            # rpap tour
            context['customer_list'] = DispatchOrderTourCustomer.objects.filter(tour_id__order_id=context['detail'])
            context['tour'] = DispatchOrderTour.objects.filter(order_id=context['detail']).first()


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
        
        context['vehicles'] = Vehicle.objects.filter(use='사용').order_by('vehicle_num', 'driver__name')
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

def edit_rpap_estimate_value(order, field, message):
    firebase = RpaPFirebase()
    estimate_path = order.firebase_path
    # isEstimateApproval이 false면 값 변경, 알림 보냄
    if (not firebase.get_value(estimate_path, field)):
        estimate_data = firebase.edit_value(estimate_path, field, True)
        
        # rpap 유저에게 알림보내기
        user_uid = estimate_path.split("/Estimate")[0]
        fcm_token = firebase.get_value(user_uid, "fcmToken")
        send_message(message, f'{order.route}\n{order.departure_date} ~ {order.arrival_date}', fcm_token, None)


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
            # get_order_distance_and_time(order)

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
        order_form = OrderForm(request.POST, instance=order)

        if order_form.is_valid():
            order = order_form.save(commit=False)

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

            order.departure_date = departure_date
            order.arrival_date = arrival_date
            order.price = price
            order.driver_allowance = driver_allowance
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

            # rpap
            if order.firebase_path and order.contract_status == "예약확정":
                edit_rpap_estimate_value(order, "isEstimateApproval", '견적 예약이 완료되었습니다!')
            if order.firebase_path and order.contract_status == "확정":
                edit_rpap_estimate_value(order, "isCompletedReservation", "운행이 확정되었습니다!")

            # 경유지 처리
            old_stations = order.station.all()
            old_stations.delete()
            try:
                create_order_stations(request, order, creator)
            except Exception as e:
                raise BadRequest("정류장 정보를 잘못 입력하셨습니다.", e)
            
            # 노선의 정류장에서 정류장 사이의 거리, 시간 측정해서 저장
            # get_order_distance_and_time(order)

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def create_order_stations(request, order, creator):
    waypoint_list = request.POST.getlist('station_name')
    waypoint_time_list = request.POST.getlist('station_time')
    delegate_list = request.POST.getlist('delegate')
    delegate_phone_list = request.POST.getlist('delegate_phone')
    for i in range(len(waypoint_list)):
        waypoint = DispatchOrderStation(
            order_id=order,
            station_name=waypoint_list[i],
            time=waypoint_time_list[i],
            delegate=delegate_list[i] if delegate_list[i] != " " else '',
            delegate_phone=delegate_phone_list[i] if delegate_phone_list[i] != " " else '',
            creator=creator,
        )
        waypoint.save()

def order_delete(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
        
    if request.method == "POST":
        id_list = request.POST.getlist('id', None)
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')

        for id in id_list:
            order = get_object_or_404(DispatchOrder, id=id)

            #rpap
            if order.firebase_path:
                firebase = RpaPFirebase()
                firebase.delete_doc(order.firebase_path)

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

def order_tour_save(request):
    if request.session.get('authority') > 2:
        return render(request, 'authority.html')
    if request.method == "GET":
        return HttpResponseNotAllowed(['POST'])

    tour_id = request.POST.get("tour_id")
    if tour_id:
        tour_form = TourForm(request.POST, instance=get_object_or_404(DispatchOrderTour, id=tour_id))
    else:
        tour_form = TourForm(request.POST)
    
    if tour_form.is_valid():
        creator = get_object_or_404(Member, id=request.session.get('user'))
        order = get_object_or_404(DispatchOrder, id=request.POST.get('order_id', ''))
        tour = tour_form.save(commit=False)
        tour.creator = creator
        tour.order_id = order
        tour.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    raise BadRequest(f"{tour_form.errors}")


def order_tour_customer_save(request):
    if request.session.get('authority') > 2:
        return render(request, 'authority.html')
    if request.method == "GET":
        return HttpResponseNotAllowed(['POST'])
    
    # 신규 생성
    if request.POST.getlist("new_payment_status"):
        new_pay_datetime_list = request.POST.getlist("new_pay_datetime")
        new_payment_status_list = request.POST.getlist("new_payment_status")
        name_list = request.POST.getlist("name")
        phone_list = request.POST.getlist("phone")
        bank_list = request.POST.getlist("bank")

        tour = get_object_or_404(DispatchOrderTour, id=request.POST.get("tour_id"))

        if len(new_pay_datetime_list) + DispatchOrderTour.tour_customer.count() > tour.max_people:
            raise BadRequest("최대 예약 인원을 초과했습니다.")
        
        for pay_datetime, payment_status, name, phone, bank in zip(new_pay_datetime_list, new_payment_status_list, name_list, phone_list, bank_list):
            DispatchOrderTourCustomer.objects.create(
                tour_id=tour,
                name=name,
                phone=phone,
                bank=bank,
                pay_datetime=pay_datetime,
                payment_status=payment_status,
                creator = get_object_or_404(Member, id=request.session.get('user')),
            )
        
        # 최대 인원일 떄 파이어베이스 데이터 모집 마감으로 변경
        if len(new_pay_datetime_list) + DispatchOrderTour.tour_customer.count() == tour.max_people:
            edit_rpap_tour_value(tour, "status", "1")
        
    # 기존 값 수정
    pay_datetime_list = request.POST.getlist("pay_datetime")
    payment_status_list = request.POST.getlist("payment_status")
    edit_customer_list = request.POST.getlist("edit_customer")

    for pay_datetime, payment_status, customer_id in zip(pay_datetime_list, payment_status_list, edit_customer_list):
        customer = get_object_or_404(DispatchOrderTourCustomer, id=customer_id)
        customer.pay_datetime = pay_datetime
        customer.payment_status = payment_status
        customer.save()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def edit_rpap_tour_value(tour, field, value):
    firebase = RpaPFirebase()
    path = TOUR_PATH + tour.firebase_uid
    # isEstimateApproval이 false면 값 변경, 알림 보냄
    estimate_data = firebase.edit_value(path, field, value)

def order_tour_customer_delete(request):
    if request.session.get('authority') > 2:
        return render(request, 'authority.html')
    if request.method == "GET":
        return HttpResponseNotAllowed(['POST'])
    
    delete_list = request.POST.getlist("delete")
    for delete_id in delete_list:
        customer = get_object_or_404(DispatchOrderTourCustomer, id=delete_id)
        customer.delete()

    # TODO 최대 인원 아닐때 파이어베이스 데이터 모집으로 변경

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def line_print(request):
    if request.session.get('authority') > 3:
        return render(request, 'authority.html')
    
    context = {}
    date = request.GET.get('date')
    week = WEEK2[datetime.strptime(date, FORMAT).weekday()]

    connect_list = DispatchRegularlyConnect.objects.filter(
        departure_date__startswith=date
    ).order_by(
        'regularly_id__group__number', 'departure_date', 'regularly_id__num1', 'regularly_id__number1', 'regularly_id__num2', 'regularly_id__number2'
    ).select_related(
        'regularly_id', 'driver_id', 'bus_id', 'regularly_id__group'
    ).values(
        'regularly_id__departure_time',
        'regularly_id__number1',
        'regularly_id__number2',
        'regularly_id__departure',
        'regularly_id__arrival',
        'regularly_id__references',
        'driver_id__name',
        'bus_id__vehicle_num',
        'regularly_id__group__name'
    )

    group = connect_list[0]['regularly_id__group__name']
    temp = []
    context['connect_list'] = []
    for connect in connect_list:
        if group != connect['regularly_id__group__name']:
            context['connect_list'].append(temp)
            group = connect['regularly_id__group__name']
            temp = [connect]
        else:
            temp.append(connect)
    context['connect_list'].append(temp)



    # 쿼리 최적화
    # regulalry_data_list = (
    #     DispatchRegularlyData.objects
    #     .filter(use='사용', week__contains=week)
    #     .select_related('group', 'team')
    #     .order_by('group', 'num1', 'number1', 'num2', 'number2')
    # )

    # regularly_list = []
    # no_list = []

    # for regularly_data in regulalry_data_list:
    #     # 해당 정기 배차 데이터의 monthly 중 가장 적절한 레코드 찾기
    #     monthly_queryset = DispatchRegularly.objects.filter(
    #         regularly_id=regularly_data,
    #         use='사용',
    #         edit_date__lte=date
    #     ).order_by('-edit_date')

    #     # 과거 날짜 기준 레코드가 없으면 미래 날짜 중 가장 가까운 레코드 찾기
    #     dispatch = monthly_queryset.first()
    #     if not dispatch:
    #         dispatch = DispatchRegularly.objects.filter(
    #             regularly_id=regularly_data,
    #             use='사용',
    #             edit_date__gte=date
    #         ).order_by('edit_date').first()

    #     # 해당 날짜에 연결된 노선 확인
    #     if dispatch:
    #         dispatch_connect = dispatch.info_regularly.filter(departure_date__startswith=date).exists()
            
    #         if dispatch_connect:
    #             regularly_list.append(dispatch)
    #         else:
    #             no_list.append(dispatch)

    # # 그룹핑 처리
    # context['regularly_list'] = [
    #     list(group) 
    #     for _, group in itertools.groupby(regularly_list, key=lambda x: x.group.name)
    # ]

    
    # for regularly_list in context['regularly_list']:
    #     temp = []
    #     for regularly in regularly_list:
    #         temp.append(regularly.info_regularly.filter(departure_date__startswith=date).first())
    #     context['connect_list'].append(temp)

    # context['connect_list'] = [
    #     list(dispatch.info_regularly.filter(departure_date__startswith=date))
    #     for dispatch in regularly_list
    # ]

    # context['no_list'] = no_list

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
        member_list = Member.objects.filter(authority__gte=1).order_by('name')
    
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
    context['cnt'] = len(id_list)
    context['date'] = date


    # 배차 데이터 불러오기
    regularly_list = DispatchRegularlyConnect.objects.filter(departure_date__startswith=date).filter(driver_id__in=id_list).order_by('departure_date').annotate(
        departure_km=F("driving_history_regularly__departure_km"),
        arrival_km=F("driving_history_regularly__arrival_km"),
        passenger_num=F("driving_history_regularly__passenger_num"),
        departure=F('regularly_id__departure'),
        arrival=F('regularly_id__arrival'),
        bus_num=F('bus_id__vehicle_num'),
    ).values(
        'departure_km',
        'arrival_km',
        'passenger_num',
        'departure_date',
        'arrival_date',
        'departure',
        'arrival',
        'driver_id',
        'driver_id__name',
        'bus_num',
        'bus_id',
    )
    order_list = DispatchOrderConnect.objects.filter(departure_date__lte=f'{date} 24:00').filter(arrival_date__gte=f'{date} 00:00').filter(driver_id__in=id_list).order_by('departure_date').annotate(
        departure_km=F("driving_history_order__departure_km"),
        arrival_km=F("driving_history_order__arrival_km"),
        passenger_num=F("driving_history_order__passenger_num"),
        departure=F('order_id__departure'),
        arrival=F('order_id__arrival'),
        bus_num=F('bus_id__vehicle_num'),
    ).values(
        'departure_km',
        'arrival_km',
        'passenger_num',
        'departure_date',
        'arrival_date',
        'departure',
        'arrival',
        'driver_id',
        'driver_id__name',
        'bus_num',
        'bus_id',
    )
    # 두 데이터 리스트 합치기
    combined_data = list(regularly_list) + list(order_list)
    # departure_date 기준으로 정렬
    combined_data = sorted(combined_data, key=lambda x: x["departure_date"])
    
    context['connect_data'] = []
    for id in id_list:
        # 해당 기사의 데이터 필터링
        driver_data = [
            item for item in combined_data 
            if item['driver_id'] == int(id)
        ]
        
        # 버스 번호로 데이터 분류
        vehicle_groups = {}
        for item in driver_data:
            vehicle_num = item['bus_num']
            vehicle_id = item['bus_id']
            
            # 각 차량별로 별도의 데이터 그룹 생성
            if vehicle_id not in vehicle_groups:
                vehicle_groups[vehicle_id] = {
                    'driver': item['driver_id__name'],
                    'bus_num': vehicle_num,
                    'data': [],
                    'bus_id': vehicle_id
                }
            
            vehicle_groups[vehicle_id]['data'].append(item)
        
        # 각 차량 데이터를 context['connect_data']에 추가
        for vehicle_id, vehicle_data in vehicle_groups.items():
            # 첫번째와 마지막 데이터의 km 설정
            if vehicle_data['data']:
                vehicle_data['departure_km'] = vehicle_data['data'][0]['departure_km']
                vehicle_data['arrival_km'] = vehicle_data['data'][-1]['arrival_km']
            
            context['connect_data'].append(vehicle_data)
    
    # test
    for test in context['connect_data']:
        print(test)
            
        print()

    # 해당 날짜의 주유 데이터 가져오기
    refueling_list = Refueling.objects.filter(refueling_date__startswith=date).filter(driver__in=id_list).order_by('refueling_date').values(
        'refueling_date',
        'km',
        'refueling_amount',
        'urea_solution',
        'driver_id',
        'driver__name',
        'vehicle',
    )

    # context['connect_data']에 주유 데이터 추가
    for driver_data in context['connect_data']:
        driver_id = driver_data['data'][0]['driver_id']
        driver_bus_id = driver_data['data'][0]['bus_id']
        
        # 해당 기사, 해당 차량의 주유 데이터 필터링
        driver_refueling_data = [
            item for item in refueling_list 
            if item['driver_id'] == driver_id and item['vehicle'] == driver_bus_id
        ]

        # 주유량과 요소수 합계 계산
        if driver_refueling_data:
            # 문자열로 된 값을 숫자로 변환하여 합계 계산
            total_refueling_amount = sum(int(item['refueling_amount']) for item in driver_refueling_data)
            total_urea_solution = sum(int(item['urea_solution']) for item in driver_refueling_data)
            
            driver_data['refueling'] = {
                'refueling_amount': total_refueling_amount,
                'urea_solution': total_urea_solution,
            }
        else:
            # 주유 데이터가 없는 경우 0으로 초기화
            driver_data['refueling'] = {
                'refueling_amount': 0,
                'urea_solution': 0
            }

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
    