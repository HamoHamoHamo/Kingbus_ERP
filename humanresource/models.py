from django.db import models
from crudmember.models import User

class Member(models.Model):
    name = models.CharField(verbose_name='이름', max_length=10, null=False)
    role = models.CharField(verbose_name='업무', max_length=10, null=False)
    person_id1 = models.IntegerField(verbose_name='주민번호 앞자리', null=False)
    person_id2 = models.IntegerField(verbose_name='주민번호 뒷자리', null=False)
    address = models.CharField(verbose_name='주소', max_length=50, null=False)
    phone_num = models.IntegerField(verbose_name='전화번호', null=False)
    entering_date = models.CharField(verbose_name='입사일', max_length=10, null=False, blank=True)
    resignation_date = models.CharField(verbose_name='퇴사일', max_length=10, null=False, blank=True)
    license_num = models.CharField(verbose_name='면허번호', max_length=30, null=False, blank=True)
    #bus_id = models.CharField(verbose_name='이름', max_length=10, null=False)
    check = models.CharField(verbose_name='운행판정표', max_length=50, null=False, blank=True)

    def __str__(self):
        return self.name


class HR(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="hr_member", db_column="member_id", null=True)
    hr_type = models.CharField(verbose_name="종류", max_length=10, null=False)
    reason = models.CharField(verbose_name="내용", max_length=100, null=False)
    start_date = models.CharField(verbose_name="시작날짜", max_length=10,  null=False)
    finish_date = models.CharField(verbose_name="종료날짜", max_length=10,  null=False)
    pub_date = models.DateTimeField(verbose_name="등록날짜", auto_now_add=True, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", db_column="creator_id", null=True)

class MemberDocument(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="document_member", db_column="member_id", null=False)
    file = models.FileField(verbose_name="파일", null=False)