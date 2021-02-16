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

