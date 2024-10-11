from django.db import models
from humanresource.models import Member
# Create your models here.

class Vehicle(models.Model):

    vehicle_number_front = models.CharField(max_length=20, verbose_name='차량번호앞', null=False, blank=False)  # 차량번호앞
    vehicle_number_back = models.CharField(max_length=20, verbose_name='차량번호뒤', null=False, blank=False)  # 차량번호뒤
    maker = models.CharField(max_length=50, verbose_name='제조사', null=True , blank=True)  # 제조사
    vehicle_name = models.CharField(max_length=20, verbose_name='차량이름', null=True, blank=True)  # 차량종류
    # driver = models.OneToOneField(Member, verbose_name='기사', on_delete=models.SET_NULL, null=True, related_name="newVehicle")
    # driver_name = models.CharField(verbose_name='기사이름', max_length=100, null=False, blank=True)
    # driver = models.CharField(verbose_name='기사이름', max_length=100, null=False, blank=True)
    # driver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='newVehicles')
    driver = models.ForeignKey("humanresource.Member", on_delete=models.CASCADE, null=True, related_name='newVehicle')
    vehicle_serial = models.CharField(max_length=50, verbose_name='제조사', null=True, blank=True)  # 차대번호
    passenger_capacity = models.IntegerField(verbose_name='승차인원', null=True, blank=True)  # 승차인원
    type = models.CharField(verbose_name='형식', max_length=100, null=True, blank=True) #형식
    make_year = models.IntegerField(verbose_name='출고연도', null=True, blank=True) #출고년도
    model_year = models.IntegerField(verbose_name='모델연도', null=True, blank=True)  # 모델연도
    fuel_type = models.CharField(max_length=20, verbose_name='원동기형식', null=True, blank=True)  # 원동기형식
    registration_date = models.DateField(verbose_name='정기점검일', null=True, blank=True)  # 정기점검일
    in_use = models.BooleanField(verbose_name='사용여부', null=False, blank=True,  default=True)  # 사용여부
    remark = models.TextField(verbose_name='비고', null=True, blank=True)  # 비고
    garage = models.CharField(max_length=50, verbose_name='차고지', null=True , blank=True) #차고지
    
    #차량가격
    vehicle_price = models.IntegerField(verbose_name='차량가격', null=True, blank=True)  # 차량가격
    depreciation_month = models.IntegerField(verbose_name='감가상각(월)', null=True, blank=True)  # 감가상각(월)
    number_price = models.IntegerField(verbose_name='번호판가격', null=True, blank=True)  # 번호판가격
    depreciation_year = models.IntegerField(verbose_name='감가상각 기준 연도', null=True, blank=True)  # 감가상각 기준 연도
    insurance_pay_date = models.DateField(verbose_name='보험납부일', null=True, blank=True)  # 보험납부일
    insurance_price = models.IntegerField(verbose_name='보험비', null=True, blank=True)  # 보험비
    monthly_installment = models.IntegerField(verbose_name='할부금액(월)', null=True, blank=True)  # 할부금액(월)
    remaining_installment_amount = models.IntegerField(verbose_name='남은 할부액', null=True, blank=True)  # 남은 할부액

    #차량옵션
    led = models.BooleanField(verbose_name='전광판유무', null=True, blank=True, default=False)
    cold = models.BooleanField(verbose_name='냉장고유무', null=True, blank=True, default=False)
    sing = models.BooleanField(verbose_name='노래방유무', null=True, blank=True, default=False)
    usb = models.BooleanField(verbose_name='USB 유무', null=True, blank=True, default=False)
    hot = models.BooleanField(verbose_name='온수기유무', null=True, blank=True, default=False)
    tv = models.BooleanField(verbose_name='tv유무', null=True, blank=True, default=False)

    # 총 정비 금액
    total_maintenance_cost = models.IntegerField(verbose_name='총정비금액', default=0)
    # 총 튜닝 금액
    total_tuning_cost = models.IntegerField(verbose_name='총튜닝금액', default=0)

    
    def count_filled_fields(self):
        """차량 필드 중 값이 채워진 필드의 개수를 계산하고 디버깅 출력"""
        
        fields_to_check = [
            self.vehicle_number_front, self.vehicle_number_back, self.maker, self.vehicle_name, self.driver,
            self.vehicle_serial, self.passenger_capacity, self.type, self.make_year, self.model_year,
            self.fuel_type, self.registration_date, self.remark, self.garage,
            self.vehicle_price, self.depreciation_month, self.number_price, self.depreciation_year, 
            self.insurance_pay_date, self.insurance_price, self.monthly_installment, self.remaining_installment_amount
        ]
        
        boolean_fields = [
            self.led, self.cold, self.sing, self.usb, self.hot, self.tv, self.in_use
        ]

        # 값이 있는 필드만 세기 (None과 빈 문자열 제외)
        filled_fields_count = sum(1 for field in fields_to_check if field not in [None, ''])
        
        # BooleanField는 None이 아닌 경우 모두 카운팅 (True/False 모두 포함)
        boolean_fields_count = sum(1 for field in boolean_fields if field is not None)

        # 디버깅 출력
        print("일반 필드 값:")
        for field in fields_to_check:
            print(f"Field: {field}, Is Counted: {field not in [None, '']}")

        print("Boolean 필드 값:")
        for field in boolean_fields:
            print(f"Boolean Field: {field}, Is Counted: {field is not None}")

        details_count = filled_fields_count + boolean_fields_count


        return details_count
    

    def __str__(self):
        return f'{self.id} / {self.vehicle_number_back}'


class Maintenance(models.Model):
    MAINTENANCE_CHOICES = [
        ('정비', '정비'),
        ('튜닝', '튜닝'),
        ('점검', '점검')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    type = models.CharField(verbose_name='구분', max_length=100, choices=MAINTENANCE_CHOICES)
    work_date = models.DateField(verbose_name='작업일자')
    content = models.TextField(verbose_name='작업내용')
    cost = models.IntegerField(verbose_name='비용')


    def delete(self, *args, **kwargs):
        # 삭제 시, 정비 내역에 따라 차량 금액에서 빼줍니다.
        if self.type == '정비':
            self.vehicle.total_maintenance_cost -= self.cost
        elif self.type == '튜닝':
            self.vehicle.total_tuning_cost -= self.cost

        # super() 호출하여 실제 삭제 처리
        super().delete(*args, **kwargs)

        # Vehicle 저장
        self.vehicle.save()