from datetime import datetime
from uuid import uuid4
from django.db import models
from crudmember.models import User

class Member(models.Model):
    name = models.CharField(verbose_name='이름', max_length=10, null=False)
    role = models.CharField(verbose_name='업무', max_length=10, null=False)
    birthdate = models.CharField(verbose_name='생년월일', max_length=10, null=False)
    address = models.CharField(verbose_name='주소', max_length=50, null=False)
    phone_num = models.CharField(verbose_name='전화번호', max_length=11, null=False)
    entering_date = models.CharField(verbose_name='입사일', max_length=10, null=False, blank=True)
    license_number = models.CharField(verbose_name='면허번호', max_length=30, null=False, blank=True)
    pub_date = models.DateTimeField(verbose_name="등록날짜", auto_now_add=True, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_creator", db_column="creator_id", null=True)

    def __str__(self):
        return self.name

class HR(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="hr_member", null=True)
    hr_type = models.CharField(verbose_name="종류", max_length=30, null=False)
    reason = models.CharField(verbose_name="내용", max_length=100, null=False)
    start_date = models.CharField(verbose_name="시작날짜", max_length=10,  null=False)
    end_date = models.CharField(verbose_name="종료날짜", max_length=10,  null=False)
    pub_date = models.DateTimeField(verbose_name="등록날짜", auto_now_add=True, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hr_creator", db_column="creator_id", null=True)

class Yearly(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="yearly_member", null=True)
    year = models.CharField(verbose_name="년도", max_length=4, null=False)
    cnt = models.CharField(verbose_name="연차 사용 개수", max_length=10, null=False)

    def __str__(self):
        return self.member_id.name
