from django.db import models
from crudmember.models import User

class DispatchConsumer(models.Model):
    name = models.CharField(verbose_name='주문자 이름', max_length=10, null=False)
    tel = models.IntegerField(verbose_name='전화번호', null=False)

    def __str__(self):
        return self.name

class DispatchOrder(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer", db_column="writer_id", null=True)
    order_consumer = models.ForeignKey(DispatchConsumer, on_delete=models.CASCADE, related_name="consumer", db_column="consumer_id", null=False)
    bus_cnt = models.IntegerField(verbose_name='버스 대수', null=False)
    price = models.IntegerField(verbose_name='가격', null=False)
    kinds = models.CharField(verbose_name='왕복or편도', max_length=2, null=False)
    purpose = models.CharField(verbose_name='용도', max_length=30, null=True)
    bus_type = models.CharField(verbose_name='버스종류', max_length=20, null=True)
    requirements = models.CharField(verbose_name='요구사항', max_length=100, null=True)
    people_num = models.IntegerField(verbose_name='탑승인원', null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    pay_type = models.CharField(verbose_name='카드or현금', max_length=2, null=False)
    
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self):
        return str(self.id)

class DispatchRoute(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="route_order", db_column="order_id", null=False)
    departure = models.CharField(verbose_name='출발지', max_length=50, null=False)
    departure_date = models.DateTimeField(verbose_name='출발시간', null=False)
    arrival = models.CharField(verbose_name='도착지', max_length=50, null=False)
    arrival_date = models.DateTimeField(verbose_name='도착시간', null=False)
    boarding_place = models.CharField(verbose_name='승차장소', max_length=50, null=True)

    def __str__(self):
        return str(self.order_id.id)

class DispatchInfo(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="info_order", db_column="order_id", null=False)
    #bus_id = models.ForeignKey(, on_delete=models.CASCADE, related_name="info_bus_id", db_column="bus_id", null=False)
    #drive_id = models.ForeignKey(, on_delete=models.CASCADE, related_name="info_driver_id", db_column="driver_id", null=False)
