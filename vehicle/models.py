from django.db import models
from crudmember.models import User
from humanresource.models import Member

class Vehicle(models.Model):
    vehicle_num = models.CharField(verbose_name='차량번호', max_length=15, null=False)
    group = models.CharField(verbose_name='소속', max_length=15, null=False)
    vehicle_type = models.CharField(verbose_name='차량종류', max_length=15, null=False)
    maker = models.CharField(verbose_name='제조사', max_length=15, null=False)
    model_year = models.CharField(verbose_name='연식', max_length=15, null=False)
    driver = models.ForeignKey(Member, verbose_name='기사', on_delete=models.SET_NULL, null=True, related_name="driver", db_column="driver")
    use = models.BooleanField(verbose_name='사용여부', default=False)
    passenger_num = models.IntegerField(verbose_name='승차인원', null=False)

    def __str__(self):
        return self.vehicle_num

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'vehicle'

class VehicleInsurance(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column="vehicle_id", null=False)
    insurance_date = models.CharField(max_length=10, null=False, verbose_name='보험일자')
    insurance_price = models.CharField(verbose_name='금액', max_length=20, null=False)
    insurance_comp = models.CharField(verbose_name='보험회사', max_length=50, null=False)
    expiration_date = models.CharField(max_length=10, null=False, verbose_name='만료일자')
    
    def __str__(self):
        return self.vehicle_id
    
    class Meta:
        db_table = 'vehicle_insurance'

class VehicleCheck(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column="vehicle_id", null=False)
    check_date = models.CharField(verbose_name='점검날짜', max_length=50, null=False)
    check_detail = models.CharField(verbose_name='점검내용', max_length=500, null=False)
    
    def __str__(self):
        return self.check_date
    
    class Meta:
        db_table = 'vehicle_check'
    
class VehicleDocument(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column="vehicle_id", null=False)
    vehicle_file = models.FileField(upload_to='vehicle/', blank=True, null=True)
    check_id = models.ForeignKey(VehicleCheck, on_delete=models.CASCADE, db_column="check_id", null=True)
    
    def __str__(self):
        return self.vehicle_id
    
    class Meta:
        db_table = 'vehicle_document'
