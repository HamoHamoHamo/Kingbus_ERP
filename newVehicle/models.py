from django.db import models
from django.apps import apps
from humanresource.models import Member
# Create your models here.

class Vehicle(models.Model):
    vehicle_number_front = models.CharField(max_length=20, verbose_name='차량번호앞', null=False)  # 차량번호앞
    vehicle_number_back = models.CharField(max_length=20, verbose_name='차량번호뒤', null=False)  # 차량번호뒤
    maker = models.CharField(max_length=50, verbose_name='제조사', null=False)  # 제조사
    vehicle_name = models.CharField(max_length=20, verbose_name='차량이름', null=False)  # 차량종류
    driver = models.OneToOneField(Member, verbose_name='기사', on_delete=models.SET_NULL, null=True, related_name="vehicle", db_column="vehicle") #담당기사
    vehicle_serial = models.CharField(max_length=50, verbose_name='제조사', null=False)  # 차대번호
    passenger_capacity = models.IntegerField(verbose_name='승차인원', null=False)  # 승차인원
    type = models.CharField(verbose_name='형식', max_length=100, null=False, blank=True) #형식
    model_year = models.IntegerField(verbose_name='모델연도')  # 모델연도
    fuel_type = models.CharField(max_length=20, verbose_name='원동기형식')  # 원동기형식
    registration_date = models.DateField(verbose_name='정기점검일')  # 정기점검일
    in_use = models.BooleanField(verbose_name='사용여부')  # 사용여부
    remark = models.TextField(verbose_name='비고', null=True, blank=True)  # 비고



class VehiclePrice(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)  # 차량과의 일대일 관계
    vehicle_price = models.IntegerField(verbose_name='차량가격')  # 차량가격
    depreciation_month = models.IntegerField(verbose_name='감가상각(월)')  # 감가상각(월)
    depreciation_year = models.IntegerField(verbose_name='감가상각 기준 연도')  # 감가상각 기준 연도
    insurance_pay_date = models.DateField(verbose_name='보험납부일')  # 보험납부일
    insurance_price = models.IntegerField(verbose_name='보험비')  # 보험비
    monthly_installment = models.IntegerField(verbose_name='할부금액(월)')  # 할부금액(월)
    remaining_installment_amount = models.IntegerField(verbose_name='남은 할부액')  # 남은 할부액

class vehicleOption(models.Model):
    led = models.BooleanField(verbose_name='전광판유무')
    cold = models.BooleanField(verbose_name='냉장고유무')
    sing = models.BooleanField(verbose_name='노래방유무')
    usb = models.BooleanField(verbose_name='USB 유무')
    hot = models.BooleanField(verbose_name='온수기유무')
    tv = models.BooleanField(verbose_name='tv유무')