from crudmember.models import User
from django.db import models
from humanresource.models import Member
import datetime

class Salary(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="salary_monthly", null=False)
    attendance = models.IntegerField(verbose_name='출근요금', null=False)
    leave = models.IntegerField(verbose_name='퇴근요금', null=False)
    order = models.IntegerField(verbose_name='일반주문요금', null=False)
    additional = models.IntegerField(verbose_name='기타요금', null=False)
    total = models.IntegerField(verbose_name='총금액', null=False)
    remark = models.CharField(verbose_name='비고', null=True, max_length=100 )
    month = models.CharField(verbose_name='지급월', null=False,max_length=7, default=str(datetime.datetime.now())[:7])
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="salary_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    

    
class AdditionalSalary(models.Model):
    salary_id = models.ForeignKey(Salary, on_delete=models.CASCADE, related_name="additional_salary", null=False)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="additional_member", null=False)
    date = models.CharField(verbose_name='날짜', null=False, max_length=10)
    price = models.IntegerField(verbose_name='금액', null=False)
    remark = models.CharField(verbose_name='비고', null=False, blank=True, max_length=100)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="additional_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)

class Income(models.Model):
    kinds = models.CharField(verbose_name='날짜', max_length=10, null=False)
    attendance = models.CharField(verbose_name='출근금액', max_length=20, null=False)
    leave = models.CharField(verbose_name='퇴근금액', max_length=20, null=False)
    order = models.CharField(verbose_name='일반주문금액', max_length=20, null=False)
    collect = models.CharField(verbose_name='수금액', max_length=20, null=False)
    outstanding = models.CharField(verbose_name='미수금액', max_length=20, null=False)
    total = models.CharField(verbose_name='합계', max_length=30, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="income_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)