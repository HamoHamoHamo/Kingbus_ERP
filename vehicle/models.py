from django.db import models
from crudmember.models import User, Category
from humanresource.models import Member
from datetime import datetime
from uuid import uuid4

class Vehicle(models.Model):
    vehicle_num0 = models.CharField(verbose_name='차량번호 앞자리', max_length=100, null=False)
    vehicle_num = models.CharField(verbose_name='차량번호', max_length=100, null=False)
    vehicle_id = models.CharField(verbose_name='차대번호', max_length=100, null=False, blank=True)
    motor_type = models.CharField(verbose_name='원동기형식', max_length=100, null=False, blank=True)
    rated_output = models.CharField(verbose_name='정격출력', max_length=100, null=False, blank=True)
    vehicle_type = models.CharField(verbose_name='차량이름', max_length=100, null=False, blank=True)
    maker = models.CharField(verbose_name='제조사', max_length=100, null=False, blank=True)
    model_year = models.CharField(verbose_name='연식', max_length=100, null=False, blank=True)
    release_date = models.CharField(verbose_name='출고일자', max_length=100, null=False, blank=True)
    driver = models.OneToOneField(Member, verbose_name='기사', on_delete=models.SET_NULL, null=True, related_name="vehicle", db_column="vehicle")
    driver_name = models.CharField(verbose_name='기사이름', max_length=100, null=False, blank=True)
    use = models.CharField(verbose_name='사용여부', max_length=100, null=False, default='사용', blank=True)
    passenger_num = models.CharField(verbose_name='승차인원', max_length=100, null=False, blank=True)
    check_date = models.CharField(verbose_name='정기점검일', max_length=100, null=False, blank=True)
    type = models.CharField(verbose_name='형식', max_length=100, null=False, blank=True)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="vehicle_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    
    def __str__(self):
        return f'{self.id} / {self.vehicle_num}'

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
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="vehicle_document_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

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

class Accident(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="accident_member", null=True)
    date = models.CharField(verbose_name="사고날짜", max_length=100, null=False, blank=True)
    # TODO 결재 구현시 반영
    # approval = models.ForeignKey(Approval, ...)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="accident_creator", db_column="creator_id", null=True)
    
    #세부사항부분
    # https://stackoverflow.com/questions/44601550/how-to-solve-the-circular-import-error-in-django
    carnum = models.ForeignKey('vehicle.Vehicle', verbose_name='차량 번호', on_delete=models.SET_NULL, related_name="accident_details_car_id", null=True)
    # carnum = models.CharField(verbose_name='차량 번호', max_length=100, null=False, blank=True) #Vehicle모델 참조하기로함
    # route_name = models.CharField(verbose_name='노선명', max_length=100, null=False, blank=True)
    dispatch_order_connect = models.ForeignKey('dispatch.DispatchOrderConnect', verbose_name='일반노선', on_delete=models.SET_NULL, related_name="accident_details_dispatch_order_connect", null=True)
    dispatch_regularly_connect = models.ForeignKey('dispatch.DispatchRegularlyConnect', verbose_name='출퇴근노선', on_delete=models.SET_NULL, related_name="accident_details_dispatch_regularly_connect", null=True)

    kind_of_accident = models.CharField(verbose_name='자차/대물', max_length=100, null=False, blank=True)
    damaged_car = models.CharField(verbose_name='피해 차량', max_length=100, null=False, blank=True)
    accident_location = models.CharField(verbose_name='사고 발생 지점', max_length=100, null=False, blank=True) # 간략히? 아니면 지도 좌표??
    accident_time_occur = models.CharField(verbose_name='사고 발생 시간', max_length=100, null=False, blank=True) 
    accident_time_solve = models.CharField(verbose_name='운행 재개 시간', max_length=100, null=False, blank=True)
    vehicle_speed = models.CharField(verbose_name='사고당시 차량 속도', max_length=100, null=False, blank=True)
    passenger_count = models.CharField(verbose_name='탑승인원', max_length=100, null=False, blank=True)
    accident_description = models.TextField(verbose_name='사고 개요', null=False, blank=True)

    #파일부분
    picture_our_vehicle = models.TextField(verbose_name='내 차량', null=False, blank=True)
    picture_thier_vehicle = models.TextField(verbose_name='상대방 차량', null=False, blank=True)
    picture_all_vehicles = models.TextField(verbose_name='내 차량/상대방 차량', null=False, blank=True) # 상대가 사람이면 어떻게??
    picture_from_far = models.TextField(verbose_name='먼 사진', null=False, blank=True)
    picture_from_close = models.TextField(verbose_name='가까운 사진', null=False, blank=True)

    picture_passenger_list = models.TextField(verbose_name='승객 명단 파일', null=False, blank=True)
    
    accident_report = models.TextField(verbose_name='사고 보고서', null=False, blank=True)
    # driver_license = models.TextField(verbose_name='운전면허증', null=False, blank=True)
    # 운전면허 누구의? 그리고 member모델에 있는거 쓰면 되는게 아닌지? case의 member모델 참조하여 가져오기
    agreement = models.TextField(verbose_name='합의서', null=False, blank=True)
    execution_confirm_oath = models.TextField(verbose_name='이행확약서', null=False, blank=True)
    vehicle_accident_reception = models.TextField(verbose_name='자동차 공제 사고 접수서', null=False, blank=True)
    vehicle_maintenence_bill = models.TextField(verbose_name='자동차 점검 정비 명세서', null=False, blank=True)
    deducted_payment_bill = models.TextField(verbose_name='공제금 지급청구서', null=False, blank=True)