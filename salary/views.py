from config.settings import MEDIA_ROOT
from django.db.models import Q, Sum
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from datetime import datetime, timedelta

from .forms import HourlyWageForm
from .selectors import SalarySelector
from .services import SalaryStatusDataCollector, SalaryTableDataCollector, SalaryTableDataCollector2, SalaryTableDataCollector3
from .models import HourlyWage
from config.custom_logging import logger
from dispatch.models import DispatchRegularlyData, MorningChecklist, EveningChecklist
from dispatch.selectors import DispatchSelector
from humanresource.models import Member, Salary
from humanresource.selectors import MemberSelector
from common.constant import TODAY
from common.datetime import *
from common.views import AuthorityCheckView

class SalaryStatus(AuthorityCheckView, generic.ListView):
    template_name = 'salary/status.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def set_search_duration(self):
        start_day = 1
        last_day = last_day_of_month(TODAY)
        return start_day, last_day

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        member_selector = MemberSelector()
        return member_selector.get_using_driver_list(name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['name'] = self.request.GET.get('name', '')
        context['month'] = self.request.GET.get('month', TODAY[:7])

        start_day, last_day = self.set_search_duration()
        first_date = f"{context['month']}-01"
        mondays = get_mondays_from_last_week_of_previous_month(context['month'])
        start_date = mondays[0] if mondays[0][:7] != context['month'] else first_date

        last_date = last_date_of_month(first_date)
        context['date_list'] = get_date_range_list(first_date, last_date)

        # 불러온 월요일부터 배차 데이터 가져오기
        dispatch_selector = DispatchSelector()
        connect_time_list = dispatch_selector.get_driving_time_list(start_date, last_day_of_month(first_date))
        holiday_data = get_holiday_list_from_open_api(context['month'])

        morning_list = dispatch_selector.get_monthly_morning_checklist(context['month'])
        evening_list = dispatch_selector.get_monthly_evening_checklist(context['month'])
        
        datas = {}
        context['weekday_list'] = ['' for i in range(31)]
        context['day_list'] = ['' for i in range(31)]

        for i in range(last_day_of_month(first_date)):
            date = f"{context['month']}-{i + 1:02d}"
            context['weekday_list'][i] = get_weekday_from_date(date)
            context['day_list'][i] = i + 1

        for member in context['member_list']:
            data_collector = SalaryStatusDataCollector(member, context['month'], mondays, connect_time_list, holiday_data, context['date_list'])
            data_collector.collect_morning(morning_list)
            data_collector.collect_evening(evening_list)

            data_collector.set_duration(start_day, last_day)
            datas[member.id] = data_collector.get_calculate_times()
            
 
        context['datas'] = datas
        return context


class DailySalaryStatus(AuthorityCheckView, generic.ListView):
    template_name = 'salary/daily_status.html'
    context_object_name = 'member_list'
    model = Member

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        member_selector = MemberSelector()
        return member_selector.get_using_driver_list(name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['name'] = self.request.GET.get('name', '')
        context['date'] = self.request.GET.get('date', TODAY)
        
        first_date = context['date']
        last_date = context['date']
        context['date_list'] = get_date_range_list(first_date, last_date)

        # 불러온 월요일부터 배차 데이터 가져오기
        dispatch_selector = DispatchSelector()
        connect_time_list = dispatch_selector.get_driving_time_list(first_date, last_date)
        holiday_data = get_holiday_list_from_open_api(first_date[:7])

        morning_list = dispatch_selector.get_morning_checklist(first_date, last_date)
        evening_list = dispatch_selector.get_evening_checklist(first_date, last_date)
        
        datas = {}
        context['day_list'] = ['' for i in range(7)]
        count = 0
        for date in context['date_list']:
            context['day_list'][count] = date[8:10]
            count += 1

        for member in context['member_list']:
            data_collector = SalaryStatusDataCollector(member, first_date[:7], [], connect_time_list, holiday_data, context['date_list'])
            data_collector.collect_morning(morning_list)
            data_collector.collect_evening(evening_list)

            data_collector.set_duration(first_date, last_date)
            calculated_data = data_collector.get_calculate_times()
            calculated_data['connects_time_list'] = data_collector.get_connects_time_list(first_date)
            datas[member.id] = calculated_data
            
 
        context['datas'] = datas
        return context
    


class WeeklySalaryStatus(AuthorityCheckView, generic.ListView):
    template_name = 'salary/weekly_status.html'
    context_object_name = 'member_list'
    model = Member

    def get_week_dates(self, week_str):
        # 문자열을 분리하여 년도와 주차를 추출
        year, week = map(int, week_str.split('-W'))
        # 해당 년도의 첫 번째 날을 구함
        first_day_of_year = datetime(year, 1, 1)
        # 첫 번째 날의 요일 (월요일이 0, 일요일이 6)
        first_weekday = first_day_of_year.weekday()
        # 첫 번째 주의 첫 번째 날을 구함
        if first_weekday <= 3:
            first_week_start = first_day_of_year - timedelta(days=first_weekday)
        else:
            first_week_start = first_day_of_year + timedelta(days=7 - first_weekday)
        # 해당 주차의 첫 번째 날과 마지막 날을 구함
        start_date = first_week_start + timedelta(weeks=week - 1)
        end_date = start_date + timedelta(days=6)
        # 형식에 맞게 반환
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    def date_to_week(self, date_str):
        # 문자열을 datetime 객체로 변환
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # 년도와 주차 계산 (ISO 달력 기준, 월요일을 한 주의 시작으로 간주)
        year, week, _ = date_obj.isocalendar()
        # 형식에 맞게 문자열로 반환
        return f"{year}-W{week:02d}"

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        member_selector = MemberSelector()
        return member_selector.get_using_driver_list(name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['name'] = self.request.GET.get('name', '')
        context['week'] = self.request.GET.get('week', self.date_to_week(TODAY))
        
        first_date, last_date = self.get_week_dates(context['week'])
        context['date_list'] = get_date_range_list(first_date, last_date)
        print(context['date_list'])

        # 불러온 월요일부터 배차 데이터 가져오기
        dispatch_selector = DispatchSelector()
        connect_time_list = dispatch_selector.get_driving_time_list(first_date, last_date)
        holiday_data = get_holiday_list_from_open_api(first_date[:7])

        morning_list = dispatch_selector.get_morning_checklist(first_date, last_date)
        evening_list = dispatch_selector.get_evening_checklist(first_date, last_date)
        
        datas = {}
        context['day_list'] = ['' for i in range(7)]
        count = 0
        for date in context['date_list']:
            context['day_list'][count] = date[8:10]
            count += 1

        for member in context['member_list']:
            data_collector = SalaryStatusDataCollector(member, first_date[:7], [], connect_time_list, holiday_data, context['date_list'])
            data_collector.collect_morning(morning_list)
            data_collector.collect_evening(evening_list)

            data_collector.set_duration(first_date, last_date)
            datas[member.id] = data_collector.get_calculate_times()
            
 
        context['datas'] = datas
        return context

class SalaryDataController(AuthorityCheckView):
    def get_datas(self, member_list, data_collector_class, month, mondays, connect_time_list, holiday_data, date_list):
        datas = {}
        for member in member_list:
            data_collector = data_collector_class(member, month, mondays, connect_time_list, holiday_data, date_list)
            datas[member.id] = data_collector.get_collected_data()
            datas[member.id]['member'] = member
        return datas



class SalaryTable(AuthorityCheckView, generic.ListView):
    template_name = 'salary/table.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3
    data_collector_class = SalaryTableDataCollector

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        search_type = self.request.GET.get("type", '전체')

        member_selector = MemberSelector()
        
        if search_type == '전체':
            member_list = member_selector.get_using_driver_list(name)
        elif search_type == '정규직':
            member_list = member_selector.get_using_permanent_driver_list(name)
        elif search_type == '일당직':
            member_list = member_selector.get_using_outsourcing_driver_list(name)
        return member_list
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = self.request.GET.get('name', '')
        context['type'] = self.request.GET.get('type', '전체')
        context['month'] = self.request.GET.get('month', TODAY[:7])

        first_date = f"{context['month']}-01"
        # 1일이 월요일이 아닌경우 저번달 마지막주 월요일부터 불러오기
        date_list = get_date_range_list(first_date, last_date_of_month(first_date))

        mondays = get_mondays_from_last_week_of_previous_month(context['month'])
        start_date = mondays[0] if mondays[0][:7] != context['month'] else first_date

        salary_selector = SalarySelector()
        context['hourly_wage'] = salary_selector.get_hourly_wage_by_month(context['month'])

        # 불러온 월요일부터 배차 데이터 가져오기
        dispatch_selector = DispatchSelector()
        connect_time_list = dispatch_selector.get_driving_time_list(start_date, get_next_sunday_after_last_day(context['month']))

        # TODO 휴일 데이터 db에 저장하기
        holiday_data = get_holiday_list_from_open_api(context['month'])
        context['date_list'] = ['' for i in range(31)]

        for i in range(last_day_of_month(first_date)):
            context['date_list'][i] = i + 1

        data_controller = SalaryDataController()
        context['datas'] = data_controller.get_datas(context['member_list'], self.data_collector_class, context['month'], mondays, connect_time_list, holiday_data, date_list)
        #datas = {}
        #for member in context['member_list']:
        #    data_collector = self.data_collector_class(member, context['month'], mondays, connect_time_list, holiday_data, date_list)
        #    datas[member.id] = data_collector.get_collected_data()
            
        #context['datas'] = datas
        return context

class SalaryTable2(SalaryTable):
    template_name = 'salary/table2.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3
    data_collector_class = SalaryTableDataCollector2

class SalaryTable3(SalaryTable):
    template_name = 'salary/table3.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3
    data_collector_class = SalaryTableDataCollector3



class HourlyWageSaveView(AuthorityCheckView):
    authority_level = 3

    def get(self, request, *args, **kwargs):
        # GET 요청을 처리하는 메소드
        return HttpResponseNotAllowed(['post'])
    
    def post(self, request, *args, **kwargs):
        month = self.request.POST.get('month', TODAY[:7])
        salary_selector = SalarySelector()
        old_hourly_wage = salary_selector.get_hourly_wage_by_month(month)

        hourly_wage_form = HourlyWageForm(request.POST, instance=old_hourly_wage) if old_hourly_wage else HourlyWageForm(request.POST)
        
        if hourly_wage_form.is_valid():
            hourly_wage = hourly_wage_form.save(commit=False)
            hourly_wage.creator = self.creator
            hourly_wage.save()
        
            # 급여 연차수당 수정
            
            salary_list = Salary.objects.filter(month=month)
            for salary in salary_list:
                salary.new_annual_allowance = Salary.set_new_annual_allowance(month, salary.member_id)
                salary.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        raise BadRequest(hourly_wage_form.errors)

