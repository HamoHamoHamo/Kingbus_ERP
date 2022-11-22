from django.db import models
from humanresource.models import Member
from vehicle.models import Vehicle
import re

class RegularlyGroup(models.Model):
    name = models.CharField(verbose_name='그룹 이름', max_length=30, null=False, unique=True)
    number = models.IntegerField(verbose_name='순번', null=False, default=999 )
    fix = models.CharField(verbose_name='고정', max_length=1, null=False, default='n')
    settlement_date = models.CharField(verbose_name='정산일', max_length=5, null=False, default='1')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="group_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return str(self.number) + self.name

class DispatchRegularly(models.Model):
    group = models.ForeignKey(RegularlyGroup, verbose_name='그룹', related_name="regularly_info", on_delete=models.SET_NULL, null=True)
    references = models.CharField(verbose_name='참조사항', max_length=200, null=False, blank=True)
    departure = models.CharField(verbose_name='출발지', max_length=200, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=200, null=False)
    departure_time = models.CharField(verbose_name='출발시간', max_length=10, null=False)
    arrival_time = models.CharField(verbose_name='복귀시간', max_length=10, null=False)
    # bus_type = models.CharField(verbose_name='버스종류', max_length=30, null=False, blank=True)
    # bus_cnt = models.CharField(verbose_name='버스대수', max_length=3, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=40, null=False, default=0)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=40, null=False, default=0)
    number1 = models.CharField(verbose_name='순번1', max_length=20, null=False, blank=True)
    number2 = models.CharField(verbose_name='순번2', max_length=20, null=False, blank=True)
    num1 = models.IntegerField(verbose_name='순번1숫자만', null=True)
    num2 = models.IntegerField(verbose_name='순번2숫자만', null=True)
    week = models.CharField(verbose_name='운행요일', max_length=20, null=False)
    # customer = models.CharField(verbose_name='예약자', max_length=20, null=False, blank=True)
    # customer_phone = models.CharField(verbose_name='예약자 전화번호', max_length=20, null=False, blank=True)
    # contract_start_date = models.CharField(verbose_name='계약시작일', max_length=10, null=False, blank=True)
    # contract_end_date = models.CharField(verbose_name='계약종료일', max_length=10, null=False, blank=True)
    work_type = models.CharField(verbose_name='출/퇴근', max_length=2, null=False)
    route = models.CharField(verbose_name='노선이름', max_length=200, null=False)
    location = models.CharField(verbose_name='위치', max_length=200, null=False, blank=True)
    detailed_route = models.CharField(verbose_name='상세노선', max_length=200, null=False, blank=True)
    
    # bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="regulary_bus_id", null=True)
    # driver_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_driver_id", null=True)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="regularly_creator", db_column="creator_id", null=True)
    def __str__(self):
        return self.route
    
# class DispatchRegularlyFixed(models.Model):
#     regularly_id = models.ForeignKey(DispatchRegularly, on_delete=models.CASCADE, related_name="info_regularly_fixed", db_column="order_id", null=False)
#     bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="info_regularly_fixed_bus_id", db_column="bus_id", null=True)
#     driver_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="info_regularly_fixed_driver_id", db_column="driver_id", null=True)
#     week = models.CharField(verbose_name='운행요일', max_length=20, null=False)

#     def __str__(self):
#         return self.regularly_id.route + ' / ' + self.bus_id.vehicle_num + self.driver_id.name

class DispatchOrder(models.Model):
    operation_type = models.CharField(verbose_name='왕복,편도,', max_length=10, null=False, blank=True)
    references = models.CharField(verbose_name='참조사항', max_length=200, null=False, blank=True)
    departure = models.CharField(verbose_name='출발지', max_length=200, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=200, null=False)
    departure_date = models.CharField(verbose_name='출발날짜', max_length=20, null=False)
    arrival_date = models.CharField(verbose_name='복귀날짜', max_length=20, null=False)
    bus_type = models.CharField(verbose_name='버스종류', max_length=30, null=False, blank=True)
    bus_cnt = models.CharField(verbose_name='버스대수', max_length=5, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=40, null=False, default=0)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=40, null=False, default=0)
    contract_status = models.CharField(verbose_name='계약현황', max_length=100, null=False, blank=True)
    cost_type = models.CharField(verbose_name='비용구분', max_length=100, null=False, blank=True)
    customer = models.CharField(verbose_name='예약자', max_length=100, null=False, blank=True)
    customer_phone = models.CharField(verbose_name='예약자 전화번호', max_length=100, null=False, blank=True)
    deposit_status = models.CharField(verbose_name='입금현황', max_length=50, null=False, blank=True)
    bill_place = models.CharField(verbose_name='계산서 발행처', max_length=50, null=False, blank=True)
    bill_date = models.CharField(verbose_name='계산서 발행일', max_length=10, null=False, blank=True)
    collection_type = models.CharField(verbose_name='수금구분', max_length=50, null=False, blank=True)
    VAT = models.CharField(verbose_name='VAT포함여부', max_length=1, null=False, default='n')
    total_price = models.CharField(verbose_name='VAT포함 금액', max_length=30, null=False, blank=True)
    option = models.CharField(verbose_name='버스옵션', max_length=50, null=False, blank=True)
    route = models.CharField(verbose_name='노선이름', max_length=200, null=False)
    ticketing_info = models.CharField(verbose_name='표찰정보', max_length=200, null=False, blank=True)
    order_type = models.CharField(verbose_name='유형', max_length=50, null=False, blank=True, default='기타')
    payment_method = models.CharField(verbose_name='결제방법', max_length=50, null=False, blank=True)
    # collection_amount = models.CharField(verbose_name='수금금액', max_length=30, null=False, default='0')
    # collection_date = models.CharField(verbose_name='수금날짜', max_length=10, null=False, blank=True)
    # collection_creator = models.CharField(verbose_name='수금입력자', max_length=50, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="dispatch_creator", db_column="creator_id", null=True)
    def __str__(self):
        return self.route
        
class DispatchOrderWaypoint(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="waypoint", db_column="order_id", null=False)
    waypoint = models.CharField(verbose_name='경유지', max_length=100, null=False)
    time = models.CharField(verbose_name='시간', max_length=5, null=False, blank=True)
    delegate = models.CharField(verbose_name='인솔자', max_length=50, null=False, blank=True)
    delegate_phone = models.CharField(verbose_name='인솔자 전화번호', max_length=50, null=False, blank=True)
    
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="waypoint_creator", db_column="creator_id", null=True)

class DispatchOrderConnect(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="info_order", db_column="order_id", null=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="info_bus_id", db_column="bus_id", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="info_driver_id", db_column="driver_id", null=True)
    outsourcing = models.CharField(verbose_name='용역', max_length=1, null=False, default='n')
    departure_date = models.CharField(verbose_name='출발날짜', max_length=16, null=False)
    arrival_date = models.CharField(verbose_name='도착날짜', max_length=16, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=40, null=False)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=40, null=False)
    payment_method = models.CharField(verbose_name='상여금 선지급', max_length=1, null=False, default="n")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="connect_creator", db_column="creator_id", null=True)
    def __str__(self):
        return f'{self.order_id.route} / {self.departure_date[2:10]}'

class DispatchRegularlyConnect(models.Model):
    regularly_id = models.ForeignKey(DispatchRegularly, on_delete=models.CASCADE, related_name="info_regularly", db_column="order_id", null=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="info_regularly_bus_id", db_column="bus_id", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="info_regularly_driver_id", db_column="driver_id", null=True)
    outsourcing = models.CharField(verbose_name='용역', max_length=1, null=False, default='n')
    departure_date = models.CharField(verbose_name='출발날짜', max_length=16, null=False)
    arrival_date = models.CharField(verbose_name='도착날짜', max_length=16, null=False)
    work_type = models.CharField(verbose_name='출/퇴근', max_length=2, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=10, null=False)
    driver_allowance = models.CharField(verbose_name='기사수당', max_length=10, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="connect_regularly_creator", db_column="creator_id", null=True)
    def __str__(self):
        return f'{self.regularly_id.route} / {self.departure_date[2:10]}'
        
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
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="schedule_creator", db_column="creator_id", null=True)

    def __str__(self):
        return self.date + '' + self.content
