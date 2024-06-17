

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
from common.datetime import calculate_time_difference, get_hour_minute_with_colon, get_hour_minute, get_minute_from_colon_time
from datetime import datetime

class SalaryStatus(generic.ListView):
    template_name = 'salary/status.html'
    context_object_name = 'member_list'
    model = Member

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
        for member in context['member_list']:
            member_connects = list(filter(lambda item : item['driver_id'] == member.id, connect_time_list))
            morning = list(filter(lambda item : item['member'] == member.id, morning_list))
            evening = list(filter(lambda item : item['member'] == member.id, evening_list))

            morning_time_list = ['' for i in range(31)]
            evening_time_list = ['' for i in range(31)]
            work_time_list = ['' for i in range(31)]
            wait_time_list = ['' for i in range(31)]
            work_total_minute = 0
            work_count = 0
            work_list = ['' for i in range(31)]
            for i in range(31):
                date = f"{context['month']}-{i + 1}" if i + 1 > 9 else f"{context['month']}-0{i + 1}"
                print("DATEEEEE", date)
                date_morning = list(filter(lambda item : item['date'] == date, morning))
                if len(date_morning) > 1:
                    logger.warning(f"아침 점호는 1일 당 1개만 있어야 됨 {date} {member.name}")
                if date_morning:
                    morning_time_list[i] = date_morning[0]['arrival_time']

                # 지금은 저녁점호 업데이트 한 시간으로 불러옴, 나중에는 기사가 직접 입력한 date 불러오게 수정
                date_evening = list(filter(lambda item : item['date'] == date, evening))
                if len(date_evening) > 1:
                    logger.warning(f"저녁 점호는 1일 당 1개만 있어야 됨 {date} {member.name}")
                if date_evening:
                    evening_time_list[i] = (datetime.strftime(date_evening[0]['updated_at'], '%Y-%m-%d %H:%M')[11:]) 

                # 지금은 노선의 도착시간 - 출발시간으로 계산해서 총 근무시간 계산하는데 나중에는 카카오api로 나온 시간을 더해서 계산
                daily_connects = list(filter(lambda item : item['departure_date'][:10] == date, member_connects))
                minutes = 0
                for connect in daily_connects:
                    minutes += calculate_time_difference(connect['departure_date'], connect['arrival_date'])
                time_data = get_hour_minute_with_colon(minutes)
                work_time_list[i] = time_data if time_data != "00:00" else ''
                work_total_minute += minutes

                # 근무 구분, 근무일 카운트
                if minutes > 0:
                    work_list[i] = '근무'
                    work_count += 1
                else:
                    work_list[i] = ''

                # 대기 시간 계산
                if morning_time_list[i] and evening_time_list[i] and work_time_list[i]:
                    wait_time_list[i] = get_hour_minute_with_colon(get_minute_from_colon_time(evening_time_list[i]) - get_minute_from_colon_time(morning_time_list[i]) - get_minute_from_colon_time(work_time_list[i]))
            
            datas[member.id] = {
                'morning_time_list' : morning_time_list,
                'evening_time_list' : evening_time_list,
                'work_time_list' : work_time_list,
                'wait_time_list' : wait_time_list,
                'work_total_minute' : get_hour_minute(work_total_minute),
                'work_list' : work_list,
                'work_count' : work_count,
            }
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