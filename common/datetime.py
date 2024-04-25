from datetime import datetime

def calculate_time_difference(start_time_str, end_time_str):
    # 입력된 시간 문자열을 datetime 객체로 변환
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

    # 두 datetime 객체의 차이 계산
    time_difference = end_time - start_time

    # timedelta 객체에서 일(day), 시간(hour), 분(minute)을 추출
    total_seconds = time_difference.seconds
    minutes = (total_seconds % 3600) // 60

    # 결과를 문자열로 포맷팅하여 반환
    return minutes