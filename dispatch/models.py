from django.db import models
from enum import Enum
from typing import Optional
from crudmember.models import Category
from humanresource.models import Member
from vehicle.models import Vehicle
from datetime import datetime
from uuid import uuid4
from django.core.exceptions import BadRequest

from common.datetime import get_hour_minute

class ConnectStatus(str, Enum):
    BEFORE_DRIVE = "운행 전"
    PREPARE = "운행 준비"
    BOARDING = "탑승 및 운행 시작"
    DRIVE_LOG_START = "운행 일보 작성(출발)"
    FIRST_STOP = "첫 정류장 도착"
    DEPARTURE = "운행 출발"
    DRIVING = "운행 중"
    DRIVE_LOG_END = "운행 일보 작성(도착)"
    END = "운행 종료"
    COMPLETE = "운행 완료"

    @classmethod
    def choices(cls):
        return [(status.value, status.value) for status in cls]

    
    @classmethod
    def get_next_status(cls, current_status: str) -> Optional[str]:
        """
        현재 상태값(한글)을 받아서 다음 상태값(한글)을 반환합니다.
        마지막 상태인 경우 None을 반환합니다.

        Args:
            current_status (str): 현재 상태값 (예: "운행 전")

        Returns:
            Optional[str]: 다음 상태값 또는 None (마지막 상태인 경우)
        """
        try:
            # 현재 상태의 인덱스 찾기
            current_index = -1
            for i, status in enumerate(cls):
                if status.value == current_status:
                    current_index = i
                    break
            
            if current_index == -1:
                raise ValueError(f"Invalid status: {current_status}")
            
            # 다음 상태 반환
            if current_index < len(cls) - 1:
                status_list = list(cls)
                return status_list[current_index + 1].value
            return None
        except ValueError:
            raise ValueError(f"Invalid status: {current_status}")


class ConnectStatusFieldMapping:
    # 상태값과 시간 필드 매핑
    DRIVER_CHECK_STATUS_FIELD_MAP = {
        ConnectStatus.PREPARE: "wake_time",  # 1시간 30분 전
        ConnectStatus.BOARDING: "drive_time",  # 1시간 전
        ConnectStatus.FIRST_STOP: "departure_time",  # 20분 전
        ConnectStatus.DEPARTURE: "drive_start_time",  # 운행 출발
        ConnectStatus.END: "drive_end_time",  # 운행 종료
    }

class RouteTeam(models.Model):
    name = models.CharField(verbose_name='팀이름', max_length=100)
    team_leader = models.ForeignKey(Member, on_delete=models.SET_NULL, limit_choices_to={'role': '팀장'}, related_name='route_teams_leader', null=True, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="route", db_column="creator_id", null=True)
    
    def __str__(self):
        return f"{self.name}"

class BusinessEntity(models.Model):
    name = models.CharField(verbose_name='사업장 이름', max_length=50, null=False, unique=True)
    number = models.IntegerField(verbose_name='순번', null=False, default=999)
    regularly_groups = models.ManyToManyField('RegularlyGroup', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="business_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return self.name


class RegularlyGroup(models.Model):
    name = models.CharField(verbose_name='그룹 이름', max_length=50, null=False, unique=True)
    number = models.IntegerField(verbose_name='순번', null=False, default=999)
    fix = models.CharField(verbose_name='고정', max_length=1, null=False, default='n')
    settlement_date = models.CharField(verbose_name='정산일', max_length=5, null=False, default='1')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="group_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return str(self.number) + self.name

class DispatchRegularlyData(models.Model):
    def get_hour_minute(self):
        return get_hour_minute(int(self.time)) if self.time else ""

    group = models.ForeignKey(RegularlyGroup, verbose_name='그룹', related_name="regularly", on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(RouteTeam, verbose_name='팀', related_name="regularly", on_delete=models.SET_NULL, null=True)
    station = models.ManyToManyField("Station", related_name="regularly_data", through="DispatchRegularlyDataStation")
    references = models.CharField(verbose_name='참조사항', max_length=100, null=False, blank=True)
    departure = models.CharField(verbose_name='출발지', max_length=200, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=200, null=False)
    departure_time = models.CharField(verbose_name='출발시간', max_length=10, null=False)
    arrival_time = models.CharField(verbose_name='복귀시간', max_length=10, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=100, null=False, default=0)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=100, null=False, default=0)
    driver_allowance2 = models.CharField(verbose_name='기사수당(변경)', max_length=100, null=False, default=0)
    outsourcing_allowance = models.CharField(verbose_name='용역수당', max_length=100, null=False, default=0)
    number1 = models.CharField(verbose_name='순번1', max_length=100, null=False, default=0)
    number2 = models.CharField(verbose_name='순번2', max_length=100, null=False, default=0)
    num1 = models.IntegerField(verbose_name='순번1숫자만', null=True)
    num2 = models.IntegerField(verbose_name='순번2숫자만', null=True)
    week = models.CharField(verbose_name='운행요일', max_length=20, null=False)
    work_type = models.CharField(verbose_name='출/퇴근', max_length=2, null=False)
    route = models.CharField(verbose_name='노선이름', max_length=15, null=False)
    location = models.CharField(verbose_name='위치', max_length=100, null=False, blank=True)
    detailed_route = models.TextField(verbose_name='상세노선', null=False, blank=True)
    maplink = models.CharField(verbose_name='카카오맵', max_length=100, null=False, blank=True)
    use = models.CharField(verbose_name='사용여부', max_length=50, null=False, blank=True, default='사용')
    distance = models.CharField(verbose_name='거리', max_length=50, null=False, blank=True)
    time = models.CharField(verbose_name='운행시간(분)', max_length=50, null=False, blank=True)
    distance_list = models.CharField(verbose_name="정류장별 거리", max_length=500, null=False, blank=True)
    time_list = models.CharField(verbose_name="정류장별 시간", max_length=500, null=False, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_creator", db_column="creator_id", null=True)
    def __str__(self):
        return self.route

class DispatchRegularly(models.Model):
    def get_hour_minute(self):
        return get_hour_minute(int(self.time)) if self.time else ""
    
    regularly_id = models.ForeignKey(DispatchRegularlyData, verbose_name='정기배차 데이터', related_name="monthly", on_delete=models.SET_NULL, null=True)
    edit_date = models.CharField(verbose_name='수정기준일', max_length=50, null=False, blank=True)
    group = models.ForeignKey(RegularlyGroup, verbose_name='그룹', related_name="regularly_monthly", on_delete=models.SET_NULL, null=True)
    station = models.ManyToManyField("Station", related_name="regularly", through="DispatchRegularlyStation")
    references = models.CharField(verbose_name='참조사항', max_length=100, null=False, blank=True)
    departure = models.CharField(verbose_name='출발지', max_length=200, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=200, null=False)
    departure_time = models.CharField(verbose_name='출발시간', max_length=10, null=False)
    arrival_time = models.CharField(verbose_name='복귀시간', max_length=10, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=100, null=False, default=0)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=100, null=False, default=0)
    driver_allowance2 = models.CharField(verbose_name='기사수당(변경)', max_length=100, null=False, default=0)
    outsourcing_allowance = models.CharField(verbose_name='용역수당', max_length=100, null=False, default=0)
    number1 = models.CharField(verbose_name='순번1', max_length=100, null=False, default=0)
    number2 = models.CharField(verbose_name='순번2', max_length=100, null=False, default=0)
    num1 = models.IntegerField(verbose_name='순번1숫자만', null=True)
    num2 = models.IntegerField(verbose_name='순번2숫자만', null=True)
    week = models.CharField(verbose_name='운행요일', max_length=20, null=False)
    work_type = models.CharField(verbose_name='출/퇴근', max_length=2, null=False)
    route = models.CharField(verbose_name='노선이름', max_length=15, null=False)
    location = models.CharField(verbose_name='위치', max_length=100, null=False, blank=True)
    detailed_route = models.TextField(verbose_name='상세노선', null=False, blank=True)
    maplink = models.CharField(verbose_name='카카오맵', max_length=100, null=False, blank=True)
    use = models.CharField(verbose_name='사용여부', max_length=50, null=False, blank=True, default='사용')
    distance = models.CharField(verbose_name='거리', max_length=50, null=False, blank=True)
    time = models.CharField(verbose_name='운행시간(분)', max_length=50, null=False, blank=True)
    distance_list = models.CharField(verbose_name="정류장별 거리", max_length=500, null=False, blank=True)
    time_list = models.CharField(verbose_name="정류장별 시간", max_length=500, null=False, blank=True)
    
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_monthly_creator", db_column="creator_id", null=True)
    def __str__(self):
        return self.edit_date + ' ' + self.route

class DispatchRegularlyWaypoint(models.Model):
    regularly_id = models.ForeignKey(DispatchRegularlyData, verbose_name='정기배차 데이터', related_name="regularly_waypoint", on_delete=models.CASCADE, null=False)
    waypoint = models.CharField(verbose_name='경유지명', max_length=50, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_waypoint", db_column="creator_id", null=True)
    
    def __str__(self):
        return f'{self.regularly_id.route} {self.waypoint}'

class DispatchRegularlyRouteKnow(models.Model):
    regularly_id = models.ForeignKey(DispatchRegularlyData, related_name="regularly_route_know", on_delete=models.CASCADE, null=False)
    driver_id = models.ForeignKey(Member, related_name="regularly_route_know", on_delete=models.CASCADE, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_route_know_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return f'{self.regularly_id.route} {self.driver_id.name}'

class DispatchOrder(models.Model):
    def get_hour_minute(self):
        return get_hour_minute(int(self.time)) if self.time else ""
    
    departure = models.CharField(verbose_name='출발지', max_length=200, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=200, null=False)
    departure_date = models.CharField(verbose_name='출발날짜', max_length=20, null=False)
    arrival_date = models.CharField(verbose_name='복귀날짜', max_length=20, null=False)
    bus_cnt = models.CharField(verbose_name='차량대수', max_length=5, null=False)
    bus_type = models.CharField(verbose_name='차량종류', max_length=100, null=False, blank=True)
    customer = models.CharField(verbose_name='예약자', max_length=100, null=False)
    customer_phone = models.CharField(verbose_name='예약자 전화번호', max_length=100, null=False)
    contract_status = models.CharField(verbose_name='계약현황', max_length=100, null=False, blank=True)
    operation_type = models.CharField(verbose_name='왕복,편도,', max_length=100, null=False)
    reservation_company = models.CharField(verbose_name='예약회사', max_length=100, null=False, blank=True)
    operating_company = models.CharField(verbose_name='운행회사', max_length=100, null=False, blank=True)
    price = models.CharField(verbose_name='계약금액', max_length=30, null=False, default=0)
    driver_allowance = models.CharField(verbose_name='상여금', max_length=30, null=False, default=0)
    option = models.CharField(verbose_name='버스옵션', max_length=100, null=False, blank=True)
    cost_type = models.CharField(verbose_name='비용구분', max_length=100, null=False, blank=True)
    bill_place = models.CharField(verbose_name='계산서 발행처', max_length=100, null=False, blank=True)
    collection_type = models.CharField(verbose_name='수금구분', max_length=100, null=False, blank=True)
    payment_method = models.CharField(verbose_name='결제방법', max_length=100, null=False)
    VAT = models.CharField(verbose_name='VAT포함여부', max_length=1, null=False, default='n')
    total_price = models.CharField(verbose_name='VAT포함 금액', max_length=30, null=False, blank=True)
    ticketing_info = models.CharField(verbose_name='표찰정보', max_length=100, null=False, blank=True)
    order_type = models.CharField(verbose_name='유형', max_length=100, null=False, blank=True)
    references = models.CharField(verbose_name='참조사항', max_length=100, null=False, blank=True)
    driver_lease = models.CharField(verbose_name='인력임대차', max_length=100, null=False, blank=True)
    vehicle_lease = models.CharField(verbose_name='차량임대차', max_length=100, null=False, blank=True)
    route = models.CharField(verbose_name='노선이름', max_length=500, null=False)
    distance = models.CharField(verbose_name='거리', max_length=50, null=False, blank=True)
    time = models.CharField(verbose_name='운행시간(분)', max_length=50, null=False, blank=False, default="0")
    night_work_time = models.CharField(verbose_name='야간운행시간(분)', max_length=50, null=False, blank=False, default="0")
    distance_list = models.CharField(verbose_name="정류장별 거리", max_length=500, null=False, blank=True)
    time_list = models.CharField(verbose_name="정류장별 시간", max_length=500, null=False, blank=True)
    
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="dispatch_creator", db_column="creator_id", null=True)

    firebase_uid = models.CharField(verbose_name="파이어베이스 견적 uid", max_length=100, null=True)
    firebase_path = models.CharField(verbose_name="파이어베이스 견적 path", max_length=100, null=True)

    def __str__(self):
        return self.route

class DispatchOrderTour(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.SET_NULL, related_name="tour", null=True)
    firebase_uid = models.CharField(unique=True, verbose_name="파이어베이스 uid", max_length=100, null=False)
    price = models.CharField(verbose_name="가격", max_length=100, null=False)
    max_people = models.IntegerField(verbose_name="최대 인원수", null=False, default=45)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="작성시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="tour_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return f'{self.order_id.route}'

class DispatchOrderTourCustomer(models.Model):
    tour_id = models.ForeignKey(DispatchOrderTour, on_delete=models.CASCADE, related_name="tour_customer", null=False)
    user_uid = models.CharField(verbose_name="파이어베이스 유저 uid", max_length=100, null=False, blank=True)
    name = models.CharField(verbose_name="이름", max_length=100, null=False)
    phone = models.CharField(verbose_name="전화번호", max_length=100, null=False)
    bank = models.CharField(verbose_name="은행", max_length=100, null=False)
    pay_datetime = models.CharField(verbose_name="결제시간", max_length=100, null=False, blank=True)
    payment_status = models.CharField(verbose_name="결제현황", max_length=100, null=False, default="결제대기")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="tour_customer_creator", db_column="creator_id", null=True)

    def __str__(self):
        return f'{self.tour_id.__str__()} {self.name}'

class DispatchOrderStation(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="station", db_column="order_id", null=False)
    station_name = models.CharField(verbose_name='경유지명', max_length=100, null=False)
    place_name = models.CharField(verbose_name='장소이름', max_length=100, null=False, blank=True)
    address = models.CharField(verbose_name='경유지 주소', max_length=100, null=False, blank=True)
    longitude = models.CharField(verbose_name='경도 x', max_length=100, null=False, blank=True)
    latitude = models.CharField(verbose_name='위도 y', max_length=100, null=False, blank=True)
    time = models.CharField(verbose_name='시간', max_length=5, null=False, blank=True)
    delegate = models.CharField(verbose_name='인솔자', max_length=100, null=False, blank=True)
    delegate_phone = models.CharField(verbose_name='인솔자 전화번호', max_length=100, null=False, blank=True)
    
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="order_station_creator", db_column="creator_id", null=True)

class DispatchOrderConnect(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="info_order", db_column="order_id", null=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="info_bus_id", db_column="bus_id", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="info_driver_id", db_column="driver_id", null=True)
    outsourcing = models.CharField(verbose_name='용역', max_length=1, null=False, default='n')
    departure_date = models.CharField(verbose_name='출발날짜', max_length=16, null=False)
    arrival_date = models.CharField(verbose_name='도착날짜', max_length=16, null=False)
    work_type = models.CharField(verbose_name='일반', max_length=2, null=False, default='일반')
    price = models.CharField(verbose_name='계약금액', max_length=40, null=False)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=40, null=False)
    payment_method = models.CharField(verbose_name='상여금 선지급', max_length=1, null=False, default="n")
    status = models.CharField(verbose_name='운행상태', max_length=100, null=False, default="운행 전", choices=ConnectStatus.choices())
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="connect_creator", db_column="creator_id", null=True)
    def __str__(self):
        return f'{self.order_id.route} / {self.departure_date[2:10]}'

class DispatchRegularlyConnect(models.Model):
    regularly_id = models.ForeignKey(DispatchRegularly, on_delete=models.CASCADE, related_name="info_regularly", db_column="order_id", null=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="info_regularly_bus_id", db_column="bus_id", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="info_regularly_driver_id", db_column="driver_id", null=True)
    outsourcing = models.CharField(verbose_name='용역', max_length=1, null=False, default='n')
    departure_date = models.CharField(verbose_name='출발날짜', max_length=16, null=False)
    arrival_date = models.CharField(verbose_name='도착날짜', max_length=16, null=False)
    work_type = models.CharField(verbose_name='출/퇴근', max_length=2, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=10, null=False)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=10, null=False)
    time = models.CharField(verbose_name='시간', max_length=100, null=False, blank=True)
    distance = models.CharField(verbose_name='거리', max_length=100, null=False, blank=True)
    status = models.CharField(verbose_name='운행상태', max_length=100, null=False, default="운행 전", choices=ConnectStatus.choices())
    locations = models.JSONField(verbose_name="운행 경로", null=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="connect_regularly_creator", db_column="creator_id", null=True)
    def __str__(self):
        return f'{self.work_type} {self.regularly_id} / {self.departure_date[2:10]}'

class DispatchCheck(models.Model):
    date = models.CharField(verbose_name='날짜', max_length=20, null=False)
    # dispatch_check = models.CharField(verbose_name='확인완료', max_length=1, null=False, default='n')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="dispatch_check_creator", db_column="creator_id", null=True)

    def __str__(self):
        return self.date

class Schedule(models.Model):
    date = models.CharField(verbose_name='날짜', max_length=10, null=False)
    content = models.CharField(verbose_name='내용', max_length=250, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="schedule_creator", db_column="creator_id", null=True)

    def __str__(self):
        return self.date + '' + self.content

# Connect 생성될 때 signals에서 DriverCheck 생성
class DriverCheck(models.Model):
    regularly_id = models.OneToOneField(DispatchRegularlyConnect, on_delete=models.CASCADE, related_name="check_regularly_connect", null=True)
    order_id = models.OneToOneField(DispatchOrderConnect, on_delete=models.CASCADE, related_name="check_order_connect", null=True)
    wake_time = models.CharField(verbose_name='기상확인시간(1시간 30분 전)', max_length=16, null=False, blank=True)
    drive_time = models.CharField(verbose_name='운행시작시간(1시간 전)', max_length=16, null=False, blank=True)
    departure_time = models.CharField(verbose_name='출발지도착시간(20분 전)', max_length=16, null=False, blank=True)
    drive_start_time = models.CharField(verbose_name='운행 출발', max_length=16, null=False, blank=True)
    drive_end_time = models.CharField(verbose_name='운행 종료', max_length=16, null=False, blank=True)
    
    connect_check = models.CharField(verbose_name='배차확인여부', max_length=1, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="driver_check_creator", db_column="creator_id", null=True)

# 정류장 도착 버튼 클릭으로 입력된 시간 (출퇴근만)
class StationArrivalTime(models.Model):
    regularly_connect_id = models.ForeignKey(DispatchRegularlyConnect, on_delete=models.CASCADE, related_name="station_arrival_time", null=False)
    station_id = models.ForeignKey('DispatchRegularlyStation', on_delete=models.CASCADE, related_name="station_arrival_time", null=False)
    arrival_time = models.CharField(verbose_name="정류장 도착 시각", max_length=100, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="station_arrival_time_crator", db_column="creator_id", null=True)

class ConnectRefusal(models.Model):
    def get_file_path():
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['dispatch/refusal', ymd_path, uuid_name])

    regularly_id = models.OneToOneField(DispatchRegularlyConnect, on_delete=models.SET_NULL, related_name="refusal_regularly_connect", null=True)
    order_id = models.OneToOneField(DispatchOrderConnect, on_delete=models.SET_NULL, related_name="refusal_order_connect", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="refusal_driver_id", null=False)
    departure_date = models.CharField(verbose_name='출발시간', max_length=16, null=False, blank=True)
    arrival_date = models.CharField(verbose_name='도착시간', max_length=16, null=False, blank=True)
    route = models.CharField(verbose_name='노선이름', max_length=500, null=False, blank=True)
    check_date = models.CharField(verbose_name='확인날짜', max_length=16, null=False, blank=True)
    refusal = models.CharField(verbose_name='배차거부사유', max_length=500, null=False, blank=True)
    files = models.TextField(verbose_name='증빙서류', null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="connect_refusal_creator", db_column="creator_id", null=True)

class MorningChecklist(models.Model):
    def get_vehicle_list(self):
        order_bus = list(DispatchOrderConnect.objects.filter(departure_date__startswith=self.date[:10]).filter(driver_id=self.member).values_list('bus_id__vehicle_num'))
        regularly_bus = list(DispatchRegularlyConnect.objects.filter(departure_date__startswith=self.date[:10]).filter(driver_id=self.member).values_list('bus_id__vehicle_num'))
        result = []
        for i in order_bus:
            result.append(i[0])
        for i in regularly_bus:
            result.append(i[0])
        result = set(result)
        return list(result)

    submit_check = models.BooleanField(verbose_name="제출여부", null=False, default=False)
    submit_time = models.CharField(verbose_name="제출시간", max_length=10, blank=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="morning_checklist_member", null=True)
    date = models.CharField(verbose_name="날짜", max_length=100, null=False, blank=False)
    arrival_time = models.CharField(verbose_name="점호지 도착시간", max_length=100, null=False, blank=True)
    garage_location = models.CharField(verbose_name="차고지", max_length=100, null=False, blank=True)
    health_condition = models.CharField(verbose_name="건강상태", max_length=100, null=False, blank=True)
    cleanliness_condition = models.CharField(verbose_name="청소상태", max_length=100, null=False, blank=True)
    route_familiarity = models.CharField(verbose_name="노선숙지", max_length=100, null=False, blank=True)
    alcohol_test = models.CharField(verbose_name="음주측정", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="morning_checklist_creator", db_column="creator_id", null=True)

class EveningChecklist(models.Model):
    STATUS_TYPE_CHOCIES = [
        '배차 확인',
        '퇴근'
    ]

    def get_vehicle(self):
        order_bus = DispatchOrderConnect.objects.filter(departure_date__startswith=self.date[:10]).filter(driver_id=self.member).order_by('arrival_date').last()
        regularly_bus = DispatchRegularlyConnect.objects.filter(departure_date__startswith=self.date[:10]).filter(driver_id=self.member).order_by('arrival_date').last()
        if not (order_bus and regularly_bus):
            return ""
        if order_bus.arrival_date > regularly_bus.arrival_date or not regularly_bus:
            return order_bus.bus_id.vehicle_num
        return regularly_bus.bus_id.vehicle_num
    
    submit_check = models.BooleanField(verbose_name="제출여부", null=False, default=False)
    checklist_submit_time = models.CharField(verbose_name="제출시간", max_length=10, blank=True)
    tomorrow_check_submit_time = models.CharField(verbose_name="내일 배차 확인시간", max_length=10, blank=True)
    get_off_submit_time = models.CharField(verbose_name="퇴근시간", max_length=10, blank=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="evening_checklist_member", null=True)
    date = models.CharField(verbose_name="날짜", max_length=100, null=False, blank=False)
    garage_location = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="garage_location", verbose_name="차고지", null=True)
    battery_condition = models.CharField(verbose_name="메인스위치(배터리)", max_length=100, null=False, blank=True)
    drive_distance = models.CharField(verbose_name="운행거리", max_length=100, null=False, blank=True)
    fuel_quantity = models.CharField(verbose_name="주유량", max_length=100, null=False, blank=True)
    urea_solution_quantity = models.CharField(verbose_name="요소수량", max_length=100, null=False, blank=True)
    suit_gauge = models.CharField(verbose_name="수트게이지", max_length=100, null=False, blank=True)
    special_notes = models.CharField(verbose_name="특이사항", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="evening_checklist_creator", db_column="creator_id", null=True)

# Connect 생성될 때 signals에서 DrivingHistory 생성
class DrivingHistory(models.Model):
    def get_connect_data(self):
        if self.order_connect_id:
            connect = self.order_connect_id
            order = connect.order_id
            work_type = '일반'
        elif self.regularly_connect_id:
            connect = self.regularly_connect_id
            order = connect.regularly_id
            work_type = order.work_type
        else:
            return {}
        return {
            "bus" : connect.bus_id.vehicle_num,
            'departure' : order.departure,
            'arrival' : order.arrival,
            'departure_date' : connect.departure_date,
            'arrival_date' : connect.arrival_date,
            'work_type': work_type,

        }

    submit_check = models.BooleanField(verbose_name="제출여부", null=False, default=False)
    submit_time = models.CharField(verbose_name="제출시간", max_length=10, blank=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="driving_history_member", null=True)
    date = models.CharField(verbose_name="날짜", max_length=100, null=False, blank=True)
    regularly_connect_id = models.OneToOneField(DispatchRegularlyConnect, on_delete=models.CASCADE, related_name="driving_history_regularly", null=True)
    order_connect_id = models.OneToOneField(DispatchOrderConnect, on_delete=models.CASCADE, related_name="driving_history_order", null=True)
    departure_km = models.CharField(verbose_name="출발계기km", max_length=100, null=False, blank=True)
    arrival_km = models.CharField(verbose_name="도착계기km", max_length=100, null=False, blank=True)
    passenger_num = models.CharField(verbose_name="탑승인원수", max_length=100, null=False, blank=True)
    special_notes = models.CharField(verbose_name="특이사항", max_length=100, null=False, blank=True)
    departure_date = models.CharField(verbose_name="출발날짜", max_length=100, null=False, blank=True)
    arrival_date = models.CharField(verbose_name="도착날짜", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="driving_history_creator", db_column="creator_id", null=True)

class Station(models.Model):
    TYPES_CHOICES = [
        '차고지',
        '첫 정류장 대기장소',
        '정류장',
        '사업장',
        '대기장소',
        '마지막 정류장',
    ]

    def set_types(self, type_list):
        for type in type_list:
            if not type in self.TYPES_CHOICES:
                raise BadRequest('정류장 종류의 값이 올바르지 않습니다.')
        self.station_type = ', '.join(type_list)

    def get_types(self):
        return self.station_type.split(', ') if self.station_type else None

    name = models.CharField(verbose_name="정류장명", max_length=100, null=False)
    address = models.CharField(verbose_name="주소", max_length=100, null=False)
    latitude = models.CharField(verbose_name="위도", max_length=100, null=False)
    longitude = models.CharField(verbose_name="경도", max_length=100, null=False)
    references = models.CharField(verbose_name="참조사항", max_length=100, null=False, blank=True)
    station_type = models.CharField(verbose_name="종류", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="station_creator", db_column="creator_id", null=True)

class DispatchRegularlyDataStation(models.Model):
    regularly_data = models.ForeignKey(DispatchRegularlyData, on_delete=models.CASCADE, related_name="regularly_data_station", null=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="station_regularly_data", null=False)
    index = models.IntegerField(verbose_name='순번')
    station_type = models.CharField(verbose_name="종류", max_length=100, null=False)
    time = models.CharField(verbose_name="시각", max_length=100, null=False)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_data_station_creator", db_column="creator_id", null=True)

    def __str__(self):
        return f'{self.regularly_data.route} {self.station.name} {self.index} {self.station_type} {self.time}'
    
class DispatchRegularlyStation(models.Model):
    regularly = models.ForeignKey(DispatchRegularly, on_delete=models.CASCADE, related_name="regularly_station", null=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="station_regularly", null=False)
    index = models.IntegerField(verbose_name='순번')
    station_type = models.CharField(verbose_name="종류", max_length=100, null=False)
    time = models.CharField(verbose_name="시각", max_length=100, null=False)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_station_creator", db_column="creator_id", null=True)
    # def __str__(self):
    #     return f'{self.regularly.route} {self.station.name} {self.index} {self.station_type} {self.time}'

