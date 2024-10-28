from django.db import models
from django.db.models import F
from crudmember.models import Category
from humanresource.models import Member
from datetime import datetime
from enum import Enum
from uuid import uuid4
from firebase.media_firebase import delete_firebase_file

class Vehicle(models.Model):
    # 차량정보
    vehicle_num0 = models.CharField(verbose_name='차량번호 앞자리', max_length=100, null=False)
    vehicle_num = models.CharField(verbose_name='차량번호', max_length=100, null=False)
    vehicle_id = models.CharField(verbose_name='차대번호', max_length=100, null=False, blank=True)
    motor_type = models.CharField(verbose_name='원동기형식', max_length=100, null=False, blank=True)
    rated_output = models.CharField(verbose_name='정격출력', max_length=100, null=False, blank=True)
    vehicle_type = models.CharField(verbose_name='차량이름', max_length=100, null=False, blank=True)
    maker = models.CharField(verbose_name='제조사', max_length=100, null=False, blank=True)
    model_year = models.CharField(verbose_name='연식', max_length=100, null=False, blank=True)
    release_date = models.CharField(verbose_name='출고일자', max_length=100, null=False, blank=True)
    driver = models.ForeignKey(Member, verbose_name='기사', on_delete=models.SET_NULL, null=True, related_name="vehicle", db_column="vehicle", blank=True)
    use = models.CharField(verbose_name='사용여부', max_length=100, null=False, default='사용', blank=True)
    passenger_num = models.CharField(verbose_name='승차인원', max_length=100, null=False, blank=True)
    check_date = models.CharField(verbose_name='정기점검일', max_length=100, null=False, blank=True)
    type = models.CharField(verbose_name='형식', max_length=100, null=False, blank=True)
    garage = models.ForeignKey("dispatch.Station", on_delete=models.SET_NULL, related_name="garage", verbose_name='차고지', null=True, blank=True)
    remark = models.CharField(verbose_name='비고', max_length=100, null=False, blank=True)

    #차량가격
    vehicle_price = models.IntegerField(verbose_name='차량가격', null=True, blank=True)  # 차량가격
    depreciation_month = models.IntegerField(verbose_name='감가상각(월)', null=True, blank=True)  # 감가상각(월)
    number_price = models.IntegerField(verbose_name='번호판가격', null=True, blank=True)  # 번호판가격
    depreciation_year = models.IntegerField(verbose_name='감가상각 기준 연도', null=True, blank=True)  # 감가상각 기준 연도
    insurance_pay_date = models.CharField(verbose_name='보험납부일', max_length=100, null=True, blank=True)  # 보험납부일
    insurance_price = models.IntegerField(verbose_name='보험비', null=True, blank=True)  # 보험비
    monthly_installment = models.IntegerField(verbose_name='할부금액(월)', null=True, blank=True)  # 할부금액(월)
    remaining_installment_amount = models.IntegerField(verbose_name='남은 할부액', null=True, blank=True)  # 남은 할부액

    #차량옵션
    led = models.BooleanField(verbose_name='전광판유무', default=False)
    fridge = models.BooleanField(verbose_name='냉장고유무', default=False)
    sing = models.BooleanField(verbose_name='노래방유무', default=False)
    usb = models.BooleanField(verbose_name='USB유무', default=False)
    water_heater = models.BooleanField(verbose_name='온수기유무', default=False)
    tv = models.BooleanField(verbose_name='tv유무', default=False)

    # 총 정비 금액
    total_maintenance_cost = models.IntegerField(verbose_name='총정비금액', default=0)
    # 총 튜닝 금액
    total_tuning_cost = models.IntegerField(verbose_name='총튜닝금액', default=0)

    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="vehicle_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    
    def count_filled_fields(self):
        """차량 필드 중 값이 채워진 필드의 개수를 계산하고 디버깅 출력"""
        
        fields_to_check = [
            # 차량정보
            self.vehicle_num0,
            self.vehicle_num,
            self.vehicle_id,
            self.motor_type,
            self.rated_output,
            self.vehicle_type,
            self.maker,
            self.model_year,
            self.release_date,
            self.driver,
            # self.use,
            self.passenger_num,
            self.check_date,
            self.type,
            self.garage,
            self.remark,

            # 차량가격
            self.vehicle_price,
            self.depreciation_month,
            self.number_price,
            self.depreciation_year,
            self.insurance_pay_date,
            self.insurance_price,
            self.monthly_installment,
            self.remaining_installment_amount,

            # 차량옵션
            # self.led,
            # self.cold,
            # self.sing,
            # self.usb,
            # self.hot,
            # self.tv,
        ]

        # 값이 있는 필드만 세기 (None과 빈 문자열 제외)
        filled_fields_count = sum(1 for field in fields_to_check if field not in [None, ''])
        
        # 디버깅 출력
        # print("일반 필드 값:")
        # for field in fields_to_check:
        #     print(f"Field: {field}, Is Counted: {field not in [None, '']}")

        return filled_fields_count


    def __str__(self):
        return f'{self.id} / {self.vehicle_num}'

class Maintenance(models.Model):
    MAINTENANCE_CHOICES = [
        ('정비', '정비'),
        ('튜닝', '튜닝'),
        ('점검', '점검')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='maintenance_records', null=True)
    type = models.CharField(verbose_name='구분', max_length=100, choices=MAINTENANCE_CHOICES)
    work_date = models.DateField(verbose_name='작업일자')
    content = models.TextField(verbose_name='작업내용')
    cost = models.IntegerField(verbose_name='비용')

    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="maintenance_creator", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    def save(self, *args, **kwargs):
        if self.vehicle:
            if self.type == '정비':
                # self.vehicle.total_maintenance_cost += self.cost
                self.vehicle.total_maintenance_cost = F('total_maintenance_cost') + self.cost
            elif self.type == '튜닝':
                # self.vehicle.total_tuning_cost += self.cost
                self.vehicle.total_tuning_cost = F('total_tuning_cost') + self.cost
            self.vehicle.save()

        # super() 호출하여 실제 저장 처리
        super().save(*args, **kwargs)


class DocumentType(Enum):
    VEHICLE_REGISTRATION_CERTIFICATE = '차량등록증'
    VEHICLE_FUNCTIONAL_DIAGNOSIS = '자동차기능종합진단서'
    VEHICLE_INSURANCE = '차량보험'
    VEHICLE_INSTALLMENT = '차량할부'

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

class VehicleDocument(models.Model):
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['vehicle/document', uuid_name])

    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE,related_name="vehicle_file", db_column="vehicle_id", null=False)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.TextField(null=True, verbose_name='첨부파일명')
    path = models.TextField(null=True, verbose_name='경로')
    type = models.CharField(max_length=30, verbose_name='종류', choices=DocumentType.choices())
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="vehicle_document_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    def delete(self, *args, **kwargs):
        # firebase에서 파일 삭제
        delete_firebase_file(self.path)
        super().delete(*args, **kwargs)
        
class VehiclePhoto(models.Model):
    PHOTO_TYPE_CHOICES = [
        ('차량 앞', '차량 앞'),
        ('차량 뒤', '차량 뒤'),
        ('차량 옆', '차량 옆')
    ]

    def get_file_path(instance, filename):
        uuid_name = uuid4().hex
        return '/'.join(['vehicle/photo', uuid_name])
    
    driver = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="vehicle_photo",)
    date = models.CharField(max_length=30, verbose_name='날짜')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_photo", db_column="vehicle_id", null=False)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.TextField(null=True, verbose_name='첨부파일명')
    path = models.TextField(null=True, verbose_name='경로')
    type = models.CharField(max_length=30, verbose_name='종류', choices=PHOTO_TYPE_CHOICES)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="vehicle_photo_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    def delete(self, *args, **kwargs):
        # firebase에서 파일 삭제
        delete_firebase_file(self.path)
        super().delete(*args, **kwargs)

class Refueling(models.Model):
    refueling_date = models.CharField(verbose_name='주유일', max_length=100, null=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="vehicle_refueling", null=True)
    driver = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="driver_refueling", null=True)
    km = models.CharField(verbose_name='주유 시 km', max_length=100, null=False)
    refueling_amount = models.CharField(verbose_name='주유량', max_length=100, null=False)
    urea_solution = models.CharField(verbose_name='요소수 L', max_length=100, null=False)
    gas_station = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="gas_station", null=True)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="refueling_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    
class DailyChecklist(models.Model):
    submit_check = models.BooleanField(verbose_name="제출여부", null=False, default=False)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="daily_checklist_member", null=True)
    date = models.CharField(verbose_name="날짜", max_length=100, null=False, blank=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="daily_checklist_bus_id", null=True)
    oil_engine_condition = models.CharField(verbose_name="오일/엔진,부동액", max_length=100, null=False, blank=True)
    oil_power_clutch_condition = models.CharField(verbose_name="오일/파워,클러치", max_length=100, null=False, blank=True)
    coolant_washer_condition = models.CharField(verbose_name="냉각수,워셔액", max_length=100, null=False, blank=True)
    external_body_condition = models.CharField(verbose_name="외부차체상태(파손확인)", max_length=100, null=False, blank=True)
    lighting_device_condition = models.CharField(verbose_name="등화장치(실내/외)", max_length=100, null=False, blank=True)
    blackbox_condition = models.CharField(verbose_name="블랙박스(작동여부확인)", max_length=100, null=False, blank=True)
    tire_condition = models.CharField(verbose_name="타이어상태(나사,못)", max_length=100, null=False, blank=True)
    interior_condition = models.CharField(verbose_name="실내상태(복도,선반,청소상태)", max_length=100, null=False, blank=True)
    safety_belt_slide_condition = models.CharField(verbose_name="안전 벨트/슬라이드 상태", max_length=100, null=False, blank=True)
    uniform_worn_condition = models.CharField(verbose_name="제복착용", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="daily_checklist_creator", db_column="creator_id", null=True)

class WeeklyChecklist(models.Model):
    submit_check = models.BooleanField(verbose_name="제출여부", null=False, default=False)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="weekly_checklist_member", null=True)
    date = models.CharField(verbose_name="날짜", max_length=100, null=False, blank=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="weekly_checklist_bus_id", null=True)
    glass_tint_condition = models.CharField(verbose_name="유리/선팅", max_length=100, null=False, blank=True)
    license_garage_record_condition = models.CharField(verbose_name="자격증/차고지증명서/운행기록증", max_length=100, null=False, blank=True)
    tire_wheel_condition = models.CharField(verbose_name="타이어 휠 상태", max_length=100, null=False, blank=True)
    vehicle_cleanliness_condition = models.CharField(verbose_name="차량청결(외부)", max_length=100, null=False, blank=True)
    emergency_hammer_condition = models.CharField(verbose_name="비상망치(수량 및 야광스티커)", max_length=100, null=False, blank=True)
    fire_extinguisher_condition = models.CharField(verbose_name="소화기(수량 및 충전상태)", max_length=100, null=False, blank=True)
    blackbox_format_check_condition = models.CharField(verbose_name="블랙박스 포맷확인", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="weekly_checklist_creator", db_column="creator_id", null=True)

class EquipmentChecklist(models.Model):
    submit_check = models.BooleanField(verbose_name="제출여부", null=False, default=False)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="equipment_checklist_member", null=True)
    date = models.CharField(verbose_name="날짜", max_length=100, null=False, blank=False)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name="equipment_checklist_bus_id", null=True)
    tv_condition = models.CharField(verbose_name="TV", max_length=100, null=False, blank=True)
    dvd_condition = models.CharField(verbose_name="DVD", max_length=100, null=False, blank=True)
    karaoke_condition = models.CharField(verbose_name="노래방", max_length=100, null=False, blank=True)
    floor_speaker_condition = models.CharField(verbose_name="바닥스피커", max_length=100, null=False, blank=True)
    wireless_microphone_condition = models.CharField(verbose_name="무선마이크", max_length=100, null=False, blank=True)
    gilseong_tech_condition = models.CharField(verbose_name="길성테크", max_length=100, null=False, blank=True)
    floor_power_condition = models.CharField(verbose_name="바닥파워", max_length=100, null=False, blank=True)
    inverter_condition = models.CharField(verbose_name="인버터", max_length=100, null=False, blank=True)
    blackbox_condition = models.CharField(verbose_name="블랙박스", max_length=100, null=False, blank=True)
    billboard_condition = models.CharField(verbose_name="전광판", max_length=100, null=False, blank=True)
    blind_condition = models.CharField(verbose_name="블라인드", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="equipment_checklist_creator", db_column="creator_id", null=True)
