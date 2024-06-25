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
from .services import SalaryStatusDataCollector, SalaryTableDataCollector
from .models import HourlyWage
from config.custom_logging import logger
from dispatch.models import DispatchRegularlyData, MorningChecklist, EveningChecklist
from dispatch.selectors import DispatchSelector
from humanresource.models import Member, Salary
from humanresource.selectors import MemberSelector
from common.constant import TODAY
from common.datetime import last_day_of_month, get_weekday_from_date, get_mondays_from_last_week_of_previous_month, get_holiday_list_from_open_api
from common.views import AuthorityCheckView

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

        first_date = f"{context['month']}-01"
        mondays = get_mondays_from_last_week_of_previous_month(context['month'])
        start_date = mondays[0] if mondays[0][:7] != context['month'] else first_date

        # 불러온 월요일부터 배차 데이터 가져오기
        dispatch_selector = DispatchSelector()
        connect_time_list = dispatch_selector.get_driving_time_list(start_date, last_day_of_month(first_date))
    
        morning_list = dispatch_selector.get_monthly_morning_checklist(context['month'])
        evening_list = dispatch_selector.get_monthly_evening_checklist(context['month'])
        
        datas = {}
        context['weekday_list'] = ['' for i in range(31)]
        context['date_list'] = ['' for i in range(31)]

        for i in range(last_day_of_month(first_date)):
            date = f"{context['month']}-{i + 1:02d}"
            context['weekday_list'][i] = get_weekday_from_date(date)
            context['date_list'][i] = i + 1

        for member in context['member_list']:
            data_collector = SalaryStatusDataCollector(member, context['month'], mondays)
            data_collector.collect_connects(connect_time_list)
            data_collector.collect_morning(morning_list)
            data_collector.collect_evening(evening_list)
            datas[member.id] = data_collector.get_collected_status_data()
            
 
        context['datas'] = datas
        return context


class SalaryTable(AuthorityCheckView, generic.ListView):
    template_name = 'salary/table.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        member_selector = MemberSelector()
        return member_selector.get_using_driver_list(name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['name'] = self.request.GET.get('name', '')
        context['month'] = self.request.GET.get('month', TODAY[:7])
        salary_selector = SalarySelector()
        context['hourly_wage'] = salary_selector.get_hourly_wage_by_month(context['month'])
        if context['hourly_wage'] == None:
            context['hourly_wage'] = HourlyWage.new_wage(context['month'], self.creator)

        first_date = f"{context['month']}-01"
        # 1일이 월요일이 아닌경우 저번달 마지막주 월요일부터 불러오기
        mondays = get_mondays_from_last_week_of_previous_month(context['month'])
        start_date = mondays[0] if mondays[0][:7] != context['month'] else first_date

        # 불러온 월요일부터 배차 데이터 가져오기
        dispatch_selector = DispatchSelector()
        connect_time_list = dispatch_selector.get_driving_time_list(start_date, last_day_of_month(first_date))

        member_selector = MemberSelector()
        salary_list = member_selector.get_monthly_salary_list(context['month'])
        
        salary_selector = SalarySelector()

        holiday_list = get_holiday_list_from_open_api(context['month'])
        datas = {}
        context['date_list'] = ['' for i in range(31)]

        for i in range(last_day_of_month(first_date)):
            context['date_list'][i] = i + 1

        for member in context['member_list']:
            data_collector = SalaryTableDataCollector(member, context['month'], mondays, context['hourly_wage'], holiday_list)
            data_collector.collect_connects(connect_time_list)
            data_collector.set_salary(salary_list)
            datas[member.id] = data_collector.get_collected_data()
            
        context['datas'] = datas
        return context

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
            logger.warning(f"test {old_hourly_wage}")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        raise BadRequest(hourly_wage_form.errors)

