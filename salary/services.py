from config.custom_logging import logger
from django.forms.models import model_to_dict
from dispatch.models import DispatchRegularlyData, MorningChecklist, EveningChecklist, DispatchRegularly
from dispatch.selectors import DispatchSelector
from humanresource.models import Member, Salary
from humanresource.selectors import MemberSelector
from common.constant import TODAY
from common.formatter import format_number_with_commas, remove_comma_from_number
from common.datetime import calculate_time_difference, get_hour_minute_with_colon, get_hour_minute, get_minute_from_colon_time, last_day_of_month, get_weekday_from_date, calculate_date_difference, add_days_to_date, last_date_of_month, get_next_sunday_after_last_day, calculate_time_with_minutes, calculate_minute_difference, get_mondays_from_last_week_of_previous_month, get_holiday_list, get_date_range_list, count_range_hits
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
    def get_work_time(self, connects_list):
        minutes = 0

        for connect in connects_list:
            minutes += connect['total_time']
            # print("TESt", connect['total_time'], connect['connect_time_list'])
            # print(connect['start_time1'],connect['end_time1'], connect['start_time2'],connect['end_time2'],)

        # minutes = sum(self.round_up_to_nearest_ten(int(connect['route_time'])) if connect['route_time'] else self.round_up_to_nearest_ten(calculate_time_difference(connect['departure_date'], connect['arrival_date'])) for connect in daily_connects)
        return minutes

    def work_time_for_date(self, date):
        minutes = 0
        connects_list = self.get_connects_time_list(date)
        for connect in connects_list:
            minutes += connect['total_time']
            # print("TESt", connect['total_time'], connect['connect_time_list'])
            # print(connect['start_time1'],connect['end_time1'], connect['start_time2'],connect['end_time2'],)

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
            minutes = self.work_time_for_date(date)
            total_minutes += minutes
        return total_minutes
    
     # 마지막 일요일이 다음달일 경우 weekly_minute 계산하기
    # def get_work_minutes_from_next_month_sunday(self):
    #     last_date = last_date_of_month(f'{self.month}-01')
    #     calculated_day = calculate_date_difference(last_date, get_next_sunday_after_last_day(self.month))
    #     total_minutes = 0
    #     for i in range(calculated_day):
    #         date = add_days_to_date(last_date, i + 1)
    #         minutes = self.get_work_time(date)
    #         total_minutes += minutes
    #     return total_minutes

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
            
    def calculate_night_shift_minutes(self, departure_time, arrival_time):
        # 출발 및 도착 시간 설정 (%H:%M 형식)
        departure = datetime.strptime(departure_time, '%H:%M')
        arrival = datetime.strptime(arrival_time, '%H:%M')

        # 야근 시간대 설정
        night_start = datetime.strptime('00:00', '%H:%M')
        night_end = datetime.strptime('06:00', '%H:%M')
        mid_night_start = datetime.strptime('22:00', '%H:%M')
        mid_night_end = datetime.strptime('23:59', '%H:%M')

        # 야근 시간 계산 변수 초기화
        night_shift_minutes = 0

        # 도착 시간이 자정을 넘어간 경우 처리
        if arrival < departure:
            # 자정 이전까지의 야근 시간 계산 (22:00 ~ 23:59)
            if departure <= mid_night_end:
                night_shift_minutes += (mid_night_end - max(mid_night_start, departure)).seconds // 60 + 1
            
            # 자정 이후 (00:00)부터 도착 시간까지의 야근 시간 계산 (00:00 ~ 06:00)
            night_shift_minutes += (arrival - night_start).seconds // 60
        else:
            # 00:00 ~ 06:00 시간대 야근 시간 계산
            if departure <= night_end:
                if arrival >= night_start:
                    night_shift_minutes += (min(arrival, night_end) - max(departure, night_start)).seconds // 60

            # 22:00 ~ 23:59 시간대 야근 시간 계산
            if departure <= mid_night_end:
                if arrival >= mid_night_start:
                    night_shift_minutes += (min(arrival, mid_night_end) - max(departure, mid_night_start)).seconds // 60

        return night_shift_minutes
    
    def get_night_shift_time(self, daily_connects):
        minutes = 0
        for connect in daily_connects:
            if connect['work_type'] == '일반':
                minutes += connect['night_work_time']
                continue
            if connect['start_time1'] and connect['end_time1']:
                minutes += self.calculate_night_shift_minutes(connect['start_time1'], connect['end_time1'])
            if connect['start_time2'] and connect['end_time2']:
                minutes += self.calculate_night_shift_minutes(connect['start_time2'], connect['end_time2'])
            
        return minutes

    def get_daily_meal_count(self, daily_connects) -> int:
        count = 0
        result = {}

        for connect in daily_connects:
            if connect['work_type'] == '일반':
                result = count_range_hits(connect['departure_date'], connect['arrival_date'], result)
            elif connect['start_time1'] and connect['end_time2']:
                # 날짜값 임의로 넣어줌
                date = connect['departure_date'][:10]
                result = count_range_hits(f"{date} {connect['start_time1']}", f"{date} {connect['end_time2']}", result)
        
        print("result", result)
        return len(result)

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

            'welfare_fuel_allowance': '0',
            'total': '0',

        }
    
    def get_connects_time_list(self, date):
        daily_connects = self.get_daily_connects(date)
        connect_list = []
        i = 0
        # 현재 운행 도착 시간과 다음 운행 출발 시간의 차이가 90분 이하
        is_time_difference_under_90 = False

        # 정류장 개수 8개 이하인 regulalry_id id 찾기
        # for connect in daily_connects:
        #     if connect['work_type'] == "출근" or connect['work_type'] == "퇴근":
        #         length = len(connect['stations_list'])
        #         if length < 8:
        #             regularly = DispatchRegularly.objects.get(id=connect['regularly_id'])
        #             id = regularly.regularly_id
        #             logger.info(f"정류장 에러 regularly_id = {regularly.id}\t\t{id}\t\t\t{id.id}")
        # return []
        for connect in daily_connects:
            connect_time_list = ['' for i in range(9)]

            # 일반
            if connect['work_type'] == '일반':
                route_time = int(connect['route_time']) if connect['route_time'] else 0
                connect_list.append({
                    'total_time': route_time,
                    'work_type': '일반',
                    'start_time1':  '',
                    'end_time1': '',
                    'start_time2':  '',
                    'end_time2': '',
                    'connect_time_list': '',
                    'night_work_time': int(connect['night_work_time']) if connect['night_work_time'] else 0,
                    'departure_date': connect['departure_date'],
                    'arrival_date': connect['arrival_date'],
                    'route': connect['route'],
                })
                i += 1
                continue

            # 업무
            if connect['work_type'] == '업무':
                connect_list.append({
                    'total_time': calculate_minute_difference(get_minute_from_colon_time(connect['departure_date'][11:]), get_minute_from_colon_time(connect['arrival_date'][11:])),
                    'work_type': connect['work_type'],
                    'start_time1': connect['departure_date'][11:],
                    'end_time1': connect['arrival_date'][11:],
                    'start_time2': "",
                    'end_time2': connect['arrival_date'][11:], # 식대 계산용
                    'connect_time_list': '',
                    'route': connect['route'],
                    'departure_date': connect['departure_date'],
                    'arrival_date': connect['arrival_date'],
                })
                i += 1
                continue

            # 출퇴근
            time_list = connect['stations_list']

            # 정류장 정보 없을 경우
            if not time_list:
                connect_list.append({
                    'total_time': 0,
                    'work_type': connect['work_type'],
                    'start_time1':  '',
                    'end_time1': '',
                    'start_time2':  '',
                    'end_time2': '',
                    'route': connect['route'],
                })
                i += 1
                continue

            length = len(connect['stations_list'])
            departure_index = 3 # 첫 정류장 대기장소 인덱스
            arrival_index = length - 3 # 사업장(도착지) 인덱스
            first_station_ready_index = 3 # 첫 정류장 대기장소 인덱스
            
            # 출발시간 정하기
            # start_time1 = 차고지
            # end_time1 = 첫정류장대기장소
            # start_time2 = 첫정류장(출발지)
            # end_time2 = 대기장소 + 10분(뒷정리)

            # is_time_difference_under_90 = 전 운행과 90분 차이 이내 여부
            start_time1 = self.get_start_time(i, daily_connects, is_time_difference_under_90)
            
            end_time1 = connect['stations_list'][departure_index]
            # 출발지 인덱스 = 4
            start_time2 = connect['stations_list'][4]

            connect_time_list[0] = start_time1 # DailySalaryStatus
            connect_time_list[1] = start_time1 # DailySalaryStatus

            if is_time_difference_under_90:
                connect_time_list[2] = start_time1 # DailySalaryStatus
                connect_time_list[3] = end_time1 # DailySalaryStatus
            else:
                connect_time_list[2] = connect['stations_list'][2] # DailySalaryStatus
                connect_time_list[3] = connect['stations_list'][3] # DailySalaryStatus


            connect_time_list[4] = connect['stations_list'][4] # DailySalaryStatus
            connect_time_list[5] = connect['stations_list'][arrival_index] # DailySalaryStatus
            
            # # is_time_difference_under_90 = 다음 운행과 90분 차이 이내 여부
            is_time_difference_under_90 = self.check_time_difference_under_90(i, daily_connects, departure_index, arrival_index)
            # print("is_time_difference_under_90", is_time_difference_under_90)
            if is_time_difference_under_90:
                end_time2 = connect['stations_list'][arrival_index]
                connect_time_list[6] = end_time2 # DailySalaryStatus
                connect_time_list[7] = end_time2 # DailySalaryStatus
                connect_time_list[8] = end_time2
            else:
                end_time2 = self.check_arrival_can_parking_outside(i, time_list, length, daily_connects)
                connect_time_list[6] = end_time2 # DailySalaryStatus
                connect_time_list[7] = end_time2 # DailySalaryStatus
                
                # 뒷정리 완료 = 그 날 마지막 운행이면 마지막에서 10분 추가
                if connect == daily_connects[len(daily_connects) - 1] or daily_connects[i + 1]['work_type'] == '일반' or daily_connects[i + 1]['work_type'] == '업무':
                    end_time2_minute = get_minute_from_colon_time(end_time2) + 10
                else:
                    end_time2_minute = get_minute_from_colon_time(end_time2)
                # +10분으로 자정이 넘으면 24시간 빼기
                if end_time2_minute >= 1440:
                    end_time2_minute -= 1440
                
                end_time2 = get_hour_minute_with_colon(end_time2_minute)
                connect_time_list[8] = get_hour_minute_with_colon(get_minute_from_colon_time(end_time2))
            

            
            # 운행시간이 자정을 넘겼을 떄 운행시간 계산
            # end_time2 + 10분(뒷정리 시간) 추가

            # 외부주차장 시간이 사전준비시간 이후 라면?
            route_time1 = calculate_minute_difference(get_minute_from_colon_time(start_time1), get_minute_from_colon_time(end_time1))
            route_time2 = calculate_minute_difference(get_minute_from_colon_time(start_time2), get_minute_from_colon_time(end_time2))

            connect_list.append({
                'total_time': route_time1 + route_time2,
                'work_type': connect['work_type'],
                'start_time1':  start_time1,
                'end_time1': end_time1,
                'start_time2':  start_time2,
                'end_time2': end_time2,
                'connect_time_list': connect_time_list,
                'route': connect['route'],
                'departure_date': connect['departure_date'],
                'arrival_date': connect['arrival_date'],
            })
            i += 1
        return connect_list

    # 이전 도착 시간과 현재 출발 시간 차이가 1시간 30
    def get_start_time(self, i, daily_connects, is_time_difference_under_90):
        time_list = daily_connects[i]['stations_list']
        
        if is_time_difference_under_90:
            prev_time_list = daily_connects[i - 1]['stations_list']        
            prev_arrival_time = prev_time_list[len(prev_time_list) - 3] # 도착지는 뒤에서 3번째 정류장
            return prev_arrival_time
        return self.check_departure_can_parking_outside(i, time_list)
        
    def check_departure_can_parking_outside(self, i, time_list):
        # 첫 운행일 경우에만 외부 주차 가능 여부 확인
        if i == 0 and self.member.can_parking_outside:
            return time_list[1]
        else:
            return time_list[0]

    def check_arrival_can_parking_outside(self, i, time_list, length, daily_connects):
        # 첫 운행일 경우에만 외부 주차 가능 여부 확인
        if (i == len(daily_connects) - 1 or daily_connects[i + 1]['work_type'] == '일반' or daily_connects[i + 1]['work_type'] == '업무') and self.member.can_parking_outside:
            return time_list[length - 1]
        else:
            return time_list[length - 2]


    def check_time_difference_under_90(self, i, daily_connects, departure_index, arrival_index) -> bool:
        time_list = daily_connects[i]['stations_list']
        
        # i가 마지막 운행이거나,
        # 다음 운행이 일반이거나,
        # 다음 운행이 3M일 경우 False
        if i >= len(daily_connects) - 1 or daily_connects[i + 1]['work_type'] == '일반' or daily_connects[i + 1]['work_type'] == '업무' or self.is3M(daily_connects, i + 1):
            return False
        
        # 다음 운행의 정류장 정보가 없으면 False
        next_time_list = daily_connects[i + 1]['stations_list']
        if not next_time_list:
            return False

        # 대기장소(내부), 대기장소(외부), 사전준비시간, 사업장 대기장소, 사업장, 정류장, 마지막 정류장, 차고지(내부), 차고지(외부), 뒷 정리 완료
        arrival_time = get_minute_from_colon_time(time_list[arrival_index])
        next_departure_time = get_minute_from_colon_time(next_time_list[departure_index])
        
        # 다음 출발시간 - 현재 도착시간 < 90 이면 도착지 이후 정류장들 전부 현재 도착시간
        time_difference = calculate_minute_difference(arrival_time, next_departure_time)
        # print("time_difference", time_difference, arrival_time, next_departure_time)
        return time_difference < 90

    def is3M(self, daily_connects, i) -> bool:
        try:
            # 현재랑 다음 운행이 쓰리엠인지 확인
            return "쓰리엠" in daily_connects[i]['group'] or \
                    (i + 1 < len(daily_connects) and "쓰리엠" in daily_connects[i + 1]['group'])
        except Exception as e:
            # logger.info(f"is3M error {e}")
            return False


    # 근무현황
    def get_calculate_times(self):
        morning_time_list = ['' for i in range(len(self.date_list))]
        evening_time_list = ['' for i in range(len(self.date_list))]
        wait_time_list = ['' for i in range(len(self.date_list))]
        work_time_list = ['' for i in range(len(self.date_list))]
        night_shift_time_list = ['' for i in range(len(self.date_list))]
        meal_list = ['' for i in range(len(self.date_list))]
        work_list = ['' for i in range(len(self.date_list))]
        holiday_time_list = ['' for i in range(len(self.date_list))]
        additional_holiday_time_list = ['' for i in range(len(self.date_list))]
        
        total_work_minute = 0
        total_night_shift_minute = 0
        total_weekly_minute = 0 # 주간 근로시간(최대30시간) 한달치
        total_within_law_extension_minute = 0
        total_outside_law_extension_minute = 0
        total_meal = 0

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

            connects_time_list = self.get_connects_time_list(date)

            weekday = get_weekday_from_date(date)
            daily_connects = self.get_daily_connects(date)
            minutes = self.get_work_time(connects_time_list)
            work_time = get_hour_minute_with_colon(minutes) if minutes != 0 else ''

            work_type = self.get_work_type(minutes, weekday, weekly_minute)
            holiday_check = self.is_holiday(self.holiday_data, date) or work_type == '주휴'
            # weekly_minute += minutes
            weekly_minute, within_law_extension_minute, outside_law_extension_minute = self.calculate_work_minutes(minutes, weekly_minute, within_law_extension_minute, outside_law_extension_minute, holiday_check)
            # total_within_law_extension_minute += within_law_extension_minute
            # total_outside_law_extension_minute += outside_law_extension_minute

            weekly_work_count += 1 if daily_connects else  0
            night_shift_time = self.get_night_shift_time(connects_time_list)

            
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

            MEAL_PRICE = 5000
            meal_list[i] = self.get_daily_meal_count(connects_time_list) * MEAL_PRICE
            print('i', i, meal_list[i])
            total_meal += meal_list[i]

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

            'meal_list': meal_list,
            'meal': total_meal,

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
        weekly_holiday_allowance = ordinary_hourly_wage * 6 * weekly_holiday_count - int(self.member_salary['weekly_holiday_allowance_deduction'])# 주휴수당
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
        meal = times_data['meal']
        statutory_allowance = math.ceil(weekly_holiday_allowance + legal_holiday_allowance + weekly_within_law_extension_wage + weekly_outside_law_extension_wage + weekly_extension_additional_wage + night_shift_wage + holiday_work_wage + additional_holiday_work_wage + additional_holiday_work_wage_half + annual_allowance + meal)

        return {
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

        # datas['new_annual_allowance'] = format_number_with_commas(int(self.member_salary['new_annual_allowance']))
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
            # - remove_comma_from_number(datas['meal'])
            - remove_comma_from_number(datas['annual_allowance'])
            # + remove_comma_from_number(datas['new_annual_allowance'])
            + remove_comma_from_number(datas['team_leader_allowance_roll_call'])
            + remove_comma_from_number(datas['team_leader_allowance_vehicle_management'])
            + remove_comma_from_number(datas['team_leader_allowance_task_management'])
            + remove_comma_from_number(datas['full_attendance_allowance'])
            + remove_comma_from_number(datas['diligence_allowance'])
            + remove_comma_from_number(datas['accident_free_allowance']))

        datas['welfare_fuel_allowance'] = format_number_with_commas(int(self.member_salary['welfare_fuel_allowance']))

        datas['sum_ordinary_salary_and_statutory_allowance'] = format_number_with_commas(
            remove_comma_from_number(datas['ordinary_salary']) + \
            remove_comma_from_number(datas['statutory_allowance']) + \
            remove_comma_from_number(datas['welfare_fuel_allowance'])
        )
        datas['total'] = format_number_with_commas(remove_comma_from_number(datas['sum_ordinary_salary_and_statutory_allowance']) + remove_comma_from_number(datas['additional']) - remove_comma_from_number(datas['deduction']))
        

        return datas



class SalaryDataController2:
    member_list = []
    dispatch_selector = DispatchSelector
    data_collector_class = SalaryTableDataCollector3

    def __init__(self, month):
        self.set_date_datas(month)
        self.get_connect_time_list_from_dispatch_selector()


    def set_date_datas(self, month):
        self.month = month
        self.first_date = f"{month}-01"
        self.mondays = get_mondays_from_last_week_of_previous_month(month)
        self.start_date = self.mondays[0] if self.mondays[0][:7] != month else self.first_date
        self.holiday_data = get_holiday_list(month)
        self.date_list = get_date_range_list(self.first_date, last_date_of_month(self.first_date))


    def get_connect_time_list_from_dispatch_selector(self):
        self.connect_time_list = self.dispatch_selector().get_driving_time_list(self.start_date, get_next_sunday_after_last_day(self.month))

    def get_datas(self, member_list):
        datas = {}
        self.member_list = []
        for member in member_list:
            data_collector = self.data_collector_class(member, self.month, self.mondays, self.connect_time_list, self.holiday_data, self.date_list)
            temp_data = data_collector.get_collected_data()

            datas[member.id] = temp_data
            datas[member.id]['member__name'] = member.name
            datas[member.id]['member__role'] = member.role
            datas[member.id]['member__entering_date'] = member.entering_date
            # 임금
            datas[member.id]['wage'] = format_number_with_commas(
                remove_comma_from_number(temp_data['total'])
                - remove_comma_from_number(temp_data['service_allowance'])
                # - remove_comma_from_number(temp_data['new_annual_allowance'])
                - remove_comma_from_number(temp_data['team_leader_allowance_roll_call'])
                - remove_comma_from_number(temp_data['team_leader_allowance_vehicle_management'])
                - remove_comma_from_number(temp_data['team_leader_allowance_task_management'])
                - remove_comma_from_number(temp_data['full_attendance_allowance'])
                - remove_comma_from_number(temp_data['diligence_allowance'])
                - remove_comma_from_number(temp_data['accident_free_allowance'])
                - remove_comma_from_number(temp_data['meal'])
                - remove_comma_from_number(temp_data['welfare_fuel_allowance'])
                - remove_comma_from_number(temp_data['weekly_holiday_allowance'])
                - remove_comma_from_number(temp_data['additional']) 
                + remove_comma_from_number(temp_data['deduction'])   
            )
            # 팀장수당
            datas[member.id]['team_leader_allowance'] = format_number_with_commas(
                + remove_comma_from_number(temp_data['team_leader_allowance_roll_call'])
                + remove_comma_from_number(temp_data['team_leader_allowance_vehicle_management'])
                + remove_comma_from_number(temp_data['team_leader_allowance_task_management'])
            )

            self.member_list.append(member)

        return datas
