from django.db import models
from crudmember.models import User
from humanresource.models import Member
from datetime import datetime
from uuid import uuid4

class Vehicle(models.Model):
    vehicle_num = models.CharField(verbose_name='차량번호', max_length=15, null=False)
    vehicle_id = models.CharField(verbose_name='차대번호', max_length=20, null=False)
    motor_type = models.CharField(verbose_name='원동기형식', max_length=30, null=False, blank=True)
    rated_output = models.CharField(verbose_name='정격출력', max_length=15, null=False, blank=True)
    vehicle_type = models.CharField(verbose_name='차량종류', max_length=15, null=False)
    maker = models.CharField(verbose_name='제조사', max_length=15, null=False)
    model_year = models.CharField(verbose_name='연식', max_length=15, null=False)
    release_date = models.CharField(verbose_name='출고일자', max_length=15, null=False)
    driver = models.ForeignKey(Member, verbose_name='기사', on_delete=models.SET_NULL, null=True, related_name="driver", db_column="driver")
    use = models.CharField(verbose_name='사용여부', max_length=10, null=False)
    passenger_num = models.IntegerField(verbose_name='승차인원', null=False)

    check_duration = models.CharField(verbose_name='정기점검정비기록', max_length=30, null=False, blank=True)
    inspection_duration = models.CharField(verbose_name='검사유효기간', max_length=30, null=False, blank=True)
    # vehicle_registration = models.CharField(verbose_name='차량등록증', max_length=30, null=False, blank=True)
    # insurance_receipt = models.CharField(verbose_name='보험영수증', max_length=30, null=False, blank=True)

class VehicleDocument(models.Model):
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['vehicle/', ymd_path, uuid_name])

    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE,related_name="vehicle_file", db_column="vehicle_id", null=False)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')
    # 보험영수증, 차량등록증 저장
    type = models.CharField(max_length=30, null=True, verbose_name='종류')

    def __str__(self):
        return self.vehicle_id