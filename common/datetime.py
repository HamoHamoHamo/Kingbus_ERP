from datetime import datetime, timedelta
from common.constant import WEEK2, DATE_FORMAT, DATE_TIME_FORMAT

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