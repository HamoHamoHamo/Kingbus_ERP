from .models import *
from datetime import datetime, timedelta
from config.settings.base import TODAY, FORMAT
from config.custom_logging import logger
from django.db.models import Q
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