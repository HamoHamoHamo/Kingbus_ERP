from .models import *
from datetime import datetime, timedelta
from config.settings.base import TODAY, FORMAT
from config.custom_logging import logger
from django.db.models import Q
from humanresource.views import send_message

def driver_check_notification():
    # 알림 시간 계산
    now = datetime.now()
    time1 = now + timedelta(hours=1.5)
    time2 = now + timedelta(hours=1)
    time3 = now + timedelta(minutes=20)
    time0 = now

    # 시간 문자열 생성
    time_str = lambda t: t.strftime("%Y-%m-%d %H:%M")

    # 알림 데이터 필터링 및 중복 제거
    data1 = set(DispatchRegularlyConnect.objects.filter(departure_date=time_str(time1), check_regularly_connect__wake_time='').values_list('driver_id', flat=True)) | \
            set(DispatchOrderConnect.objects.filter(departure_date=time_str(time1), check_order_connect__wake_time='').values_list('driver_id', flat=True))
    
    data2 = set(DispatchRegularlyConnect.objects.filter(departure_date=time_str(time2), check_regularly_connect__drive_time='').values_list('driver_id', flat=True)) | \
            set(DispatchOrderConnect.objects.filter(departure_date=time_str(time2), check_order_connect__drive_time='').values_list('driver_id', flat=True))

    data3 = set(DispatchRegularlyConnect.objects.filter(departure_date=time_str(time3), check_regularly_connect__departure_time='').values_list('driver_id', flat=True)) | \
            set(DispatchOrderConnect.objects.filter(departure_date=time_str(time3), check_order_connect__departure_time='').values_list('driver_id', flat=True))

    # 상태 필터링
    regularly_dispatch1 = DispatchRegularlyConnect.objects.filter(driver_id__in=data2, departure_date=time_str(time2), status="운행 준비")
    order_dispatch1 = DispatchOrderConnect.objects.filter(driver_id__in=data2, departure_date=time_str(time2), status="운행 준비")
    regularly_dispatch2 = DispatchRegularlyConnect.objects.filter(driver_id__in=data3, departure_date=time_str(time3), status="탑승 및 운행 시작")
    order_dispatch2 = DispatchOrderConnect.objects.filter(driver_id__in=data3, departure_date=time_str(time3), status="탑승 및 운행 시작")
    regularly_dispatch0 = DispatchRegularlyConnect.objects.filter(departure_date=time_str(time0), status="첫 정류장 도착")
    order_dispatch0 = DispatchOrderConnect.objects.filter(departure_date=time_str(time0), status="첫 정류장 도착")

    # 관리자 및 팀장 정보 미리 조회
    admin_and_team_leads = list(Member.objects.filter(role__in=["관리자", "팀장"], use="사용"))

    # 알림 발송 데이터 맵핑
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

        # 기사 알림 (0분 전 제외)
        if i != 3:
            for user_id in data_list:
                user = drivers.get(user_id)  # 이미 가져온 기사 데이터 사용
                if user:
                    send_message(title, text, user.token, None)

        # 관리자 알림 및 has_issue 업데이트 (1시간 전, 20분 전)
        if i == 1:
            send_admin_alerts(regularly_dispatch1, order_dispatch1, admin_and_team_leads, "운행 준비 확인 필요", "아직 운행 준비 확인 되지 않았습니다.")
        elif i == 2:
            send_admin_alerts(regularly_dispatch2, order_dispatch2, admin_and_team_leads, "운행 시작 확인 필요", "아직 운행 시작 상태가 아닙니다.")

    # 0분 전 관리자 알림
    send_admin_alerts(regularly_dispatch0, order_dispatch0, admin_and_team_leads, "출발 확인 필요", "아직 출발 확인되지 않았습니다.")
    print("DATETIME : ", now.strftime("%Y-%m-%d %H:%M"))

def send_admin_alerts(regular_dispatches, order_dispatches, admin_and_team_leads, admin_title, admin_text):
    # has_issue 업데이트 및 관리자 알림 전송
    for dispatch in list(regular_dispatches) + list(order_dispatches):
        dispatch.has_issue = True
        dispatch.save()
        for admin in admin_and_team_leads:
            send_message(admin_title, f"기사 {dispatch.driver_id} {admin_text}", admin.token, None)
	
    # for i in range(3):
    #     if i == 0:
    #         data_list = set(data1 + data4)
    #         text = '기상 확인 바랍니다'
    #         title = '운행 1시간 30분 전입니다'
    #         logger.error("") 
        
    #     if i == 1:
    #         data_list = set(data2 + data5)
    #         text = '운행 출발 확인 바랍니다'
    #         title = '운행 1시간 전입니다'

    #         # 추가: 운행 준비 상태인 경우 관리자에게 알림
    #         for driver_id in data_list:
    #             try:
    #                 # DispatchRegularlyConnect에서 driver_id로 배차 조회
    #                 dispatch = DispatchRegularlyConnect.objects.filter(driver_id=driver_id, departure_date=time2).first()
    #                 if dispatch and dispatch.status == "운행 준비":
    #                     admin_user = Member.objects.filter(role="관리자", use="사용")  
    #                     admin_text = f"기사 {dispatch.driver_id} 이(가) 아직 기상 확인 되지 않았습니다."
    #                     admin_title = "기상 확인 필요"
    #                     for admin in admin_user:
    #                         send_message(admin_title, admin_text, admin.token, None)

    #                 # DispatchOrderConnect에서 driver_id로 배차 조회
    #                 order_dispatch = DispatchOrderConnect.objects.filter(driver_id=driver_id, departure_date=time2).first()
    #                 if order_dispatch and order_dispatch.status == "운행 준비":
    #                     admin_user = Member.objects.filter(role="관리자", use="사용")  
    #                     admin_text = f"기사 {order_dispatch.driver_id} 이(가) 아직 기상 확인 되지 않았습니다."
    #                     admin_title = "기상 확인 필요"
    #                     for admin in admin_user:
    #                         send_message(admin_title, admin_text, admin.token, None)

    #             except Exception as e:
    #                 print(f"관리자 알림 에러: {e}")	

    #     if i == 2:
    #         data_list = set(data3 + data6)
    #         text = '첫 정류장 도착 확인 바랍니다'
    #         title = '운행 20분 전입니다'
            
    #     for user_id in data_list:
    #         user = Member.objects.get(id=user_id)
    #         token = user.token
    #         try:
    #             send_message(title, text, 'f4-nRN9ZO0K7lQ2VthFJd1:APA91bFxuYwFyny2eO3v8Mut61IrS2kxg-c4DoPeom4gMmgetwXxxh6U88isj8q3c7hlWWcEdE2I_sGQempBoyGLARCoZFyl3BAX3UHIGkpCw9qj2ELPkH8', None)
    #         except Exception as e:
    #             print(e)
    #         print("TOKEN ", user.name)
    # print("DATETIME : ", str(datetime.now())[:16])

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