from django.db import models
from crudmember.models import User

class Member(models.Model):
    name = models.CharField(verbose_name='이름', max_length=10, null=False)
    authority = models.CharField(verbose_name='권한', max_length=10, null=False)
    role = models.CharField(verbose_name='업무', max_length=10, null=False)
    person_id = models.IntegerField(verbose_name='주민번호', null=False)
    address = models.CharField(verbose_name='주소', max_length=50, null=False)
    phone_num = models.IntegerField(verbose_name='전화번호', null=False)
    entering_date = models.DateField(verbose_name='입사일', null=False)
    resignation_date = models.DateField(verbose_name='퇴사일', null=False)
    license_num = models.CharField(verbose_name='면허번호', max_length=30, null=False)
    #bus_id = models.CharField(verbose_name='이름', max_length=10, null=False)
    check = models.CharField(verbose_name='운행판정표', max_length=50, null=False)

    def __str__(self):
        return self.name


class HR(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="hr_member", db_column="member_id", null=False)
    hr_type = models.CharField(verbose_name="종류", max_length=10, null=False)
    reason = models.CharField(verbose_name="사유", max_length=100, null=False)
    start_date = models.DateTimeField(verbose_name="시작날짜", null=False)
    finish_date = models.DateTimeField(verbose_name="종료날짜", null=False)
    pub_date = models.DateTimeField(verbose_name="등록날짜",auto_now_add=True, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", db_column="creator_id", null=True)

class MemberDocument(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="document_member", db_column="member_id", null=False)
    file = models.FileField(verbose_name="파일", null=False)