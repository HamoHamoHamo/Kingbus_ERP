from .models import *
from datetime import datetime, timedelta
from config.settings.base import TODAY, FORMAT
from config.custom_logging import logger
from django.db.models import Q, Prefetch
from humanresource.views import send_message

def driver_check_notification():
    time1 = str(datetime.now() + timedelta(hours=1.5))[:16]
    time2 = str(datetime.now() + timedelta(hours=1))[:16]
    time3 = str(datetime.now() + timedelta(minutes=20))[:16]

    data1 = list(DispatchRegularlyConnect.objects.filter(departure_date=time1).filter(check_regularly_connect__wake_time='').values_list('driver_id', flat=True))
    data2 = list(DispatchRegularlyConnect.objects.filter(departure_date=time2).filter(check_regularly_connect__drive_time='').values_list('driver_id', flat=True))
    data3 = list(DispatchRegularlyConnect.objects.filter(departure_date=time3).filter(check_regularly_connect__departure_time='').values_list('driver_id', flat=True))
    data4 = list(DispatchOrderConnect.objects.filter(departure_date=time1).filter(check_order_connect__wake_time='').values_list('driver_id', flat=True))
    data5 = list(DispatchOrderConnect.objects.filter(departure_date=time2).filter(check_order_connect__drive_time='').values_list('driver_id', flat=True))
    data6 = list(DispatchOrderConnect.objects.filter(departure_date=time3).filter(check_order_connect__departure_time='').values_list('driver_id', flat=True))

    for i in range(3):
        if i == 0:
            data_list = set(data1 + data4)
            text = '기상 확인 바랍니다'
            title = '운행 1시간 30분 전입니다'
        if i == 1:
            data_list = set(data2 + data5)
            text = '운행 출발 확인 바랍니다'
            title = '운행 1시간 전입니다'
        if i == 2:
            data_list = set(data3 + data6)
            text = '첫 정류장 도착 확인 바랍니다'
            title = '운행 20분 전입니다'
            
        for user_id in data_list:
            user = Member.objects.get(id=user_id)
            token = user.token
            try:
                send_message(title, text, token, None)
            except Exception as e:
                print(e)
            print("TOKEN ", user.name)
    print("DATETIME : ", str(datetime.now())[:16])

# rpad 관리자 알림

# 정류장 체크 시간 맞춰 체크 하지 않을 경우 관리자에게 알림
def admin_station_check_problem_notification(date_time=str(datetime.now())[:16]):
    STATION_TYPE = [
        '정류장',
        '사업장',
        '마지막 정류장',
    ]
    # 기준 시간이 되는 현재 시간에서 15분을 빼서 예상 도착 시각을 설정
    now = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
    threshold_time = (now - timedelta(minutes=15)).strftime("%H:%M")
    today_date = now.strftime("%Y-%m-%d")

    # DispatchRegularlyConnect를 기준으로 필터링하고 관련 데이터를 Prefetch로 미리 로드
    connects = DispatchRegularlyConnect.objects.filter(
        departure_date__startswith=today_date
    ).prefetch_related(
        Prefetch(
            "regularly_id__regularly_station",
            queryset=DispatchRegularlyStation.objects.filter(
                time=threshold_time,
                station_type__in=STATION_TYPE
            ),
            to_attr="filtered_stations"
        ),
        Prefetch(
            "station_arrival_time",
            queryset=StationArrivalTime.objects.filter(
                arrival_time__startswith=today_date
            ),
            to_attr="arrival_records"
        )
    )

    # DispatchRegularlyConnect 각각에 대해 정류장 도착 여부를 확인
    for connect in connects:
        for station in connect.regularly_id.filtered_stations:
            # 해당 Station에 대한 도착 기록이 없는 경우를 찾기 위해 arrival_records를 체크
            if not any(arrival.station_id_id == station.id for arrival in connect.arrival_records):
                connect.has_issue = True
                connect.not_update_salary = True
                connect.save()
                logger.info(f"{connect} station_index={station.index}")
                print(f"{connect} station_index={station.index}")
                send_notification_to_manager("문제 발생", f"{connect} {connect.bus_id.vehicle_num}({connect.driver_id.name})")
    print(f"admin_station_check_problem_notification {date_time}")

# 관리자, 팀장에게 알림 보내기
def send_notification_to_manager(title: str, text: str):
    targets = Member.objects.filter(use="사용").filter(Q(role="팀장") | Q(role="관리자"))
    for target in targets:
        print("Target: ", target)
        send_message(title, text, target.token, None)


from django.db import connection, reset_queries
import time

def debug_send_missing_arrival_time_notifications():
    reset_queries()  # 쿼리 기록을 초기화
    start_time = time.time()

    # 함수 실행
    admin_station_check_problem_notification("2024-08-01 06:45")
    # driver_check_notification()

    end_time = time.time()
    execution_time = end_time - start_time

    # 쿼리 정보 출력
    for query in connection.queries:
        print(f"Time: {query['time']}s | SQL: {query['sql']}")

    print(f"Total execution time: {execution_time:.2f}s")
    print(f"Total queries: {len(connection.queries)}")



# rpap 관리자 알림
def admin_dispatch_check_notification():
    order_list = DispatchOrder.objects.exclude(Q(firebase_uid=None) | Q(info_order=None) | Q(contract_status="예약확정") | Q(contract_status="확정")).filter(departure_date__gte=TODAY)

    target_list = []
    try:
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="김인숙"))
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="이세명"))
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="박유진"))
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="엄성환"))

    except Exception as e:
        logger.error(f"ERROR {e}")
    for order in order_list:
        for target in target_list:
            send_message("TRP에서 계약현황-예약확정을 해주세요", f"{order.route}\n{order.departure_date} ~ {order.arrival_date}", target.token, None)

def admin_complete_check_notification():
    order_list = DispatchOrder.objects.exclude(Q(firebase_uid=None) | Q(info_order=None) | Q(contract_status="확정")).filter(departure_date__gte=TODAY)

    target_list = []
    try:
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="김인숙"))
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="이세명"))
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="박유진"))
        target_list.append(Member.objects.get(use="사용", authority__lte=1, name="엄성환"))

    except Exception as e:
        logger.error(f"ERROR {e}")
    for order in order_list:
        for target in target_list:
            send_message("계약금 입금 확인 후 TRP에서 계약현황-확정을 해주세요", f"{order.route}\n{order.departure_date} ~ {order.arrival_date}", target.token, None)