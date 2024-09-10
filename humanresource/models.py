from datetime import datetime
from uuid import uuid4
from django.db import models
from datetime import datetime, timedelta
from config.settings import FORMAT
from dateutil.relativedelta import relativedelta
from common.constant import TODAY, WEEK
from django.apps import apps
from salary.selectors import SalarySelector
from salary.models import HourlyWage

class Team(models.Model):
    name =models.CharField(verbose_name='팀이름', max_length=100, null=False, blank=False)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    def __str__(self):
        return self.name

class Member(models.Model):
    def clean(self):
        if self.user_id == "":
            self.user_id = None
            
    user_id = models.CharField(max_length=100, verbose_name='사용자id', null=True, blank=True)
    password = models.TextField(verbose_name='비밀번호', null=False, blank=True)
    name = models.CharField(verbose_name='이름', max_length=100, null=False)
    role = models.CharField(verbose_name='업무', max_length=100, null=False)
    birthdate = models.CharField(verbose_name='생년월일', max_length=100, null=False, blank=True)
    resident_number1 = models.CharField(verbose_name='주민등록번호 앞자리', max_length=100, null=False, blank=True)
    resident_number2 = models.CharField(verbose_name='주민등록번호 뒷자리', max_length=100, null=False, blank=True)
    phone_num = models.CharField(verbose_name='전화번호', max_length=100, null=False)
    emergency = models.CharField(verbose_name='비상연락망', max_length=100, null=False, blank=True)
    address = models.CharField(verbose_name='주소', max_length=100, null=False)
    entering_date = models.CharField(verbose_name='입사일', max_length=100, null=False)
    note = models.CharField(verbose_name='비고', max_length=100, null=False, blank=True)
    interview_date = models.CharField(verbose_name='면접일', max_length=100, null=False, blank=True)
    contract_date = models.CharField(verbose_name='계약일', max_length=100, null=False, blank=True)
    contract_renewal_date = models.CharField(verbose_name='근로계약갱신일', max_length=100, null=False, blank=True)
    contract_condition = models.CharField(verbose_name='근로계약조건', max_length=100, null=False, blank=True)
    renewal_reason = models.CharField(verbose_name='갱신사유', max_length=100, null=False, blank=True)
    apply_path = models.CharField(verbose_name='지원경로', max_length=100, null=False, blank=True)
    career = models.CharField(verbose_name='경력사항', max_length=100, null=False, blank=True)
    position = models.CharField(verbose_name='직급', max_length=100, null=False, blank=True)
    apprenticeship_note = models.CharField(verbose_name='견습노선 및 내용', max_length=100, null=False, blank=True)
    leave_reason = models.CharField(verbose_name='퇴사사유', max_length=100, null=False, blank=True)
    company = models.CharField(verbose_name='소속회사', max_length=100, null=False, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="member_team", null=True)
    final_opinion = models.CharField(verbose_name='최종소견', max_length=100, null=False, blank=True)
    interviewer = models.CharField(verbose_name='면접담당자', max_length=100, null=False, blank=True)
    end_date = models.CharField(verbose_name='종료일', max_length=100, null=False, blank=True)
    leave_date = models.CharField(verbose_name='퇴사일', max_length=100, null=False, blank=True)
    allowance_type = models.CharField(verbose_name='수당지급기준', max_length=100, null=False, blank=True, default="기사수당(현재)")
    license = models.CharField(verbose_name='버스기사자격증', max_length=100, null=False, blank=True)

    base = models.CharField(verbose_name='기본급', max_length=20, null=False, default=0)
    service_allowance = models.CharField(verbose_name='근속수당', max_length=20, null=False, default=0)
    annual_allowance = models.CharField(verbose_name='연차수당', max_length=20, null=False, default=0)
    performance_allowance = models.CharField(verbose_name='성과급', max_length=20, null=False, default=0)
    overtime_allowance = models.CharField(verbose_name='근로추가수당', max_length=20, null=False, default=0)
    meal = models.CharField(verbose_name='식대', max_length=20, null=False, default=0)
    
    new_annual_allowance = models.CharField(verbose_name="연차수당2", max_length=100, null=False, default=0)
    team_leader_allowance_roll_call = models.CharField(verbose_name="팀장수당(점호관리)", max_length=100, null=False, default=0)
    team_leader_allowance_vehicle_management = models.CharField(verbose_name="팀장수당(차량관리)", max_length=100, null=False, default=0)
    team_leader_allowance_task_management = models.CharField(verbose_name="팀장수당(업무관리)", max_length=100, null=False, default=0)
    full_attendance_allowance = models.CharField(verbose_name="만근수당", max_length=100, null=False, default=0)
    diligence_allowance = models.CharField(verbose_name="성실수당", max_length=100, null=False, default=0)
    accident_free_allowance = models.CharField(verbose_name="무사고수당", max_length=100, null=False, default=0)
    welfare_meal_allowance = models.CharField(verbose_name="복리후생 (식대)", max_length=100, null=False, default=0)
    welfare_fuel_allowance = models.CharField(verbose_name="복리후생(유류비)", max_length=100, null=False, default=0)
    
    pub_date = models.DateTimeField(verbose_name="등록날짜", auto_now_add=True, null=False)
    creator = models.CharField(verbose_name='작성자 이름', max_length=100, null=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    token = models.CharField(verbose_name='fcmtoken', max_length=500, null=False, blank=True)
    authority = models.IntegerField(verbose_name='권한', null=False, default=4)
    use = models.CharField(verbose_name='사용여부', max_length=30, null=False, default='사용')
    def __str__(self):
        return self.name

class MemberFile(models.Model):
    def get_file_path(instance, filename):
    
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['humanresource/', ymd_path, uuid_name])

    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="member_file", db_column="member_id", null=False)
    file = models.FileField(upload_to=get_file_path, null=False)
    filename = models.TextField(null=True, verbose_name='첨부파일명')
    path = models.TextField(null=True, verbose_name='경로')
    type = models.CharField(max_length=100, null=False, verbose_name='면허증, 버스운전자격증')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="member_file_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    def __str__(self):
        return self.member_id.name + "_" + self.filename

# class HR(models.Model):
#     member_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="hr_member", null=True)
#     hr_type = models.CharField(verbose_name="종류", max_length=30, null=False)
#     reason = models.CharField(verbose_name="내용", max_length=100, null=False)
#     start_date = models.CharField(verbose_name="시작날짜", max_length=10,  null=False)
#     end_date = models.CharField(verbose_name="종료날짜", max_length=10,  null=False)
#     pub_date = models.DateTimeField(verbose_name="등록날짜", auto_now_add=True, null=False)
#     creator = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="hr_creator", db_column="creator_id", null=True)

# class Yearly(models.Model):
#     member_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="yearly_member", null=True)
#     year = models.CharField(verbose_name="년도", max_length=4, null=False)
#     cnt = models.CharField(verbose_name="연차 사용 개수", max_length=10, null=False)
#     creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="yearly_creator", db_column="user_id", null=True)
#     pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
#     def __str__(self):
#         return self.member_id.name


class Salary(models.Model):
    def set_new_annual_allowance(month, member):
        salary_selector = SalarySelector()
        hourly_wage = salary_selector.get_hourly_wage_by_month(month)
        if hourly_wage == None:
            hourly_wage = HourlyWage.new_wage(month)

        ordinary_hourly_wage = int(int(hourly_wage.wage1) + int(member.service_allowance) * 12 / 1470)
        return ordinary_hourly_wage * 6

    def new_salary(creator, month, member):
        last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
        # attendance = DispatchRegularlyConnect.objects.filter(work_type='출근').filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))
        # leave = DispatchRegularlyConnect.objects.filter(work_type='퇴근').filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))
        # order = DispatchOrderConnect.objects.filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))

        # attendance_price = 0
        # leave_price = 0
        # order_price = 0
        # assignment_price = 0
        # regularly_assignment_price = 0

        base = 0
        service_allowance = 0
        performance_allowance = 0
        annual_allowance = 0
        overtime_allowance = 0
        meal = 0

        new_annual_allowance = Salary.set_new_annual_allowance(month, member)
        team_leader_allowance_roll_call = 100000 if member.role == "팀장" else 0
        team_leader_allowance_vehicle_management = 100000 if member.role == "팀장" else 0
        team_leader_allowance_task_management = 100000 if member.role == "팀장" else 0
        full_attendance_allowance = 200000 if member.role == "팀장" or member.role == "운전원" else 0
        diligence_allowance = 200000 if member.role == "팀장" or member.role == "운전원" else 0
        accident_free_allowance = 200000 if member.role == "팀장" or member.role == "운전원" else 0
        welfare_meal_allowance = 0 if member.role == "팀장" or member.role == "운전원" else 0
        welfare_fuel_allowance = 0 if member.role == "팀장" or member.role == "운전원" else 0
        

        # 이번달 이후의 급여면 현재 member에 있는 값으로 급여 생성
        if TODAY[:7] <= month:
            base = int(member.base)
            service_allowance = int(member.service_allowance)
            performance_allowance = int(member.performance_allowance)
            annual_allowance = int(member.annual_allowance)
            overtime_allowance = int(member.overtime_allowance)
            meal = int(member.meal)

        #    new_annual_allowance = int(member.new_annual_allowance)
        #    team_leader_allowance_roll_call = int(member.team_leader_allowance_roll_call)
        #    team_leader_allowance_vehicle_management = int(member.team_leader_allowance_vehicle_management)
        #    team_leader_allowance_task_management = int(member.team_leader_allowance_task_management)
        #    full_attendance_allowance = int(member.full_attendance_allowance)
        #    diligence_allowance = int(member.diligence_allowance)
        #    accident_free_allowance = int(member.accident_free_allowance)
        #    welfare_meal_allowance = int(member.welfare_meal_allowance)
        #    welfare_fuel_allowance = int(member.welfare_fuel_allowance)
            

        # if salary:
        #     base = salary.base
        #     service_allowance = salary.service_allowance
        #     performance_allowance = salary.performance_allowance

        # Salary가 없을 때만 동작하는 함수라서 계산할 필요 없음
        # if attendance['driver_allowance__sum']:
        #     attendance_price = int(attendance['driver_allowance__sum'])
        # if leave['driver_allowance__sum']:
        #     leave_price = int(leave['driver_allowance__sum'])
        # if order['driver_allowance__sum']:
        #     order_price = int(order['driver_allowance__sum'])
        
        try:
            Category = apps.get_model('Category', 'Model')
            payment_date = Category.objects.get(type='급여지급일').category
        except:
            payment_date = 1


        salary = Salary(
            member_id = member,
            base = base,
            service_allowance = service_allowance,
            performance_allowance = performance_allowance,
            annual_allowance = annual_allowance,
            overtime_allowance = overtime_allowance,
            meal = meal,

            new_annual_allowance = new_annual_allowance,
            team_leader_allowance_roll_call = team_leader_allowance_roll_call,
            team_leader_allowance_vehicle_management = team_leader_allowance_vehicle_management,
            team_leader_allowance_task_management = team_leader_allowance_task_management,
            full_attendance_allowance = full_attendance_allowance,
            diligence_allowance = diligence_allowance,
            accident_free_allowance = accident_free_allowance,
            welfare_meal_allowance = welfare_meal_allowance,
            welfare_fuel_allowance = welfare_fuel_allowance,
            # attendance = attendance_price,
            # leave = leave_price,
            # order = order_price,
            # assignment = assignment_price,
            # regularly_assignment = regularly_assignment_price,
            attendance = 0,
            leave = 0,
            order = 0,
            assignment = 0,
            regularly_assignment = 0,
            total = 0,
            month = month,
            payment_date = payment_date,
            creator = creator
        )
        salary.save()
        salary.total = salary.calculate_total()
        return salary

    def calculate_total(self):
        member = self.member_id
        if member.role == '용역' or member.role == '관리자':
            return int(self.performance_allowance) + int(self.attendance) + int(self.leave) + int(self.order) + int(self.assignment) + int(self.regularly_assignment) + int(self.additional) - int(self.deduction)
        elif (member.role == '팀장' or member.role == '운전원') and member.allowance_type == '기사수당(현재)':
            return int(self.base) + int(self.service_allowance) + int(self.performance_allowance) + int(self.annual_allowance) + int(self.meal) + int(self.attendance) + int(self.leave) + int(self.order) + int(self.assignment) + int(self.regularly_assignment) + int(self.additional) - int(self.deduction)
        elif (member.role == '팀장' or member.role == '운전원') and member.allowance_type == '기사수당(변경)':
            return int(self.overtime_allowance) + int(self.performance_allowance) + int(self.attendance) + int(self.leave) + int(self.order) + int(self.assignment) + int(self.regularly_assignment) + int(self.additional) - int(self.deduction)
        else:
            return "error"
    def calculate_new_total(self, wage):
        return int(wage) + int(self.service_allowance) + int(self.annual_allowance) + int(self.team_leader_allowance_roll_call) + int(self.team_leader_allowance_vehicle_management) + int(self.team_leader_allowance_task_management) + int(self.full_attendance_allowance) + int(self.diligence_allowance) + int(self.accident_free_allowance) + int(self.welfare_meal_allowance) + int(self.welfare_fuel_allowance) + int(self.additional) - int(self.deduction)

    def calculate_fixed(self):
        member = self.member_id
        if member.role == '용역' or member.role == '관리자':
            return int(self.performance_allowance)
        elif (member.role == '팀장' or member.role == '운전원') and member.allowance_type == '기사수당(현재)':
            return int(self.base) + int(self.service_allowance) + int(self.performance_allowance) + int(self.annual_allowance) + int(self.meal)
        elif (member.role == '팀장' or member.role == '운전원') and member.allowance_type == '기사수당(변경)':
            return int(self.overtime_allowance) + int(self.performance_allowance)
        else:
            return 0

    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="salary", null=True)
    base = models.CharField(verbose_name='기본급', max_length=20, null=False, default=0)
    service_allowance = models.CharField(verbose_name='근속수당', max_length=20, null=False, default=0)
    performance_allowance = models.CharField(verbose_name='성과급', max_length=20, null=False, default=0)
    annual_allowance = models.CharField(verbose_name='연차수당', max_length=20, null=False, default=0)
    overtime_allowance = models.CharField(verbose_name='근로추가수당', max_length=20, null=False, default=0)
    meal = models.CharField(verbose_name='식대', max_length=20, null=False, default=0)
    attendance = models.CharField(verbose_name='출근요금', max_length=20, null=False)
    leave = models.CharField(verbose_name='퇴근요금', max_length=20, null=False)
    order = models.CharField(verbose_name='일반주문요금', max_length=20, null=False)
    additional = models.CharField(verbose_name='추가요금', max_length=20, null=False, default=0)
    deduction = models.CharField(verbose_name='공제', max_length=20, null=False, default=0)
    assignment = models.CharField(verbose_name='일반업무', max_length=20, null=False, default=0)
    regularly_assignment = models.CharField(verbose_name='고정업무', max_length=20, null=False, default=0)
    
    new_annual_allowance = models.CharField(verbose_name="연차수당2", max_length=100, null=False, default=0)
    team_leader_allowance_roll_call = models.CharField(verbose_name="팀장수당(점호관리)", max_length=100, null=False, default=0)
    team_leader_allowance_vehicle_management = models.CharField(verbose_name="팀장수당(차량관리)", max_length=100, null=False, default=0)
    team_leader_allowance_task_management = models.CharField(verbose_name="팀장수당(업무관리)", max_length=100, null=False, default=0)
    full_attendance_allowance = models.CharField(verbose_name="만근수당", max_length=100, null=False, default=0)
    diligence_allowance = models.CharField(verbose_name="성실수당", max_length=100, null=False, default=0)
    accident_free_allowance = models.CharField(verbose_name="무사고수당", max_length=100, null=False, default=0)
    welfare_meal_allowance = models.CharField(verbose_name="복리후생 (식대)", max_length=100, null=False, default=0)
    welfare_fuel_allowance = models.CharField(verbose_name="복리후생(유류비)", max_length=100, null=False, default=0)

    #FIXME 임금총합계 저장 안하고 salary service에서 불러와서 계산하기, 추후 수정
    #new_total = models.CharField(verbose_name='임금총합계', max_length=20, null=False, default=0)

    #임금	근속수당	연차수당	팀장수당(점호관리)	팀장수당(차량관리)	팀장수당(업무관리)	만근수당	성실수당	무사고수당	복리후생 (식대)	복리후생(유류비)
    #기본급	근속수당	연차수당	성과급	식대	출근수당	퇴근수당	일반수당	업무수당
    
    total = models.CharField(verbose_name='총금액', max_length=20, null=False)
    month = models.CharField(verbose_name='지급월', null=False, max_length=7)
    payment_date = models.CharField(verbose_name='급여지급일', null=False, max_length=10, blank=True)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="salary_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    
    def __str__(self):
        if self.member_id:
            return self.member_id.name + ' ' + self.month

class AdditionalSalary(models.Model):
    salary_id = models.ForeignKey(Salary, on_delete=models.CASCADE, related_name="additional_salary", null=False)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="additional_member", null=False)
    price = models.CharField(verbose_name='금액', max_length=40, null=False, default='0')
    remark = models.CharField(verbose_name='비고', null=False, blank=True, max_length=100)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="additional_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    def __str__(self):
        if self.member_id:
            return self.member_id.name + ' ' + self.salary_id.month

class DeductionSalary(models.Model):
    salary_id = models.ForeignKey(Salary, on_delete=models.CASCADE, related_name="deduction_salary", null=False)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="deduction_member", null=False)
    price = models.CharField(verbose_name='금액', max_length=40, null=False, default='0')
    remark = models.CharField(verbose_name='비고', null=False, blank=True, max_length=100)
    deduction_type = models.CharField(verbose_name='종류', null=False, blank=True, max_length=100)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="deduction_user", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
     
    def __str__(self):
        if self.member_id:
            return self.member_id.name + ' ' + self.salary_id.month


class SalaryChecked(models.Model):
    salary = models.OneToOneField(Salary, on_delete=models.SET_NULL, related_name="salary_checked", null=True)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="salary_checked_user", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

class AccidentCase(models.Model):
    def get_file_path():
    
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['humanresource/accident', ymd_path, uuid_name])
    
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="accident_member", null=True)
    date = models.CharField(verbose_name="사고날짜", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="accident_creator", db_column="creator_id", null=True)
    
    #세부사항부분
    carnum = models.ForeignKey('vehicle.Vehicle', verbose_name='차량 번호', on_delete=models.SET_NULL, related_name="accident_details_car_id", null=True)
    route_name = models.CharField(verbose_name='노선명', max_length=100, null=False, blank=True)
    kind_of_accident = models.CharField(verbose_name='자차/대물', max_length=100, null=False, blank=True)
    damaged_car = models.CharField(verbose_name='피해 차량', max_length=100, null=False, blank=True)
    accident_location = models.CharField(verbose_name='사고 발생 지점', max_length=100, null=False, blank=True)
    accident_time_occur = models.CharField(verbose_name='사고 발생 시간', max_length=100, null=False, blank=True) 
    accident_time_solve = models.CharField(verbose_name='운행 재개 시간', max_length=100, null=False, blank=True)
    vehicle_speed = models.CharField(verbose_name='사고당시 차량 속도', max_length=100, null=False, blank=True)
    passenger_count = models.CharField(verbose_name='탑승인원', max_length=100, null=False, blank=True)
    accident_description = models.TextField(verbose_name='사고 개요', null=False, blank=True)

    #파일부분
    picture_our_vehicle = models.TextField(verbose_name='내 차량', null=False, blank=True)
    picture_thier_vehicle = models.TextField(verbose_name='상대방 차량', null=False, blank=True)
    picture_all_vehicles = models.TextField(verbose_name='내 차량/상대방 차량', null=False, blank=True)
    picture_from_far = models.TextField(verbose_name='먼 사진', null=False, blank=True)
    picture_from_close = models.TextField(verbose_name='가까운 사진', null=False, blank=True)

    picture_passenger_list = models.TextField(verbose_name='승객 명단 파일', null=False, blank=True)
    
    accident_report = models.TextField(verbose_name='사고 보고서', null=False, blank=True)
    agreement = models.TextField(verbose_name='합의서', null=False, blank=True)
    execution_confirm_oath = models.TextField(verbose_name='이행확약서', null=False, blank=True)
    vehicle_accident_reception = models.TextField(verbose_name='자동차 공제 사고 접수서', null=False, blank=True)
    vehicle_maintenence_bill = models.TextField(verbose_name='자동차 점검 정비 명세서', null=False, blank=True)
    deducted_payment_bill = models.TextField(verbose_name='공제금 지급청구서', null=False, blank=True)

