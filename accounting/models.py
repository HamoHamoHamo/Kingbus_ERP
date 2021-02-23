from crudmember.models import User
from dispatch.models import DispatchOrder, DispatchConnect
from django.db import models
from humanresource.models import Member

class MonthlySalary(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="salary_monthly", db_column="member_id", null=True)
    base = models.IntegerField(verbose_name='기본급', null=False)
    bonus = models.IntegerField(verbose_name='상여금', null=False)
    additional = models.IntegerField(verbose_name='추가금', null=False)
    deductible = models.IntegerField(verbose_name='공제금', null=False)
    total = models.IntegerField(verbose_name='총금액', null=False)
    payment_month = models.DateField(verbose_name='지급월', null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="salary_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)

    def __str__(self):
        return self.member_id.name

class DailySalary(models.Model):
    bonus = models.IntegerField(verbose_name='상여금', null=False, blank=True)
    additional = models.IntegerField(verbose_name='추가금', null=False, blank=True)
    dispatch_id = models.ForeignKey(DispatchConnect, on_delete=models.SET_NULL, related_name="salary_daily_dispatch", db_column="dispatch_id", null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="salary_daily_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    monthly_salary = models.ForeignKey(MonthlySalary, on_delete=models.CASCADE, related_name="salary_daily", db_column="monthly_id", null=False)

    def __str__(self):
        return self.monthly_salary.member_id.name
        
class Outlay(models.Model):
    kinds = models.CharField(verbose_name='지급구분', max_length=10, null=False)
    salary_id = models.ForeignKey(MonthlySalary, on_delete=models.CASCADE, related_name="outlay_salary", db_column="salary_id" ,null=True, blank=True)
    #vehicle_id = models.models.ForeignKey(, on_delete=models.SET_NULL, realted_name="outlay_salary", db_column="salary_id" ,null=True)
    brief = models.CharField(verbose_name='적요', max_length=30, null=False)
    price = models.IntegerField(verbose_name='지출금액', null=False)
    outlay_date = models.DateField(verbose_name='지출일자', null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="outlay_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)

    def __str__(self):
        return str(self.outlay_date)[:10]
    
class Collect(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="collect_order", db_column="order_id", null=False)
    brief = models.CharField(verbose_name='적요', max_length=30, null=False)
    collect_date = models.DateField(verbose_name='수금일자', null=True)
    check = models.BooleanField(verbose_name='입금확인', default=False)
    remark = models.CharField(verbose_name='비고', max_length=50, null=True)
    
class Income(models.Model):
    kinds = models.CharField(verbose_name='수입구분', max_length=30, null=False)
    collect_id = models.ForeignKey(Collect, on_delete=models.CASCADE, related_name="income_collect", db_column="collect_id", null=True)
    brief = models.CharField(verbose_name='적요', max_length=30, null=False)
    price = models.IntegerField(verbose_name='수입금액', null=False)
    income_date = models.DateField(verbose_name='수입일자', null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="income_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)