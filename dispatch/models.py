from django.db import models
from crudmember.models import User
from humanresource.models import Member
from vehicle.models import Vehicle

class DispatchConsumer(models.Model):
    name = models.CharField(verbose_name='주문자 이름', max_length=10, null=False)
    tel = models.CharField(verbose_name='전화번호', max_length=15, null=False)
    
    def __str__(self):
        return self.name

class RegularlyGroup(models.Model):
    name = models.CharField(verbose_name='그룹 이름', max_length=30, null=False)
    company = models.CharField(verbose_name='거래처', max_length=20, null=False, blank=True)

    def __str__(self):
        return self.name

class DispatchOrder(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dispatch_creator", db_column="creator_id", null=True)
    consumer = models.ForeignKey(DispatchConsumer, on_delete=models.SET_NULL, related_name="consumer", db_column="consumer_id", null=True)
    bus_cnt = models.IntegerField(verbose_name='버스 대수', null=False)
    price = models.IntegerField(verbose_name='가격', null=False)
    driver_allowance = models.IntegerField(verbose_name='기사수당', null=True)
    kinds = models.CharField(verbose_name='왕복or편도', max_length=2, null=False)
    purpose = models.CharField(verbose_name='용도', max_length=30, blank=True)
    bus_type = models.CharField(verbose_name='버스종류', max_length=20, blank=True)
    requirements = models.CharField(verbose_name='요구사항', max_length=100, blank=True)
    #people_num = models.IntegerField(verbose_name='탑승인원', null=False)
    #pay_type = models.CharField(verbose_name='카드or현금', max_length=2, null=False)
    departure = models.CharField(verbose_name='출발지', max_length=50, null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=50, null=False)
    stopover = models.CharField(verbose_name='경유지', max_length=100, null=False, blank=True)
    route_name = models.CharField(verbose_name="노선명", max_length=50, null=False, blank=True)
    regularly_group = models.ForeignKey(RegularlyGroup, on_delete=models.SET_NULL, related_name="regularly_route", db_column="group_id", null=True, blank=True)
    departure_date = models.CharField(verbose_name='출발시간', max_length=16, null=False)
    arrival_date = models.CharField(verbose_name='도착시간', max_length=16, null=False)
    check = models.BooleanField(verbose_name="배차완료", null=False, default=False)
    regularly = models.BooleanField(verbose_name="정기배차", null=False, default=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    
    def __str__(self):
        return self.departure_date

class DispatchConnect(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="connect_creator", db_column="creator_id", null=True)
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="info_order", db_column="order_id", null=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="info_bus_id", db_column="bus_id", null=True)
    driver_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="info_driver_id", db_column="driver_id", null=True)