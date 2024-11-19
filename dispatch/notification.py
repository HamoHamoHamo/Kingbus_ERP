from .models import *
from datetime import datetime, timedelta
from config.settings.base import TODAY, FORMAT
from config.custom_logging import logger
from django.db.models import Q, Prefetch
from humanresource.views import send_message

def driver_check_notification():
    now = datetime.now()
    time1 = now + timedelta(hours=1.5)
    time2 = now + timedelta(hours=1)
    time3 = now + timedelta(minutes=20)
    time0 = now

    time_str = lambda t: t.strftime("%Y-%m-%d %H:%M")

    # 알림 데이터 필터링 및 중복 제거
    data1 = set(DispatchRegularlyConnect.objects.filter(
        departure_date=time_str(time1), 
        check_regularly_connect__wake_time='', 
        check_regularly_connect__wake_time_has_issue__isnull=True
    ).values_list('driver_id', flat=True)) | set(
        DispatchOrderConnect.objects.filter(
            departure_date=time_str(time1), 
            check_order_connect__wake_time='', 
            check_order_connect__wake_time_has_issue__isnull=True
        ).values_list('driver_id', flat=True)
    )

    data2 = set(DispatchRegularlyConnect.objects.filter(
        departure_date=time_str(time2), 
        check_regularly_connect__drive_time='', 
        check_regularly_connect__drive_time_has_issue__isnull=True
    ).values_list('driver_id', flat=True)) | set(
        DispatchOrderConnect.objects.filter(
            departure_date=time_str(time2), 
            check_order_connect__drive_time='', 
            check_order_connect__drive_time_has_issue__isnull=True
        ).values_list('driver_id', flat=True)
    )

    data3 = set(DispatchRegularlyConnect.objects.filter(
        departure_date=time_str(time3), 
        check_regularly_connect__departure_time=''
    ).values_list('driver_id', flat=True)) | set(
        DispatchOrderConnect.objects.filter(
            departure_date=time_str(time3), 
            check_order_connect__departure_time=''
        ).values_list('driver_id', flat=True)
    )

    # 관리자 및 팀장 정보 조회
    admin_and_team_leads = list(Member.objects.filter(role__in=["관리자", "팀장"], use="사용"))

    # 알림 발송 데이터 매핑

    data_map = {
        0: {"data_list": data1, "text": "운행 준비 확인 바랍니다", "title": "운행 1시간 30분 전입니다"},
        1: {"data_list": data2, "text": "운행 출발 확인 바랍니다", "title": "운행 1시간 전입니다"},
        2: {"data_list": data3, "text": "첫 정류장 도착 확인 바랍니다", "title": "운행 20분 전입니다"},
    }

    # 기사 정보를 한 번에 가져오기
    driver_ids = set(data1) | set(data2) | set(data3)
    drivers = Member.objects.filter(id__in=driver_ids).in_bulk()

    # 기사 및 관리자 알림 발송
    for i, alert_info in data_map.items():
        data_list = alert_info["data_list"]
        text = alert_info["text"]
        title = alert_info["title"]

        if i != 3:  # 기사 알림 (0분 전 제외)
            for user_id in data_list:
                user = drivers.get(user_id)
                if user:
                    if i == 0:
                        DispatchRegularlyConnect.objects.filter(
                            driver_id=user_id, departure_date=time_str(time1)
                        ).update(status="운행 준비")
                        
                        DriverCheck.objects.filter(
                            regularly_id__driver_id=user_id,
                            regularly_id__departure_date=time_str(time1)
                        ).update(wake_time_has_issue=True)

                    elif i == 1:
                        DriverCheck.objects.filter(
                            regularly_id__driver_id=user_id,
                            regularly_id__departure_date=time_str(time2)
                        ).update(drive_time_has_issue=True)

                    send_message(title, text, user.token, None)

        if i == 1:
            send_admin_alerts(regularly_dispatch1, order_dispatch1, admin_and_team_leads, "운행 준비 확인 필요", "아직 운행 준비 확인 되지 않았습니다.")
        elif i == 2:
            send_admin_alerts(regularly_dispatch2, order_dispatch2, admin_and_team_leads, "운행 시작 확인 필요", "아직 운행 시작 상태가 아닙니다.")

    send_admin_alerts(regularly_dispatch0, order_dispatch0, admin_and_team_leads, "출발 확인 필요", "아직 출발 확인되지 않았습니다.")
    print("DATETIME : ", now.strftime("%Y-%m-%d %H:%M"))

def send_admin_alerts(regular_dispatches, order_dispatches, admin_and_team_leads, admin_title, admin_text):
    # has_issue 업데이트 및 관리자 알림 전송
    for dispatch in list(regular_dispatches) + list(order_dispatches):
        dispatch.has_issue = True
        dispatch.save()
        for admin in admin_and_team_leads:
            send_message(admin_title, f"기사 {dispatch.driver_id} {admin_text}", admin.token, None)
   
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
                StationArrivalTime.create_new(connect, station)
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
    # admin_station_check_problem_notification("2024-08-01 06:45")
    driver_check_notification()
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