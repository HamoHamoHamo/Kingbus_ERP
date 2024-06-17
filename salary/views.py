

from config.settings import MEDIA_ROOT
from django.db.models import Q, Sum
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from config.custom_logging import logger
from dispatch.models import DispatchRegularlyData, MorningChecklist, EveningChecklist
from dispatch.selectors import DispatchSelector
from humanresource.models import Member
from humanresource.selectors import MemberSelector
from common.constant import TODAY
from common.datetime import calculate_time_difference, get_hour_minute_with_colon, get_hour_minute, get_minute_from_colon_time, last_day_of_month, get_weekday_from_date
from datetime import datetime, timedelta

class SalaryStatus(generic.ListView):
    template_name = 'salary/status.html'
    context_object_name = 'member_list'
    model = Member

    class DataCollector:
        def __init__(self, member, month):
            self.member = member
            self.month = month
            self.connect_time_list = []
            self.morning_list = []
            self.evening_list = []
            self.last_day = last_day_of_month(f"{month}-01")

        def collect_connects(self, connect_time_list):
            self.connect_time_list = list(filter(lambda item: item['driver_id'] == self.member.id, connect_time_list))

        def collect_morning(self, morning_list):
            self.morning_list = list(filter(lambda item: item['member'] == self.member.id, morning_list))

        def collect_evening(self, evening_list):
            self.evening_list = list(filter(lambda item: item['member'] == self.member.id, evening_list))

        def get_morning_time(self, date, morning_data):
            if len(morning_data) > 1:
                logger.warning(f"아침 점호는 1일 당 1개만 있어야 됨 {date} {self.member.name}")
            return morning_data[0]['arrival_time'] if morning_data else ''

        def get_evening_time(self, date, evening_data):
            if len(evening_data) > 1:
                logger.warning(f"저녁 점호는 1일 당 1개만 있어야 됨 {date} {self.member.name}")
            return datetime.strftime(evening_data[0]['updated_at'], '%Y-%m-%d %H:%M')[11:] if evening_data else ''

        def get_work_time(self, daily_connects):
            minutes = sum(calculate_time_difference(connect['departure_date'], connect['arrival_date']) for connect in daily_connects)
            return get_hour_minute_with_colon(minutes) if minutes else '', minutes

        def get_wait_time(self, morning_time, evening_time, work_time):
            if morning_time and evening_time and work_time:
                return get_hour_minute_with_colon(
                    get_minute_from_colon_time(evening_time) -
                    get_minute_from_colon_time(morning_time) -
                    get_minute_from_colon_time(work_time)
                )
            return ''

        def get_work_type(self, minutes, weekday):
            if minutes > 0:
                return '근무'
            elif weekday == '일':
                return '주휴'
            else:
                return '비번'
                

        from datetime import datetime, timedelta

        def calculate_night_shift_minutes(self, departure_date, arrival_date):
            # 출발 및 도착 시간 설정
            departure = datetime.strptime(departure_date, '%Y-%m-%d %H:%M')
            arrival = datetime.strptime(arrival_date, '%Y-%m-%d %H:%M')
            
            # 야근 시작 및 종료 시간 설정
            night_start = datetime.strptime(departure_date[:10] + ' 00:00', '%Y-%m-%d %H:%M')
            night_end = datetime.strptime(departure_date[:10] + ' 06:00', '%Y-%m-%d %H:%M')
            mid_night_start = datetime.strptime(departure_date[:10] + ' 22:00', '%Y-%m-%d %H:%M')
            mid_night_end = datetime.strptime(departure_date[:10] + ' 23:59', '%Y-%m-%d %H:%M')
            
            # 야근 시간 계산 변수 초기화
            night_shift_minutes = 0

            # 00:00 ~ 06:00 시간대 야근 시간 계산
            if departure < night_end:
                if arrival > night_start:
                    night_shift_minutes += (min(arrival, night_end) - max(departure, night_start)).seconds // 60

            # 22:00 ~ 23:59 시간대 야근 시간 계산
            if departure < mid_night_end:
                if arrival > mid_night_start:
                    night_shift_minutes += (min(arrival, mid_night_end) - max(departure, mid_night_start)).seconds // 60

            return night_shift_minutes
        
        def get_night_shift_time(self, daily_connects):
            minutes = 0
            for connect in daily_connects:
                # 지금은 일반배차 제외하고 야근시간 계산
                if connect['work_type'] != '일반' and connect['departure_date'] and connect['arrival_date']:
                    minutes += self.calculate_night_shift_minutes(connect['departure_date'], connect['arrival_date'])
                
            return minutes
        
        
        def collect_daily_data(self, i):
            date = f"{self.month}-{i + 1:02d}"
            weekday = get_weekday_from_date(date)
            morning_data = list(filter(lambda item: item['date'] == date, self.morning_list))
            evening_data = list(filter(lambda item: item['date'] == date, self.evening_list))
            daily_connects = list(filter(lambda item: item['departure_date'][:10] == date, self.connect_time_list))

            morning_time = self.get_morning_time(date, morning_data)
            evening_time = self.get_evening_time(date, evening_data)
            work_time, minutes = self.get_work_time(daily_connects)
            work_type = self.get_work_type(minutes, weekday)
            wait_time = self.get_wait_time(morning_time, evening_time, work_time)
            night_shift_time = self.get_night_shift_time(daily_connects)
            

            return morning_time, evening_time, work_time, wait_time, work_type, minutes, night_shift_time

        def collect_data(self):
            morning_time_list = ['' for i in range(31)]
            evening_time_list = ['' for i in range(31)]
            work_time_list = ['' for i in range(31)]
            wait_time_list = ['' for i in range(31)]
            night_shift_time_list = ['' for i in range(31)]
            work_list = ['' for i in range(31)]
            total_work_minute = 0
            total_night_shift_minute = 0

            for i in range(self.last_day):
                morning_time, evening_time, work_time, wait_time, work_type, minutes, night_shift_time = self.collect_daily_data(i)
                morning_time_list[i] = morning_time
                evening_time_list[i] = evening_time
                work_time_list[i] = work_time
                wait_time_list[i] = wait_time
                work_list[i] = work_type
                night_shift_time_list[i] = get_hour_minute_with_colon(night_shift_time) if night_shift_time > 0 else ''
                total_work_minute += minutes
                total_night_shift_minute += night_shift_time

            return {
                'morning_time_list': morning_time_list,
                'evening_time_list': evening_time_list,
                'work_time_list': work_time_list,
                'wait_time_list': wait_time_list,
                'night_shift_time_list': night_shift_time_list,
                'total_work_minute': get_hour_minute(total_work_minute),
                'total_night_shift_minute': get_hour_minute(total_night_shift_minute),
                'work_list': work_list,
                'work_count': work_list.count('근무'),
                'off_duty_count': work_list.count('비번'),
                'weekly_holiday_count': work_list.count('주휴'),
                'total_count': len(work_list) - work_list.count(''),
            }


    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        name = self.request.GET.get('name', '')
        member_selector = MemberSelector()
        return member_selector.get_using_driver_list(name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['name'] = self.request.GET.get('name', '')
        context['month'] = self.request.GET.get('month', TODAY[:7])
        dispatch_selector = DispatchSelector()
        
        connect_time_list = dispatch_selector.get_monthly_driving_time_list(context['month'])
        morning_list = dispatch_selector.get_monthly_morning_checklist(context['month'])
        evening_list = dispatch_selector.get_monthly_evening_checklist(context['month'])
        
        datas = {}
        context['weekday_list'] = ['' for i in range(31)]
        context['date_list'] = ['' for i in range(31)]

        for i in range(last_day_of_month(f"{context['month']}-01")):
            date = f"{context['month']}-{i + 1:02d}"
            context['weekday_list'][i] = get_weekday_from_date(date)
            context['date_list'][i] = i + 1


        for member in context['member_list']:
            data_collector = self.DataCollector(member, context['month'])
            data_collector.collect_connects(connect_time_list)
            data_collector.collect_morning(morning_list)
            data_collector.collect_evening(evening_list)
            datas[member.id] = data_collector.collect_data()
            
 
        context['datas'] = datas
        return context

class SalaryStatusBackup(generic.ListView):
    template_name = 'salary/status2.html'
    context_object_name = 'member_list'
    model = Member

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        member_selector = MemberSelector()
        return member_selector.get_using_driver_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['month'] = self.request.GET.get('month', TODAY[:7])
        dispatch_selector = DispatchSelector()
        
        connect_time_list = dispatch_selector.get_monthly_driving_time_list(context['month'])

        for member in context['member_list']:
            
            list(filter(lambda item : item['driver_id'] == member.id, connect_time_list))
        
        return context