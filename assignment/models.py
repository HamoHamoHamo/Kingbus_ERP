from django.db import models
from humanresource.models import Member, Department
from vehicle.models import Vehicle

class Group(models.Model):
    name = models.CharField(verbose_name='그룹 이름', max_length=50, null=False, unique=True)
    number = models.IntegerField(verbose_name='순번', null=False, default=999)
    fix = models.CharField(verbose_name='고정', max_length=1, null=False, default='n')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="assignment_group_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        return str(self.number) + self.name

class OldAssignmentData(models.Model):
    group = models.ForeignKey(Group, verbose_name='그룹', related_name="old_assignment_data", on_delete=models.SET_NULL, null=True)
    assignment = models.CharField(verbose_name="업무", max_length=100, null=False)
    references = models.CharField(verbose_name='참조사항', max_length=100, null=False, blank=True)
    start_time = models.CharField(verbose_name='시작시간', max_length=16, null=False)
    end_time = models.CharField(verbose_name='종료시간', max_length=16, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=100, null=False, default=0)
    allowance = models.CharField(verbose_name='수당', max_length=100, null=False, default=0)
    number1 = models.CharField(verbose_name='순번1', max_length=100, null=False, default=0)
    number2 = models.CharField(verbose_name='순번2', max_length=100, null=False, default=0)
    num1 = models.IntegerField(verbose_name='순번1숫자만', null=True)
    num2 = models.IntegerField(verbose_name='순번2숫자만', null=True)
    location = models.CharField(verbose_name='위치', max_length=100, null=False)
    use_vehicle = models.CharField(verbose_name='차량사용여부', max_length=100, null=False, default='사용')
    week = models.CharField(verbose_name='운행요일', max_length=20, null=False)
    type = models.CharField(verbose_name='고정업무', max_length=20, null=False)
    use = models.CharField(verbose_name='사용여부', max_length=50, null=False, blank=True, default='사용')
    
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="old_assignment_data_creator", db_column="creator_id", null=True)
    def __str__(self):
        return self.assignment

class OldAssignment(models.Model):
    group = models.ForeignKey(Group, verbose_name='그룹', related_name="old_assignment", on_delete=models.SET_NULL, null=True)
    assignment_id = models.ForeignKey(OldAssignmentData, verbose_name='업무 데이터', related_name="old_assignment_id", on_delete=models.SET_NULL, null=True)
    edit_date = models.CharField(verbose_name='수정기준일', max_length=50, null=False, blank=True)
    assignment = models.CharField(verbose_name="업무", max_length=100, null=False)
    references = models.CharField(verbose_name='참조사항', max_length=100, null=False, blank=True)
    start_time = models.CharField(verbose_name='시작시간', max_length=16, null=False)
    end_time = models.CharField(verbose_name='종료시간', max_length=16, null=False)
    price = models.CharField(verbose_name='계약금액', max_length=100, null=False, default=0)
    allowance = models.CharField(verbose_name='수당', max_length=100, null=False, default=0)
    number1 = models.CharField(verbose_name='순번1', max_length=100, null=False, default=0)
    number2 = models.CharField(verbose_name='순번2', max_length=100, null=False, default=0)
    num1 = models.IntegerField(verbose_name='순번1숫자만', null=True)
    num2 = models.IntegerField(verbose_name='순번2숫자만', null=True)
    location = models.CharField(verbose_name='위치', max_length=100, null=False)
    use_vehicle = models.CharField(verbose_name='차량사용여부', max_length=100, null=False, default='사용')
    week = models.CharField(verbose_name='운행요일', max_length=20, null=False)
    type = models.CharField(verbose_name='고정업무', max_length=20, null=False)
    use = models.CharField(verbose_name='사용여부', max_length=50, null=False, blank=True, default='사용')
    
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="old_assignment_creator", db_column="creator_id", null=True)
    def __str__(self):
        return self.assignment

class OldAssignmentConnect(models.Model):
    assignment_id = models.ForeignKey(OldAssignment, on_delete=models.CASCADE, related_name="old_assignment_connect", null=False)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="old_member_assignment", null=True)
    bus_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="old_bus_assignment", null=True)
    start_date = models.CharField(verbose_name='시작날짜', max_length=16, null=False)
    end_date = models.CharField(verbose_name='종료날짜', max_length=16, null=False)
    price = models.CharField(verbose_name='금액', max_length=40, null=False)
    allowance = models.CharField(verbose_name='수당', max_length=40, null=False)
    type = models.CharField(verbose_name='고정업무', max_length=20, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="old_assignment_connect_creator", db_column="creator_id", null=True)
    def __str__(self):
        return f'{self.assignment_id} / {self.start_date[2:10]}'

# 고정업무
class FixedAssignment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="fixed_assignment", null=True)
    primary_manager_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="fixed_assignment_primary_manager", null=True)
    secondary_manager_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="fixed_assignment_secondary_manager", null=True)
    assignment = models.CharField(verbose_name='업무', max_length=18, null=False)
    notes = models.CharField(verbose_name='참고사항', max_length=30, null=False, blank=True)
    week = models.CharField(verbose_name='요일', max_length=10, null=False)
    start_time = models.CharField(verbose_name='시작시간', max_length=16, null=False, blank=True)
    end_time = models.CharField(verbose_name='종료시간', max_length=16, null=False, blank=True)
    is_active = models.BooleanField(verbose_name='사용 여부', null=False, default=True)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="fixed_assignment_creator", db_column="creator_id", null=True)

class FixedAssignmentHistory(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="fixed_assignment_history", null=True)
    fixed_assignment_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="history", null=True)
    edit_date = models.CharField(verbose_name='수정기준일', max_length=50, null=False)
    primary_manager_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="fixed_assignment_history_primary_manager", null=True)
    secondary_manager_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="fixed_assignment_history_secondary_manager", null=True)
    assignment = models.CharField(verbose_name='업무', max_length=18, null=False)
    notes = models.CharField(verbose_name='참고사항', max_length=30, null=False, blank=True)
    week = models.CharField(verbose_name='요일', max_length=10, null=False)
    start_time = models.CharField(verbose_name='시작시간', max_length=16, null=False, blank=True)
    end_time = models.CharField(verbose_name='종료시간', max_length=16, null=False, blank=True)
    is_active = models.BooleanField(verbose_name='사용 여부', null=False, default=True)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="fixed_assignment_history_creator", db_column="creator_id", null=True)

# 일반업무
class TemporaryAssignment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="temporary_assignment", null=True)
    primary_manager_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="temporary_assignment_primary_manager", null=True)
    secondary_manager_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="temporary_assignment_secondary_manager", null=True)
    assignment = models.CharField(verbose_name='업무', max_length=18, null=False)
    notes = models.CharField(verbose_name='참고사항', max_length=30, null=False, blank=True)
    start_date = models.CharField(verbose_name='시작일시', max_length=16, null=False, blank=True)
    end_date = models.CharField(verbose_name='종료일시', max_length=16, null=False, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="temporary_assignment_creator", db_column="creator_id", null=True)
