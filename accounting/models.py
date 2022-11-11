from dispatch.models import DispatchOrder, DispatchRegularly
from django.db import models
from humanresource.models import Member
import datetime

class Salary(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="salary_monthly", null=False)
    attendance = models.CharField(verbose_name='출근요금', max_length=40, null=False)
    leave = models.CharField(verbose_name='퇴근요금', max_length=40, null=False)
    order = models.CharField(verbose_name='일반주문요금', max_length=40, null=False)
    additional = models.CharField(verbose_name='기타요금', max_length=40, null=False)
    total = models.CharField(verbose_name='총금액', max_length=40, null=False)
    remark = models.CharField(verbose_name='비고', null=True, max_length=100 )
    month = models.CharField(verbose_name='지급월', null=False,max_length=7, default=str(datetime.datetime.now())[:7])
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="salary_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    

    
class AdditionalSalary(models.Model):
    salary_id = models.ForeignKey(Salary, on_delete=models.CASCADE, related_name="additional_salary", null=False)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="additional_member", null=False)
    date = models.CharField(verbose_name='날짜', null=False, max_length=10)
    price = models.CharField(verbose_name='금액', max_length=40, null=False)
    remark = models.CharField(verbose_name='비고', null=False, blank=True, max_length=100)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="additional_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)


class Income(models.Model):
    serial = models.CharField(verbose_name='전표번호', max_length=50, null=False)
    date = models.CharField(verbose_name='날짜', max_length=20, null=False)
    depositor = models.CharField(verbose_name='입금자', max_length=50, null=False)
    payment_method = models.CharField(verbose_name='지급방식', max_length=10, null=False, default='계좌')
    bank = models.CharField(verbose_name='은행', max_length=30, null=False)
    commission = models.CharField(verbose_name='가맹점 수수료', max_length=30, null=False, default='0')
    acc_income = models.CharField(verbose_name='입금액', max_length=30, null=False)
    used_income = models.CharField(verbose_name='처리된 금액', max_length=30, null=False, default='0')
    state = models.CharField(verbose_name='상태', max_length=30, null=False, default='미처리')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="income_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    
    def __str__(self):
        return self.serial


class Collect(models.Model):
    type = models.CharField(verbose_name='출퇴근 or 일반', max_length=1, null=False)
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.SET_NULL, related_name="order_collect", null=True)
    regularly_id = models.ForeignKey(DispatchRegularly, on_delete=models.SET_NULL, related_name="regularly_collect", null=True)
    income_id = models.ForeignKey(Income, on_delete=models.SET_NULL, related_name="income_collect", null=True)
    price = models.CharField(verbose_name='처리된 금액', max_length=20, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="user_collect", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    
    def __str__(self):
        return self.income_id + ' ' + self.price 


class LastIncome(models.Model):
    tr_date = models.CharField(verbose_name='거래일시', max_length=20, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="user_last_income", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    
    def __str__(self):
        return self.tr_date