from config.custom_logging import logger
from django.forms.models import model_to_dict
from dispatch.models import DispatchRegularlyData, MorningChecklist, EveningChecklist, DispatchRegularly
from dispatch.selectors import DispatchSelector
from humanresource.models import Member, Salary
from humanresource.selectors import MemberSelector
from common.constant import TODAY
from common.formatter import format_number_with_commas, remove_comma_from_number
from common.datetime import calculate_time_difference, get_hour_minute_with_colon, get_hour_minute, get_minute_from_colon_time, last_day_of_month, get_weekday_from_date, calculate_date_difference, add_days_to_date, last_date_of_month, get_next_sunday_after_last_day, calculate_time_with_minutes
from datetime import datetime, timedelta
import math
from .selectors import SalarySelector
from .models import HourlyWage


class DataCollector:
    def __init__(self, member, month, mondays, connect_time_list, holiday_data, date_list):
        self.member = member
        self.month = month
        self.mondays = mondays
        self.morning_list = []
        self.evening_list = []
        self.date_list = date_list
        
        self.set_member_salary()
        self.hourly_wage_data = self.set_hourly_wage_data()
        self.connect_time_list = list(filter(lambda item: item['driver_id'] == self.member.id, connect_time_list))
        self.holiday_data = holiday_data
        # 기본은 1달
        self.set_duration(1, last_day_of_month(f'{self.month}-01'))

    def collect_morning(self, morning_list):
        self.morning_list = list(filter(lambda item: item['member'] == self.member.id, morning_list))

    def collect_evening(self, evening_list):
        self.evening_list = list(filter(lambda item: item['member'] == self.member.id, evening_list))

    def set_duration(self, start_day, last_day):
        self.start_day = start_day
        self.last_day = last_day
    
    def set_hourly_wage_data(self):
        salary_selector = SalarySelector()
        hourly_wage = salary_selector.get_hourly_wage_by_month(self.month)
        if hourly_wage == None:
            hourly_wage = HourlyWage.new_wage(self.month)
        return hourly_wage
        
    def set_member_salary(self):
        member_selector = MemberSelector()
        salary_list = member_selector.get_monthly_salary_list(self.month)
        self.member_salary = next((item for item in salary_list if item['member_id'] == self.member.id), None)

        if not self.member_salary:
            salary = Salary.new_salary(self.member, self.month, self.member)
            self.member_salary = model_to_dict(salary)

    def round_up_to_nearest_ten(self, number):
        """
        주어진 숫자를 가장 가까운 10의 배수로 올립니다.
        """
        return ((number + 9) // 10) * 10

    
    def get_daily_connects(self, date):
        return list(filter(lambda item: item['departure_date'][:10] == date, self.connect_time_list))
    
    # def get_work_time(self, daily_connects):
    #     minutes = 0
    #     # for connect in daily_connects:
    #     #     if connect['time']:
    #     #         minutes += connect['time']
            
    #     minutes = sum(self.round_up_to_nearest_ten(calculate_time_difference(connect['departure_date'], connect['arrival_date'])) for connect in daily_connects)
    #     return get_hour_minute_with_colon(minutes) if minutes != 0 else '', minutes

    # 보파보
    def get_work_time(self, date):
        connects_list = self.get_connects_time_list(date)
        minutes = 0

        for connect in connects_list:
            minutes += connect['total_time']

            
        # minutes = sum(self.round_up_to_nearest_ten(int(connect['route_time'])) if connect['route_time'] else self.round_up_to_nearest_ten(calculate_time_difference(connect['departure_date'], connect['arrival_date'])) for connect in daily_connects)
        return minutes

    # 중복 시간 제거
    def calculate_total_drive_time(self, data):
        total_time = 0
        last_end_time = None

        for connect in data:
            departure = datetime.strptime(connect['departure_date'], "%Y-%m-%d %H:%M")
            arrival = datetime.strptime(connect['arrival_date'], "%Y-%m-%d %H:%M")

            if last_end_time and departure < last_end_time:
                overlap = (last_end_time - departure).total_seconds() / 60
                trip_time = (arrival - departure).total_seconds() / 60 - overlap
            else:
                trip_time = (arrival - departure).total_seconds() / 60

            if trip_time > 0:
                total_time += trip_time

            last_end_time = max(last_end_time, arrival) if last_end_time else arrival

        return total_time

    
    
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
            minutes = self.get_work_time(date)
            total_minutes += minutes
        return total_minutes
    
     # 마지막 일요일이 다음달일 경우 weekly_minute 계산하기
    def get_work_minutes_from_next_month_sunday(self):
        last_date = last_date_of_month(f'{self.month}-01')
        calculated_day = calculate_date_difference(last_date, get_next_sunday_after_last_day(self.month))
        total_minutes = 0
        for i in range(calculated_day):
            date = add_days_to_date(last_date, i + 1)
            minutes = self.get_work_time(date)
            total_minutes += minutes
        return total_minutes

    def check_monday(self, date, mondays_counter):
        if date == self.mondays[mondays_counter]:
            return True
        return False

    def is_weekly_holiday(self, weekly_minute):
        # 5일 이상 근무하면 주휴발생
        # if int(weekly_minute) >= 15 * 60:
        #     return True
        # return False
        return True
    
    def get_work_type(self, minutes, weekday, weekly_minute):
        if weekday == '일' and self.is_weekly_holiday(weekly_minute):
            return '주휴'
        if minutes > 0:
            return '근무'
        else:
            return '비번'
    
    def get_morning_time(self, date, morning_data):
        if len(morning_data) > 1:
            logger.warning(f"아침 점호는 1일 당 1개만 있어야 됨 {date} {self.member.name}")
        return morning_data[0]['arrival_time'] if morning_data else ''

    def get_evening_time(self, date, evening_data):
        if len(evening_data) > 1:
            logger.warning(f"저녁 점호는 1일 당 1개만 있어야 됨 {date} {self.member.name}")
        return datetime.strftime(evening_data[0]['updated_at'], '%Y-%m-%d %H:%M')[11:] if evening_data else ''

    def get_wait_time(self, morning_time, evening_time, work_time):
        if morning_time and evening_time and work_time:
            return get_hour_minute_with_colon(
                get_minute_from_colon_time(evening_time) -
                get_minute_from_colon_time(morning_time) -
                get_minute_from_colon_time(work_time)
            )
        return ''
            
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
    
    def get_night_shift_time(self, date):
        minutes = 0
        daily_connects = self.get_connects_time_list(date)
        for connect in daily_connects:
            # 지금은 일반배차 제외하고 야근시간 계산
            if connect['work_type'] != '일반' and connect['start_date'] and connect['end_date']:
                # minutes += self.round_up_to_nearest_ten(self.calculate_night_shift_minutes(connect['start_date'], connect['end_date']))
                minutes += self.calculate_night_shift_minutes(connect['start_date'], connect['end_date'])
            
        return minutes

    def calculate_work_minutes(self, minutes, weekly_minute, within_law_extension_minute, outside_law_extension_minute, holiday_check):
        # holiday_check로 휴일이면 연장시간에 더하기 안 함
        MAX_WEEKLY_MINUTES = 60 * 30
        MAX_WITHIN_LAW_EXTENSION_MINUTES = 60 * 10

        if weekly_minute < MAX_WEEKLY_MINUTES:
            if weekly_minute + minutes <= MAX_WEEKLY_MINUTES:
                weekly_minute += minutes
            else:
                excess_minutes = weekly_minute + minutes - MAX_WEEKLY_MINUTES
                weekly_minute = MAX_WEEKLY_MINUTES
                if not holiday_check:
                    within_law_extension_minute += excess_minutes
        else:
            if not holiday_check:
                within_law_extension_minute += minutes

        if within_law_extension_minute > MAX_WITHIN_LAW_EXTENSION_MINUTES:
            excess_minutes = within_law_extension_minute - MAX_WITHIN_LAW_EXTENSION_MINUTES
            within_law_extension_minute = MAX_WITHIN_LAW_EXTENSION_MINUTES
            outside_law_extension_minute += excess_minutes

        return weekly_minute, within_law_extension_minute, outside_law_extension_minute

    def return_zero_data(self):
        return {
            'entering_date': self.member.entering_date,

            'total_work_minute': '0',
            'total_work_hour_minute': '0', # 근무시간
            'hourly_wage1': '0',
            'hourly_wage2': '0',
            
            'ordinary_hourly_wage': '0',
            
            # 통상급여
            'wage': '0',
            'performance_allowance': '0',
            'meal': '0',
            'service_allowance': '0',
            'ordinary_salary': '0',
            
            # 법정수당
            'weekly_holiday_allowance': '0',
            'legal_holiday_allowance': '0',
            # 'weekly_extension_wage': '0',
            'weekly_within_law_extension_wage' : '0',
            'weekly_outside_law_extension_wage' : '0',
            'weekly_extension_additional_wage': '0',
            'night_shift_wage': '0',
            'holiday_work_wage': '0',
            'additional_holiday_work_wage_half': '0',
            'additional_holiday_work_wage': '0',
            'annual_allowance': '0',
            'statutory_allowance': '0',
            'sum_ordinary_salary_and_statutory_allowance': '0',

            'additional': '0',
            'deduction': '0',

            'new_annual_allowance': '0',
            'team_leader_allowance_roll_call': '0',
            'team_leader_allowance_vehicle_management': '0',
            'team_leader_allowance_task_management': '0',
            'full_attendance_allowance': '0',
            'diligence_allowance': '0',
            'accident_free_allowance': '0',

            'welfare_meal_allowance': '0',
            'welfare_fuel_allowance': '0',
            'total': '0',

        }
    
    def get_connects_time_list(self, date):
        daily_connects = self.get_daily_connects(date)
        connect_list = []
        i = 0
        for connect in daily_connects:
            route_time = int(connect['route_time']) if connect['route_time'] else 0
            connect_time_list = ['' for i in range(6)]
            if connect['work_type'] == '일반':
                connect_list.append({
                    'total_time': get_minute_from_colon_time(connect['arrival_date'][11:]) - get_minute_from_colon_time(connect['departure_date'][11:]),
                    'work_type': '일반',
                    'route': connect['order_id__route'],
                    'connect_time_list': connect_time_list,
                    'start_date':  '',
                    'end_date': ''
                })
                i += 1
                continue
            time_list = connect['stations_list']

            if not time_list:
                connect_list.append({
                    'total_time': 0,
                    'work_type': connect['work_type'],
                    'route': connect['route'],
                    'connect_time_list': connect_time_list,
                    'start_date':  '',
                    'end_date': ''
                })
                i += 1
                continue

            
            length = len(time_list)

            connect_time_list[0] = self.get_first_time_list(i, daily_connects)
            connect_time_list[1], connect_time_list[2] = self.get_pre_ready_time_and_departure_time(connect['work_type'], time_list)

            connect_time_list[3] = time_list[length - 2]
            connect_time_list[4] = time_list[length - 1]
            connect_time_list[5] = calculate_time_with_minutes(time_list[length - 1], 5)

            if self.is_time_difference_under_90(i, daily_connects):
                connect_time_list[4] = time_list[length - 2]
                connect_time_list[5] = time_list[length - 2]
            
            # 운행시간이 자정을 넘겼을 떄 운행시간 계산
            if get_minute_from_colon_time(connect_time_list[5]) >= get_minute_from_colon_time(connect_time_list[0]):
                route_time = get_minute_from_colon_time(connect_time_list[5]) - get_minute_from_colon_time(connect_time_list[0])
            else:
                route_time = 24 * 60 + get_minute_from_colon_time(connect_time_list[5]) - get_minute_from_colon_time(connect_time_list[0])

            connect_list.append({
                'total_time': route_time,
                'work_type': connect['work_type'],
                'route': connect['route'],
                'connect_time_list': connect_time_list,
                'start_date':  f"{date} {connect_time_list[0]}",
                'end_date': f"{date} {connect_time_list[5]}",
            })
            i += 1
        return connect_list

    def get_first_time_list(self, i, daily_connects):
        time_list = daily_connects[i]['stations_list']
        if i <= 0 or daily_connects[i - 1]['work_type'] == '일반' or self.is3M(daily_connects, i):
            return time_list[0]

        prev_time_list = daily_connects[i - 1]['stations_list']
        if not prev_time_list:
            return time_list[0]
        prev_length = len(prev_time_list)
        prev_arrival_time = prev_time_list[prev_length - 2]
        # 현재 사전 준비시간 - 이전 도착시간 < 90 : 현재 차고지도착 = 이전 도착시간
        pre_ready_time, __ = self.get_pre_ready_time_and_departure_time(daily_connects[i]['work_type'], time_list)
        time_difference = get_minute_from_colon_time(pre_ready_time) - get_minute_from_colon_time(prev_arrival_time)
        if time_difference < 90:
            return prev_arrival_time
        else:
            return time_list[0]

    def is_time_difference_under_90(self, i, daily_connects) -> bool:
        time_list = daily_connects[i]['stations_list']
        length = len(time_list)
        if i >= len(daily_connects) - 1 or daily_connects[i + 1]['work_type'] == '일반' or self.is3M(daily_connects, i + 1):
            return False
        
        next_time_list = daily_connects[i + 1]['stations_list']
        if not next_time_list:
            return False
        # 다음 사전 준비시간 - 현재 도착시간 < 90 : 현재 차량입고, 뒷정리완료 = 현재 도착시간
        arrival_time = time_list[length - 2]
        next_pre_ready_time, __ = self.get_pre_ready_time_and_departure_time(daily_connects[i + 1]['work_type'], next_time_list)
        time_difference = get_minute_from_colon_time(next_pre_ready_time) - get_minute_from_colon_time(arrival_time)
        return time_difference < 90

    def get_pre_ready_time_and_departure_time(self, work_type, time_list):
        time = ['', '']
        if work_type == '출근':
            time[0] = time_list[1]
            time[1] = time_list[2]
        else:
            time[0] = calculate_time_with_minutes(time_list[1], -10)
            time[1] = time_list[1]
        return time[0], time[1]

    def is3M(self, daily_connects, i) -> bool:
        try:
            return "쓰리엠" in daily_connects[i]['group'] or \
                    (i + 1 < len(daily_connects) and "쓰리엠" in daily_connects[i + 1]['group']) or \
                    (i > 0 and "쓰리엠" in daily_connects[i - 1]['group'])
        except Exception as e:
            return False


    # 근무현황
    def get_calculate_times(self):
        morning_time_list = ['' for i in range(len(self.date_list))]
        evening_time_list = ['' for i in range(len(self.date_list))]
        wait_time_list = ['' for i in range(len(self.date_list))]
        work_time_list = ['' for i in range(len(self.date_list))]
        night_shift_time_list = ['' for i in range(len(self.date_list))]
        work_list = ['' for i in range(len(self.date_list))]
        holiday_time_list = ['' for i in range(len(self.date_list))]
        additional_holiday_time_list = ['' for i in range(len(self.date_list))]
        
        total_work_minute = 0
        total_night_shift_minute = 0
        total_weekly_minute = 0 # 주간 근로시간(최대30시간) 한달치
        total_within_law_extension_minute = 0
        total_outside_law_extension_minute = 0


        last_month_weekly_minute = self.get_work_minutes_from_last_month_monday() if self.mondays else 0 
        mondays_counter = 1 if self.mondays and self.mondays[0][:7] < self.month else 0
        weekly_minute = last_month_weekly_minute
        within_law_extension_minute = 0
        outside_law_extension_minute = 0
        
        
        holiday_minute = 0
        additional_holiday_minute = 0
        weekly_work_count = 0
        
        for i in range(len(self.date_list)):
            date = self.date_list[i]

            # 월요일이면 weekly_minute 초기화
            if mondays_counter < len(self.mondays) and self.check_monday(date, mondays_counter):
                mondays_counter += 1

                # 저번달 시간 빼주기
                if i < 7:
                    total_weekly_minute += weekly_minute - last_month_weekly_minute
                else:
                    total_weekly_minute += weekly_minute
                
                total_within_law_extension_minute += within_law_extension_minute
                total_outside_law_extension_minute += outside_law_extension_minute

                weekly_minute = 0
                within_law_extension_minute = 0
                outside_law_extension_minute = 0
                weekly_work_count = 0

            weekday = get_weekday_from_date(date)
            daily_connects = self.get_daily_connects(date)
            minutes = self.get_work_time(date)
            work_time = get_hour_minute_with_colon(minutes) if minutes != 0 else ''

            work_type = self.get_work_type(minutes, weekday, weekly_minute)
            holiday_check = self.is_holiday(self.holiday_data, date) or work_type == '주휴'
            # weekly_minute += minutes
            weekly_minute, within_law_extension_minute, outside_law_extension_minute = self.calculate_work_minutes(minutes, weekly_minute, within_law_extension_minute, outside_law_extension_minute, holiday_check)
            # total_within_law_extension_minute += within_law_extension_minute
            # total_outside_law_extension_minute += outside_law_extension_minute

            weekly_work_count += 1 if daily_connects else  0
            night_shift_time = self.get_night_shift_time(date)

            
            if holiday_check:
                if minutes / 60 <= 8:
                    holiday_minute += minutes
                    additional_holiday_minute += 0
                    holiday_time_list[i] = get_hour_minute_with_colon(minutes) if minutes > 0 else ''
                    additional_holiday_time_list[i] = ''
                else:
                    holiday_minute += 60 * 8
                    additional_holiday_minute += minutes - 60 * 8
                    holiday_time_list[i] = get_hour_minute_with_colon(60 * 8)
                    additional_holiday_time_list[i] = get_hour_minute_with_colon(minutes - 60 * 8)
            else:
                holiday_time_list[i] = ''
                additional_holiday_time_list[i] = ''

            work_time_list[i] = work_time
            work_list[i] = work_type
            night_shift_time_list[i] = get_hour_minute_with_colon(night_shift_time) if night_shift_time > 0 else ''
            


            total_work_minute += minutes
            total_night_shift_minute += night_shift_time

            if self.morning_list and self.evening_list:
                morning_data = list(filter(lambda item: item['date'] == date, self.morning_list))
                evening_data = list(filter(lambda item: item['date'] == date, self.evening_list))
                morning_time = self.get_morning_time(date, morning_data)
                evening_time = self.get_evening_time(date, evening_data)

                wait_time_list[i] = self.get_wait_time(morning_time, evening_time, work_time)
                morning_time_list[i] = morning_time
                evening_time_list[i] = evening_time


        total_weekly_minute += weekly_minute
        total_within_law_extension_minute += within_law_extension_minute
        total_outside_law_extension_minute += outside_law_extension_minute
        
        weekly_holiday_count = work_list.count('주휴')
        # 5월이면 5월1일 1개 추가
        legal_holiday_count = self.holiday_data['count'] + 1 if self.month[5:7] == '05' else self.holiday_data['count']

        return {
            # 근무현황
            'morning_time_list': morning_time_list,
            'evening_time_list': evening_time_list,
            'wait_time_list': wait_time_list,
            'work_count': work_list.count('근무'),
            'off_duty_count': work_list.count('비번'),
            'total_count': len(work_list) - work_list.count(''),
            'total_work_hour_minute': get_hour_minute(total_work_minute), # 근무시간
            'holiday_time_list': holiday_time_list,
            'additional_holiday_time_list': additional_holiday_time_list,
            

            # 공통 + 임금테이블
            'work_time_list': work_time_list,
            'night_shift_time_list': night_shift_time_list,
            'work_list': work_list,
            'total_work_minute': total_work_minute,
            'total_night_shift_minute': total_night_shift_minute,
            'total_night_shift_hour_minute': get_hour_minute(total_night_shift_minute) if total_night_shift_minute != 0 else "",
            'total_weekly_minute': total_weekly_minute,
            'total_weekly_hour_minute': get_hour_minute(total_weekly_minute),
            'total_within_law_extension_minute': total_within_law_extension_minute,
            'total_within_law_extension_hour_minute': get_hour_minute(total_within_law_extension_minute) if total_within_law_extension_minute != 0 else "",
            'total_outside_law_extension_minute': total_outside_law_extension_minute,
            'total_outside_law_extension_hour_minute': get_hour_minute(total_outside_law_extension_minute) if total_outside_law_extension_minute != 0 else "",
            'weekly_holiday_count': weekly_holiday_count,
            'legal_holiday_count': legal_holiday_count,

            'holiday_minute': holiday_minute,
            'additional_holiday_minute': additional_holiday_minute,
            'holiday_hour_minute': get_hour_minute(holiday_minute) if holiday_minute != 0 else "",
            'additional_holiday_hour_minute': get_hour_minute(additional_holiday_minute) if additional_holiday_minute != 0 else "",
        }
    
    def set_wage(self, total_weekly_minute, hourly_wage1):
        return math.ceil(total_weekly_minute / 60 * hourly_wage1) # 반올림은?
    
    def get_calculate_wages(self, times_data):
        hourly_wage1 = int(self.hourly_wage_data.wage1)
        hourly_wage2 = int(self.hourly_wage_data.wage2)

        total_weekly_minute = times_data['total_weekly_minute']
        weekly_holiday_count = times_data['work_list'].count('주휴')
        legal_holiday_count = self.holiday_data['count'] + 1 if self.month[5:7] == '05' else self.holiday_data['count']


        # 근무시간 0 이면 모두 0으로 반환
        if total_weekly_minute == 0:
            return self.return_zero_data()
        
        # 통상급여
        # wage = math.ceil(hourly_wage1 * 1470 / 12)
        # wage = math.ceil(total_weekly_minute / 60 * hourly_wage1)
        wage = self.set_wage(total_weekly_minute, hourly_wage1)
        performance_allowance = int(self.member_salary['performance_allowance']) # 성과급
        service_allowance = int(self.member_salary['service_allowance']) # 근속수당
        ordinary_salary = wage + service_allowance + performance_allowance
        #ordinary_hourly_wage = math.ceil(hourly_wage1 + (performance_allowance * 12 / 2349) + (service_allowance * 12 / 1470))
        ordinary_hourly_wage = math.ceil(hourly_wage1 + (service_allowance * 12 / 1470))

        # 법정수당
        weekly_holiday_allowance = ordinary_hourly_wage * 6 * weekly_holiday_count # 주휴수당
        legal_holiday_allowance = ordinary_hourly_wage * 6 * legal_holiday_count # 법정휴일
        weekly_within_law_extension_wage = math.ceil(times_data['total_within_law_extension_minute'] / 60 * hourly_wage1) # 주 연장 법내 기본임금
        weekly_within_law_extension_wage = math.ceil(weekly_within_law_extension_wage + weekly_within_law_extension_wage * 0.2)
        weekly_outside_law_extension_wage = math.ceil(times_data['total_outside_law_extension_minute'] / 60 * hourly_wage1) # 주 연장 법외 기본임금
        weekly_extension_additional_wage = math.ceil(times_data['total_outside_law_extension_minute'] / 60 * ordinary_hourly_wage * 0.5) # 주 연장 가산임금
        night_shift_wage = math.ceil(times_data['total_night_shift_minute'] / 60 * ordinary_hourly_wage * 0.5) # 야간근로 가산임금
        
        holiday_work_wage = math.ceil((times_data['holiday_minute'] / 60 + times_data['additional_holiday_minute'] / 60) * hourly_wage1) # 휴일 기본임금
        additional_holiday_work_wage_half = math.ceil(times_data['holiday_minute'] / 60 * ordinary_hourly_wage * 0.5) #휴일 50%가산임금
        additional_holiday_work_wage = math.ceil(times_data['additional_holiday_minute'] / 60 * ordinary_hourly_wage) #휴일 100%가산임금
        annual_allowance = int(self.member_salary['annual_allowance']) # 연차수당
        meal = int(self.member_salary['meal']) # 식대 > 만근수당
        statutory_allowance = math.ceil(weekly_holiday_allowance + legal_holiday_allowance + weekly_within_law_extension_wage + weekly_outside_law_extension_wage + weekly_extension_additional_wage + night_shift_wage + holiday_work_wage + additional_holiday_work_wage + additional_holiday_work_wage_half + annual_allowance + meal)

        # additional_salary = int(self.member_salary['additional_salary__price'])
        # deduction_salary = int(self.member_salary['deduction_salary__price'])
        return {
            'entering_date': self.member.entering_date,
            'total_work_minute': times_data['total_work_minute'],
            'total_work_hour_minute': get_hour_minute(times_data['total_work_minute']), # 근무시간
            'hourly_wage1': format_number_with_commas(int(self.hourly_wage_data.wage1)), # 기본시급
            'hourly_wage2': format_number_with_commas(int(self.hourly_wage_data.wage2)), # 기본시급2
            
            'ordinary_hourly_wage': format_number_with_commas(ordinary_hourly_wage), # 통상시급
            
            # 산정시간
            'total_weekly_hour_minute': times_data['total_weekly_hour_minute'],
            'total_within_law_extension_hour_minute': times_data['total_within_law_extension_hour_minute'],
            'total_outside_law_extension_hour_minute': times_data['total_outside_law_extension_hour_minute'],
            'total_night_shift_hour_minute': times_data['total_night_shift_hour_minute'],
            'holiday_hour_minute': times_data['holiday_hour_minute'],
            'additional_holiday_hour_minute': times_data['additional_holiday_hour_minute'],

            # 통상급여
            'wage': format_number_with_commas(wage),
            'performance_allowance': format_number_with_commas(performance_allowance), # 성과급
            'meal': format_number_with_commas(meal), # 식대
            'service_allowance': format_number_with_commas(service_allowance), # 근속수당
            'ordinary_salary': format_number_with_commas(ordinary_salary),
            
            # 법정수당
            'weekly_holiday_allowance': format_number_with_commas(weekly_holiday_allowance),
            'legal_holiday_allowance': format_number_with_commas(legal_holiday_allowance),
            # 'weekly_extension_wage': format_number_with_commas(weekly_extension_wage),
            'weekly_within_law_extension_wage' : format_number_with_commas(weekly_within_law_extension_wage),
            'weekly_outside_law_extension_wage' : format_number_with_commas(weekly_outside_law_extension_wage),
            'weekly_extension_additional_wage': format_number_with_commas(weekly_extension_additional_wage),
            'night_shift_wage': format_number_with_commas(night_shift_wage),
            'holiday_work_wage': format_number_with_commas(holiday_work_wage),
            'additional_holiday_work_wage_half': format_number_with_commas(additional_holiday_work_wage_half),
            'additional_holiday_work_wage': format_number_with_commas(additional_holiday_work_wage),
            'annual_allowance': format_number_with_commas(annual_allowance), # 연차수당
            'statutory_allowance': format_number_with_commas(statutory_allowance),
            'sum_ordinary_salary_and_statutory_allowance': format_number_with_commas(ordinary_salary + statutory_allowance),

            'additional': format_number_with_commas(int(self.member_salary['additional'])),
            'deduction': format_number_with_commas(int(self.member_salary['deduction'])),
        }

class SalaryStatusDataCollector(DataCollector):
    def get_collected_status_data(self):
        time_data = self.get_calculate_times()
        
        return time_data

    

class SalaryTableDataCollector(DataCollector):
    def get_collected_data(self):
        times_data = self.get_calculate_times()
        return self.get_calculate_wages(times_data)


class SalaryTableDataCollector2(SalaryTableDataCollector):
    def set_wage(self, total_weekly_minute, hourly_wage1):
        return math.ceil(hourly_wage1 * 1470 / 12)

class SalaryTableDataCollector3(SalaryTableDataCollector):
    def get_calculate_wages(self, times_data):
        datas = super().get_calculate_wages(times_data)
        if datas['total_work_hour_minute'] == "0":
            return datas
        #통상급여
        datas['ordinary_salary'] = format_number_with_commas(remove_comma_from_number(datas['ordinary_salary']) - int(self.member_salary['performance_allowance']))

        datas['new_annual_allowance'] = format_number_with_commas(int(self.member_salary['new_annual_allowance']))
        datas['team_leader_allowance_roll_call'] = format_number_with_commas(int(self.member_salary['team_leader_allowance_roll_call']))
        datas['team_leader_allowance_vehicle_management'] = format_number_with_commas(int(self.member_salary['team_leader_allowance_vehicle_management']))
        datas['team_leader_allowance_task_management'] = format_number_with_commas(int(self.member_salary['team_leader_allowance_task_management']))
        datas['full_attendance_allowance'] = format_number_with_commas(int(self.member_salary['full_attendance_allowance']))
        datas['diligence_allowance'] = format_number_with_commas(int(self.member_salary['diligence_allowance']))
        datas['accident_free_allowance'] = format_number_with_commas(int(self.member_salary['accident_free_allowance']))
        #datas['annual_allowance'] = int(self.member_salary['annual_allowance'])
        
        #법정수당 합계
        datas['statutory_allowance'] = format_number_with_commas(
            remove_comma_from_number(datas['statutory_allowance'])
            - remove_comma_from_number(datas['meal'])
            - remove_comma_from_number(datas['annual_allowance'])
            + remove_comma_from_number(datas['new_annual_allowance'])
            + remove_comma_from_number(datas['team_leader_allowance_roll_call'])
            + remove_comma_from_number(datas['team_leader_allowance_vehicle_management'])
            + remove_comma_from_number(datas['team_leader_allowance_task_management'])
            + remove_comma_from_number(datas['full_attendance_allowance'])
            + remove_comma_from_number(datas['diligence_allowance'])
            + remove_comma_from_number(datas['accident_free_allowance']))

        datas['welfare_meal_allowance'] = format_number_with_commas(int(self.member_salary['welfare_meal_allowance']))
        datas['welfare_fuel_allowance'] = format_number_with_commas(int(self.member_salary['welfare_fuel_allowance']))

        datas['sum_ordinary_salary_and_statutory_allowance'] = format_number_with_commas(
            remove_comma_from_number(datas['ordinary_salary']) + \
            remove_comma_from_number(datas['statutory_allowance']) + \
            remove_comma_from_number(datas['welfare_meal_allowance']) + \
            remove_comma_from_number(datas['welfare_fuel_allowance'])
        )
        datas['total'] = format_number_with_commas(remove_comma_from_number(datas['sum_ordinary_salary_and_statutory_allowance']) + remove_comma_from_number(datas['additional']) - remove_comma_from_number(datas['deduction']))
        

        return datas