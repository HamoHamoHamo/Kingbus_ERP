from django.db import models
from django.db.models.deletion import SET_NULL
from crudmember.models import User
from humanresource.models import Member
from vehicle.models import Vehicle

class RegularlyGroup(models.Model):
    name = models.CharField(verbose_name='그룹 이름', max_length=30, null=False)
    company = models.CharField(verbose_name='거래처', max_length=20, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(User, on_delete=SET_NULL, related_name="group_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return self.name

class RegularlyOrder(models.Model):
    week = models.CharField(verbose_name='운행요일', max_length=7, null=False)
    term_begin = models.CharField(verbose_name='계약시작일', max_length=10, null=False, blank=True)
    term_end = models.CharField(verbose_name='계약종료일', max_length=10, null=False, blank=True)
    regularly_group = models.ForeignKey(RegularlyGroup, verbose_name="그룹", on_delete=SET_NULL, related_name="regularly_info", null=True)
    
    def __str__(self):
        return self.order_info.all()[0].route_name

class DispatchOrder(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    bus_cnt = models.IntegerField(verbose_name='버스 대수', null=False)
    price = models.IntegerField(verbose_name='가격', null=False)
    driver_allowance = models.IntegerField(verbose_name='기사수당', null=True, blank=True)
    way = models.CharField(verbose_name='왕복or편도', max_length=2, null=False)
    purpose = models.CharField(verbose_name='용도', max_length=30, blank=True)
    bus_type = models.CharField(verbose_name='버스종류', max_length=20, blank=True)
    reference = models.CharField(verbose_name='참조사항', max_length=100, blank=True)
    #people_num = models.IntegerField(verbose_name='탑승인원', null=False)
    #pay_type = models.CharField(verbose_name='카드or현금', max_length=2, null=False)
    departure = models.CharField(verbose_name='출발지', max_length=50, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=50, null=False)
    stopover = models.CharField(verbose_name='경유지', max_length=100, null=False, blank=True)
    route_name = models.CharField(verbose_name="노선명", max_length=50, null=False, blank=True)
    #regularly_group = models.ForeignKey(RegularlyGroup, verbose_name='그룹', on_delete=models.SET_NULL, related_name="regularly_route", db_column="group_id", null=True, blank=True)
    departure_date = models.CharField(verbose_name='출발시간', max_length=16, null=False, blank=True)
    arrival_date = models.CharField(verbose_name='도착시간', max_length=16, null=False, blank=True)
    regularly = models.ForeignKey(RegularlyOrder, verbose_name="정기배차", null=True, on_delete=models.CASCADE, related_name="order_info",)
    customer = models.CharField(verbose_name='주문자 이름', max_length=10, null=False)
    customer_tel = models.CharField(verbose_name='전화번호', max_length=15, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dispatch_creator", db_column="creator_id", null=True)

    def __str__(self):
        return self.departure

class DispatchConnect(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="info_order", db_column="order_id", null=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="info_bus_id", db_column="bus_id", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="info_driver_id", db_column="driver_id", null=True)
    departure_date = models.CharField(verbose_name='출발날짜', max_length=16, null=False)
    arrival_date = models.CharField(verbose_name='도착날짜', max_length=16, null=False)
    group = models.CharField(verbose_name='그룹이름', max_length=30, null=True, default="")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(User, on_delete=SET_NULL, related_name="connect_creator", db_column="creator_id", null=True)