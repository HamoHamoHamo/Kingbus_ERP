import calendar
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from common.constant import WEEK2, DATE_FORMAT, DATE_TIME_FORMAT
from my_settings import OPEN_API_KEY
from django.core.exceptions import BadRequest
from config.custom_logging import logger
from typing import Dict, Any

from django.core.cache import cache

def calculate_time_difference(start_time_str, end_time_str):
    # 입력된 시간 문자열을 datetime 객체로 변환
    try:
        start_time = datetime.strptime(start_time_str, DATE_TIME_FORMAT)
        end_time = datetime.strptime(end_time_str, DATE_TIME_FORMAT)
    
    except:
        return 0

    # 두 datetime 객체의 차이 계산
    time_difference = end_time - start_time

    # timedelta 객체에서 일(day), 시간(hour), 분(minute)을 추출
    total_seconds = time_difference.seconds

    minutes = total_seconds // 60

    # 결과를 문자열로 포맷팅하여 반환
    return minutes

def calculate_date_difference(start_date_str, end_date_str):
    # 입력된 시간 문자열을 datetime 객체로 변환
    start_date = datetime.strptime(start_date_str, DATE_FORMAT)
    end_date = datetime.strptime(end_date_str, DATE_FORMAT)

    # 두 datetime 객체의 차이 계산
    date_difference = end_date - start_date

    # timedelta 객체에서 일(day), 시간(hour), 분(minute)을 추출
    return date_difference.days

def calculate_minute_difference(start_minute, end_minute):
    try:
        int(start_minute)
        int(end_minute)
        # 도착시간이 자정을 넘을 경우
        if end_minute >= start_minute:
            return end_minute - start_minute
        else:
            return 24 * 60 + end_minute - start_minute
    except ValueError:
        raise Exception("Invalid Format")

def last_day_of_month(date_str):
    try:
        # 입력된 날짜 문자열을 datetime 객체로 변환
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
        
        # 다음 달의 첫 날을 구하기 위해 입력된 날짜에 +1 한 후 해당 월의 1일로 설정
        first_day_of_next_month = datetime(date_obj.year, date_obj.month, 1) + timedelta(days=32)
        
        # 해당 월의 1일에서 1일을 빼서 이전 월의 마지막 날을 구함
        last_day_of_month = first_day_of_next_month - timedelta(days=first_day_of_next_month.day)
        
        return last_day_of_month.day  # 해당 월의 마지막 날짜 반환
    except ValueError:
        return None  # 유효하지 않은 날짜 형식이면 None 반환

def last_date_of_month(date_str):
    try:
        # 입력된 날짜 문자열을 datetime 객체로 변환
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
        
        # 다음 달의 첫 날을 구하기 위해 입력된 날짜에 +1 한 후 해당 월의 1일로 설정
        first_day_of_next_month = datetime(date_obj.year, date_obj.month, 1) + timedelta(days=32)
        
        # 해당 월의 1일에서 1일을 빼서 이전 월의 마지막 날을 구함
        last_day_of_month = first_day_of_next_month - timedelta(days=first_day_of_next_month.day)
        
        return last_day_of_month.strftime('%Y-%m-%d')  # 해당 월의 마지막 날짜 반환
    except ValueError:
        return None  # 유효하지 않은 날짜 형식이면 None 반환

def get_hour_minute(minutes):
    convert_hours = abs(minutes) // 60
    convert_minutes = abs(minutes) % 60
    
    return f'-{convert_hours}시간 {convert_minutes}분' if minutes < 0 else f'{convert_hours}시간 {convert_minutes}분'


def get_hour_minute_with_colon(minutes):
    hour = abs(minutes) // 60
    hour = f"0{hour}" if hour < 10 else str(hour)
    
    minute = abs(minutes) % 60
    minute = f"0{minute}" if minute < 10 else str(minute)
    
    return f"{hour}:{minute}"

def get_minute_from_colon_time(time: str):
    if len(time) != 5:
        return "Invalid time format"
    return int(time[:2]) * 60 + int(time[3:])

def add_days_to_date(date_string, days_to_add):
    try:
        # 문자열 형식의 날짜를 datetime 객체로 변환
        date_obj = datetime.strptime(date_string, DATE_FORMAT)
        # 주어진 일수를 더한 후의 날짜를 계산
        new_date = date_obj + timedelta(days=days_to_add)
        # 새로운 날짜를 문자열 형식으로 반환
        return new_date.strftime(DATE_FORMAT)
    except ValueError:
        # 날짜 형식이 잘못된 경우 예외 처리
        return "Invalid date format"

def get_weekday_from_date(date):
    try:
        date_type = datetime.strptime(date, DATE_FORMAT)
    except Exception:
        return ''
    return WEEK2[date_type.weekday()]

def get_next_monday(date_str):
    # 입력된 문자열을 datetime 객체로 변환
    date = datetime.strptime(date_str, DATE_FORMAT)
    
    # 현재 요일 (월요일 = 0, 일요일 = 6)
    current_weekday = date.weekday()
    
    # 다음 주 월요일까지 남은 일수 계산
    days_until_next_monday = 7 - current_weekday
    
    # 다음 주 월요일의 날짜 계산
    next_monday = date + timedelta(days=days_until_next_monday)
    
    # 날짜를 문자열 형식으로 변환하여 반환
    return next_monday.strftime("%Y%m%d")

def get_mid_time(time1, time2):
    # 시간을 datetime 객체로 변환
    time_format = "%H:%M"
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)
    
    # 두 시간 사이의 차이를 계산
    if t1 > t2:
        t1, t2 = t2, t1  # t1이 항상 t2보다 먼저 오도록 스왑
    
    # 두 시간 사이의 중간값 계산
    mid_time = t1 + (t2 - t1) / 2
    
    # 중간값을 "HHMM" 형식으로 변환하여 반환
    return mid_time.strftime("%H%M")

def get_mondays_from_last_week_of_previous_month(month):
    # 주어진 month의 첫 날을 구합니다.
    first_day_of_month = datetime.strptime(month, "%Y-%m")

    # 첫 날이 월요일인 경우 전달을 포함하지 않습니다.
    if first_day_of_month.weekday() == 0:
        # 주어진 month의 첫 월요일부터 해당 월의 모든 월요일을 구합니다.
        mondays = []
        current_day = first_day_of_month
        while current_day.month == first_day_of_month.month:
            mondays.append(datetime.strftime(current_day, DATE_FORMAT))
            current_day += timedelta(weeks=1)
        return mondays

    # 첫 날이 월요일이 아닌 경우 전달의 마지막 날을 구합니다.
    last_day_of_previous_month = first_day_of_month - timedelta(days=1)

    # 전달의 마지막 주의 월요일을 구합니다.
    last_week_start = last_day_of_previous_month - timedelta(days=last_day_of_previous_month.weekday())

    # 전달의 마지막 주의 월요일부터 시작하여 모든 월요일을 구합니다.
    mondays = []
    current_day = last_week_start
    while current_day < first_day_of_month or current_day.month == first_day_of_month.month:
        mondays.append(datetime.strftime(current_day, DATE_FORMAT))
        current_day += timedelta(weeks=1)
    
    return mondays

def get_holiday_list(year_month):
    try:
        holiday_data = cache.get(f"holiday:{year_month}")
        if holiday_data:
            return holiday_data
    except Exception as e:
        logger.error(f"redis error {e}")

    api_url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'

    try:
        year = year_month[:4]
        month = year_month[5:7]
        datetime.strptime(year, "%Y")
        datetime.strptime(month, "%m")
    except:
        raise BadRequest("year, month 양식에 안 맞음")
    
    params = {
        'serviceKey': OPEN_API_KEY,
        'solYear': year,
        'solMonth': month,
    }
    
    response = requests.get(api_url, params=params)
    holiday_data = parse_xml_data(response.content)

    # return [item['locdate'] for item in parse_xml_data(response.content)]
    filtered_list = [item for item in holiday_data['date_name_list'] if '대체' not in item]

    holiday_data['count'] = len(filtered_list)
    
    try:
        cache.set(f"holiday:{year_month}", holiday_data)
    except Exception as e:
        logger.error(f"redis error {e}")


    return holiday_data

def parse_xml_data(xml_data):
    # XML 데이터를 문자열로 변환
    xml_data_str = xml_data.decode('utf-8')
    
    # XML 데이터 파싱
    root = ET.fromstring(xml_data_str)

    # items 요소 찾기
    items = root.find('.//items')
    
    # item 요소 파싱
    item_list = []
    locdate_list = []
    date_name_list = []
    for item in items.findall('item'):
        item_data = {
            'dateKind': item.find('dateKind').text,
            'dateName': item.find('dateName').text,
            'isHoliday': item.find('isHoliday').text,
            'locdate': item.find('locdate').text,
            'seq': item.find('seq').text
        }
        if len(locdate_list) == 0 or locdate_list[len(locdate_list) - 1] != item_data['locdate']:
            locdate_list.append(item_data['locdate'])
            date_name_list.append(item_data['dateName'])
        # item_list.append(item_data)
    
    return {
        'date_name_list': date_name_list, 
        'locdate_list': locdate_list,
    }

def get_next_sunday_after_last_day(month_str):
    """
    주어진 'YYYY-MM' 형식의 문자열을 입력받아
    해당 월의 마지막 날이 일요일이면 그대로 반환하고,
    아니라면 다음 일요일 날짜를 반환합니다.
    반환값은 문자열 형식의 날짜입니다.
    """
    # 문자열에서 연도와 월 추출
    year, month = map(int, month_str.split('-'))
    
    # 주어진 달의 마지막 날 구하기
    _, last_day = calendar.monthrange(year, month)
    last_day_date = datetime(year, month, last_day)
    
    # 마지막 날이 일요일인지 확인
    if last_day_date.weekday() == 6:  # 6은 일요일
        return last_day_date.strftime('%Y-%m-%d')
    else:
        # 다음 일요일 계산
        days_until_sunday = 6 - last_day_date.weekday()
        next_sunday = last_day_date + timedelta(days=days_until_sunday)
        return next_sunday.strftime('%Y-%m-%d')


def get_date_range_list(start_date_str, end_date_str):
    # 문자열을 datetime 객체로 변환
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # 기간 동안의 날짜를 리스트에 담음
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return date_list

def calculate_time_with_minutes(time_str, minutes):
    # 문자열을 datetime 객체로 변환
    if time_str[:2] == '24':
        time_str = f'00:{time_str[3:]}'
    time_obj = datetime.strptime(time_str, "%H:%M")
    
    # 분 데이터를 더하거나 빼기
    new_time_obj = time_obj + timedelta(minutes=minutes)

    # 결과 시간을 "HH:MM" 형식으로 반환
    return new_time_obj.strftime("%H:%M")

# 출발 시간과 도착 시간이 특정 시간 범위에 해당할 경우 카운트를 1씩 증가시키는 함수
def count_range_hits(start_time_str, end_time_str, result) -> Dict[str, Any]:
    # 주어진 시간 문자열을 datetime 객체로 변환
    start_time = datetime.strptime(start_time_str, DATE_TIME_FORMAT)
    end_time = datetime.strptime(end_time_str, DATE_TIME_FORMAT)
    
    # 범위 설정: 04:00 ~ 10:00, 17:00 ~ 21:00
    RANGES = [
        (timedelta(hours=4), timedelta(hours=10)),
        (timedelta(hours=17), timedelta(hours=21)),
    ]
    
    # 현재 시간을 출발 시간으로 초기화
    current_time = start_time
    while current_time <= end_time.replace(hour=23, minute=59):
        # 현재 날짜의 04:00과 10:00, 17:00과 21:00 범위를 확인
        for start_range, end_range in RANGES:
            range_start_time = current_time.replace(hour=start_range.seconds // 3600, minute=0)
            range_end_time = current_time.replace(hour=end_range.seconds // 3600, minute=0)
            
            # 현재 범위가 주어진 출발~도착 시간 내에 있으면 카운트를 증가
            if start_time <= range_end_time and end_time >= range_start_time:
                result[datetime.strftime(range_start_time, DATE_TIME_FORMAT)] = 1

        # 현재 시간을 하루씩 증가시킴
        current_time += timedelta(days=1)
    
    return result