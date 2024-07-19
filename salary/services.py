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
from humanresource.models import Member, Salary
from humanresource.selectors import MemberSelector
from common.constant import TODAY
from common.formatter import format_number_with_commas
from common.datetime import calculate_time_difference, get_hour_minute_with_colon, get_hour_minute, get_minute_from_colon_time, last_day_of_month, get_weekday_from_date, calculate_date_difference, add_days_to_date
from datetime import datetime, timedelta
import math

class DataCollector:
    def __init__(self, member, month, mondays):
        self.member = member
        self.month = month
        self.connect_time_list = []
        self.last_day = last_day_of_month(f"{month}-01")
        self.mondays = mondays

    def collect_connects(self, connect_time_list):
        self.connect_time_list = list(filter(lambda item: item['driver_id'] == self.member.id, connect_time_list))

    def get_daily_connects(self, date):
        return list(filter(lambda item: item['departure_date'][:10] == date, self.connect_time_list))
    
    def get_work_time(self, daily_connects):
        minutes = 0
        # for connect in daily_connects:
        #     if connect['time']:
        #         minutes += connect['time']
            
        minutes = sum(calculate_time_difference(connect['departure_date'], connect['arrival_date']) for connect in daily_connects)
        return get_hour_minute_with_colon(minutes) if minutes != 0 else '', minutes

    def get_wait_time(self, morning_time, evening_time, work_time):
        if morning_time and evening_time and work_time:
            return get_hour_minute_with_colon(
                get_minute_from_colon_time(evening_time) -
                get_minute_from_colon_time(morning_time) -
                get_minute_from_colon_time(work_time)
            )
        return ''
    
    def is_holiday(self, holiday_data, date_str):
        # 입력된 날짜 문자열을 datetime 객체로 변환
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")
    
        # holiday_list를 돌면서 date와 일치하는지 확인
        return date in holiday_data['locdate_list']

    # 첫번째 월요일이 지난달일 경우 weekly_minute 계산하기
    def get_work_minutes_from_last_month_monday(self):
        last_month_day = calculate_date_difference(self.mondays[0], f'{self.month}-01')
        total_minutes = 0
        for i in range(last_month_day):
            date = add_days_to_date(self.mondays[0], i)
            daily_connects = self.get_daily_connects(date)
            work_time, minutes = self.get_work_time(daily_connects)
            total_minutes += minutes
        return total_minutes

    def check_monday(self, date, mondays_counter):
        if date == self.mondays[mondays_counter]:
            return True
        return False

    def is_weekly_holiday(self, weekly_minute):
        if int(weekly_minute) / 60 >= 15:
            return True
        return False
    
    def get_work_type(self, minutes, weekday, weekly_minute):
        if minutes > 0:
            return '근무'
        elif weekday == '일' and self.is_weekly_holiday(weekly_minute):
            return '주휴'
        else:
            return '비번'
            
            
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


class SalaryStatusDataCollector(DataCollector):
    def __init__(self, member, month, mondays):
        super().__init__(member, month, mondays)
        self.morning_list = []
        self.evening_list = []
    
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

    # def collect_daily_data(self, i):
    #     date = f"{self.month}-{i + 1:02d}"
    #     weekday = get_weekday_from_date(date)
    #     morning_data = list(filter(lambda item: item['date'] == date, self.morning_list))
    #     evening_data = list(filter(lambda item: item['date'] == date, self.evening_list))
    #     daily_connects = list(filter(lambda item: item['departure_date'][:10] == date, self.connect_time_list))

    #     morning_time = self.get_morning_time(date, morning_data)
    #     evening_time = self.get_evening_time(date, evening_data)
    #     work_time, minutes = self.get_work_time(daily_connects)
    #     work_type = self.get_work_type(minutes, weekday, weekly_minute)
    #     wait_time = self.get_wait_time(morning_time, evening_time, work_time)
    #     night_shift_time = self.get_night_shift_time(daily_connects)
        

    #     return morning_time, evening_time, work_time, wait_time, work_type, minutes, night_shift_time

    def get_collected_status_data(self):
        morning_time_list = ['' for i in range(31)]
        evening_time_list = ['' for i in range(31)]
        work_time_list = ['' for i in range(31)]
        wait_time_list = ['' for i in range(31)]
        night_shift_time_list = ['' for i in range(31)]
        work_list = ['' for i in range(31)]
        total_work_minute = 0
        total_night_shift_minute = 0

        weekly_minute = self.get_work_minutes_from_last_month_monday()
        mondays_counter = 1 if self.mondays[0][:7] < self.month else 0
        for i in range(self.last_day):
            date = f"{self.month}-{i + 1:02d}"
            # 월요일이면 weekly_minute 초기화
            if mondays_counter < len(self.mondays) and self.check_monday(date, mondays_counter):
                mondays_counter += 1
                weekly_minute = 0

            # morning_time, evening_time, work_time, wait_time, work_type, minutes, night_shift_time = self.collect_daily_data(i)
            weekday = get_weekday_from_date(date)
            morning_data = list(filter(lambda item: item['date'] == date, self.morning_list))
            evening_data = list(filter(lambda item: item['date'] == date, self.evening_list))
            daily_connects = self.get_daily_connects(date)

            morning_time = self.get_morning_time(date, morning_data)
            evening_time = self.get_evening_time(date, evening_data)
            work_time, minutes = self.get_work_time(daily_connects)
            weekly_minute += minutes
            work_type = self.get_work_type(minutes, weekday, weekly_minute)
            wait_time = self.get_wait_time(morning_time, evening_time, work_time)
            night_shift_time = self.get_night_shift_time(daily_connects)

            
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


class SalaryTableDataCollector(DataCollector):
    def __init__(self, member, month, mondays, hourly_wage_data, holiday_data):
        super().__init__(member, month, mondays)
        self.hourly_wage_data = hourly_wage_data
        self.holiday_data = holiday_data
    
    def set_salary(self, salary_list):
        self.member_salary = next((item for item in salary_list if item['member_id'] == self.member.id), None)

        if not self.member_salary:
            salary = Salary.new_salary(self.member, self.month, self.member)
            self.member_salary = {
                'member_id' : salary.member_id,
                'base' : salary.base,
                'service_allowance' : salary.service_allowance,
                'performance_allowance' : salary.performance_allowance,
                'annual_allowance' : salary.annual_allowance,
                'overtime_allowance' : salary.overtime_allowance,
                'meal' : salary.meal,
                'attendance' : salary.attendance,
                'leave' : salary.leave,
                'order' : salary.order,
                'additional' : salary.additional,
                'deduction' : salary.deduction,
                'assignment' : salary.assignment,
                'regularly_assignment' : salary.regularly_assignment,
                'total' : salary.total,
                'month' : salary.month,
                'payment_date' : salary.payment_date,
                # additional이랑 reduction은 나중에 사용할 때 추가
            }

    def calculate_work_minutes(self, minutes, weekly_minute, within_law_extension_minute, outside_law_extension_minute):
        MAX_WEEKLY_MINUTES = 60 * 30
        MAX_WITHIN_LAW_EXTENSION_MINUTES = 60 * 10

        if weekly_minute < MAX_WEEKLY_MINUTES:
            if weekly_minute + minutes <= MAX_WEEKLY_MINUTES:
                weekly_minute += minutes
            else:
                excess_minutes = weekly_minute + minutes - MAX_WEEKLY_MINUTES
                weekly_minute = MAX_WEEKLY_MINUTES
                within_law_extension_minute += excess_minutes
        else:
            within_law_extension_minute += minutes

        if within_law_extension_minute > MAX_WITHIN_LAW_EXTENSION_MINUTES:
            excess_minutes = within_law_extension_minute - MAX_WITHIN_LAW_EXTENSION_MINUTES
            within_law_extension_minute = MAX_WITHIN_LAW_EXTENSION_MINUTES
            outside_law_extension_minute += excess_minutes

        return weekly_minute, within_law_extension_minute, outside_law_extension_minute


    def get_collected_data(self):
        work_time_list = ['' for i in range(31)]
        night_shift_time_list = ['' for i in range(31)]
        work_list = ['' for i in range(31)]
        
        hourly_wage = 0
        wage = 0
        weekly_extension_wage = 0
        
        total_work_minute = 0
        total_night_shift_minute = 0
        total_weekly_minute = 0 # 주간 근로시간(최대30시간) 한달치
        total_within_law_extension_minute = 0
        total_outside_law_extension_minute = 0


        last_month_weekly_minute = self.get_work_minutes_from_last_month_monday()
        mondays_counter = 1 if self.mondays[0][:7] < self.month else 0
        weekly_minute = last_month_weekly_minute
        within_law_extension_minute = 0
        outside_law_extension_minute = 0
        
        
        holiday_hour = 0
        additional_holiday_hour = 0
        
        for i in range(self.last_day):
            date = f"{self.month}-{i + 1:02d}"

            # 월요일이면 weekly_minute 초기화
            if mondays_counter < len(self.mondays) and self.check_monday(date, mondays_counter):
                mondays_counter += 1

                # 저번달 시간 빼주기
                total_weekly_minute += weekly_minute
                if i < 7:
                    print("i", i)
                    only_weekly_minute = weekly_minute - last_month_weekly_minute
                else:
                    only_weekly_minute = weekly_minute
                # 주 근무시간으로 시급 결정해서 계산하기 
                hourly_wage = int(self.hourly_wage_data.get_wage(weekly_minute))
                wage += math.ceil(round(only_weekly_minute / 60, 1) * hourly_wage) # 반올림은?
                print(only_weekly_minute, wage, hourly_wage)
                weekly_extension_wage += math.ceil(round((within_law_extension_minute + outside_law_extension_minute) / 60, 1) * hourly_wage) # 주 연장 기본임금
                weekly_minute = 0
                within_law_extension_minute = 0
                outside_law_extension_minute = 0

            weekday = get_weekday_from_date(date)
            daily_connects = self.get_daily_connects(date)
            work_time, minutes = self.get_work_time(daily_connects)
            # weekly_minute += minutes
            weekly_minute, within_law_extension_minute, outside_law_extension_minute = self.calculate_work_minutes(minutes, weekly_minute, within_law_extension_minute, outside_law_extension_minute)
            total_within_law_extension_minute += within_law_extension_minute
            total_outside_law_extension_minute += outside_law_extension_minute

            work_type = self.get_work_type(minutes, weekday, weekly_minute)
            night_shift_time = self.get_night_shift_time(daily_connects)

            if self.is_holiday(self.holiday_data, date) or work_type == '주휴':
                if minutes / 60 <= 8:
                    holiday_hour += round(minutes / 60, 1)
                    additional_holiday_hour += 0
                else:
                    holiday_hour += 8
                    additional_holiday_hour += round((minutes - 60 * 8) / 60, 1)

            work_time_list[i] = work_time
            work_list[i] = work_type
            night_shift_time_list[i] = get_hour_minute_with_colon(night_shift_time) if night_shift_time > 0 else ''
            total_work_minute += minutes
            total_night_shift_minute += night_shift_time


        # 주 근무시간으로 시급 결정해서 계산하기 
        total_weekly_minute += weekly_minute
        hourly_wage = int(self.hourly_wage_data.get_wage(weekly_minute))
        wage += math.ceil(round(weekly_minute / 60, 1) * hourly_wage) # 반올림은?
        weekly_extension_wage += math.ceil(round((within_law_extension_minute + outside_law_extension_minute) / 60, 1) * hourly_wage) # 주 연장 기본임금


        total_work_hour = round(total_work_minute / 60, 1)
        # hourly_wage = int(self.hourly_wage_data.get_wage(total_work_minute))
        weekly_holiday_count = work_list.count('주휴')
        # 5월이면 5월1일 1개 추가
        legal_holiday_count = self.holiday_data['count'] + 1 if self.month[5:7] == '05' else weekly_holiday_count + self.holiday_data['count']

        # 소수점 다 반올림
        # 통상급여
        # wage = math.ceil(round((total_weekly_minute - last_month_weekly_minute) / 60, 1) * hourly_wage) # 반올림은?
        # performance_allowance = int(self.member_salary['performance_allowance']) # 성과급
        performance_allowance = 0 # 일단 0으로 고정
        service_allowance = int(self.member_salary['service_allowance']) # 근속수당
        ordinary_salary = wage + service_allowance + performance_allowance
        ordinary_hourly_wage = math.ceil(ordinary_salary / round((total_weekly_minute - last_month_weekly_minute) / 60, 1)) if round((total_weekly_minute - last_month_weekly_minute) / 60, 1) != 0 else 0 # 통상시급 반올림은?
        print("test", total_weekly_minute, round((total_weekly_minute - last_month_weekly_minute) / 60, 1))
        # 법정수당
        weekly_holiday_allowance = ordinary_hourly_wage * 6 * weekly_holiday_count # 주휴수당
        legal_holiday_allowance = ordinary_hourly_wage * 6 * legal_holiday_count # 법정휴일
        # weekly_extension_wage = math.ceil(round((total_within_law_extension_minute + total_outside_law_extension_minute) / 60, 1) * hourly_wage) # 주 연장 기본임금
        weekly_extension_additional_wage = math.ceil(round(total_outside_law_extension_minute / 60, 1) * ordinary_hourly_wage * 0.5) # 주 연장 가산임금
        night_shift_wage = math.ceil(round(total_night_shift_minute / 60, 1) * ordinary_hourly_wage * 0.5) # 야간근로 가산임금
        holiday_work_wage = math.ceil(holiday_hour * ordinary_hourly_wage * 0.5) # 휴일 기본임금
        additional_holiday_work_wage = math.ceil(additional_holiday_hour * ordinary_hourly_wage * 0.5) # 휴일 가산임금
        annual_allowance = int(self.member_salary['annual_allowance']) # 연차수당
        meal = int(self.member_salary['meal']) # 식대 > 만근수당
        statutory_allowance = math.ceil(weekly_holiday_allowance + weekly_extension_wage + weekly_extension_additional_wage + night_shift_wage + holiday_work_wage + additional_holiday_work_wage + annual_allowance + meal)

        # additional_salary = int(self.member_salary['additional_salary__price'])
        # deduction_salary = int(self.member_salary['deduction_salary__price'])
        return {
            'work_time_list': work_time_list,
            'night_shift_time_list': night_shift_time_list,
            'total_night_shift_minute': get_hour_minute(total_night_shift_minute),
            'work_list': work_list,
            'work_count': work_list.count('근무'),
            'off_duty_count': work_list.count('비번'),
            'weekly_holiday_count': weekly_holiday_count,
            'entering_date': self.member.entering_date,

            'total_work_minute': total_work_minute,
            'total_work_hour_minute': get_hour_minute(total_work_minute), # 근무시간
            'hourly_wage': format_number_with_commas(hourly_wage), # 기본시급
            'ordinary_hourly_wage': format_number_with_commas(ordinary_hourly_wage), # 통상시급
            
            # 통상급여
            'wage': format_number_with_commas(wage),
            'performance_allowance': format_number_with_commas(performance_allowance), # 성과급
            'meal': format_number_with_commas(meal), # 식대
            'service_allowance': format_number_with_commas(service_allowance), # 근속수당
            'ordinary_salary': format_number_with_commas(ordinary_salary),
            
            # 법정수당
            'weekly_holiday_allowance': format_number_with_commas(weekly_holiday_allowance),
            'legal_holiday_allowance': format_number_with_commas(legal_holiday_allowance),
            'weekly_extension_wage': format_number_with_commas(weekly_extension_wage),
            'weekly_extension_additional_wage': format_number_with_commas(weekly_extension_additional_wage),
            'night_shift_wage': format_number_with_commas(night_shift_wage),
            'holiday_work_wage': format_number_with_commas(holiday_work_wage),
            'additional_holiday_work_wage': format_number_with_commas(additional_holiday_work_wage),
            'annual_allowance': format_number_with_commas(annual_allowance), # 연차수당
            'statutory_allowance': format_number_with_commas(statutory_allowance),
            'sum_ordinary_salary_and_statutory_allowance': format_number_with_commas(ordinary_salary + statutory_allowance),

        }


class SalaryTableDataCollector2(SalaryTableDataCollector):
    def get_work_time(self, daily_connects):
        minutes = 0
        # for connect in daily_connects:
        #     if connect['time']:
        #         minutes += connect['time']
            
        minutes = sum(int(connect['route_time']) if connect['route_time'] else calculate_time_difference(connect['departure_date'], connect['arrival_date']) for connect in daily_connects)
        return get_hour_minute_with_colon(minutes) if minutes != 0 else '', minutes