from datetime import datetime
from uuid import uuid4
from django.db import models
import datetime

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
    company =models.CharField(verbose_name='소속회사', max_length=100, null=False, blank=True)
    team =models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="member_team", null=True)
    final_opinion =models.CharField(verbose_name='최종소견', max_length=100, null=False, blank=True)
    interviewer =models.CharField(verbose_name='면접담당자', max_length=100, null=False, blank=True)
    end_date =models.CharField(verbose_name='종료일', max_length=100, null=False, blank=True)
    leave_date =models.CharField(verbose_name='퇴사일', max_length=100, null=False, blank=True)
    allowance_type =models.CharField(verbose_name='수당지급기준', max_length=100, null=False, default="기사수당(현재)")

    base = models.CharField(verbose_name='기본급', max_length=20, null=False, default=0)
    service_allowance = models.CharField(verbose_name='근속수당', max_length=20, null=False, default=0)
    annual_allowance = models.CharField(verbose_name='연차수당', max_length=20, null=False, default=0)
    performance_allowance = models.CharField(verbose_name='성과급', max_length=20, null=False, default=0)
    meal = models.CharField(verbose_name='식대', max_length=20, null=False, default=0)
    
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
    
        ymd_path = datetime.datetime.now().strftime('%Y/%m/%d')
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
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="salary", null=True)
    base = models.CharField(verbose_name='기본급', max_length=20, null=False, default=0)
    service_allowance = models.CharField(verbose_name='근속수당', max_length=20, null=False, default=0)
    performance_allowance = models.CharField(verbose_name='성과급', max_length=20, null=False, default=0)
    annual_allowance = models.CharField(verbose_name='연차수당', max_length=20, null=False, default=0)
    meal = models.CharField(verbose_name='식대', max_length=20, null=False, default=0)
    attendance = models.CharField(verbose_name='출근요금', max_length=20, null=False)
    leave = models.CharField(verbose_name='퇴근요금', max_length=20, null=False)
    order = models.CharField(verbose_name='일반주문요금', max_length=20, null=False)
    additional = models.CharField(verbose_name='추가요금', max_length=20, null=False, default=0)
    deduction = models.CharField(verbose_name='공제', max_length=20, null=False, default=0)
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
    