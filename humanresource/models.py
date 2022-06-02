from datetime import datetime
from uuid import uuid4
from django.db import models
from crudmember.models import User

class Member(models.Model):
    name = models.CharField(verbose_name='이름', max_length=10, null=False)
    role = models.CharField(verbose_name='업무', max_length=10, null=False)
    person_id1 = models.CharField(verbose_name='주민번호 앞자리', max_length=6, null=False)
    person_id2 = models.CharField(verbose_name='주민번호 뒷자리', max_length=7, null=False)
    address = models.CharField(verbose_name='주소', max_length=50, null=False)
    phone_num = models.CharField(verbose_name='전화번호', max_length=11, null=False)
    entering_date = models.CharField(verbose_name='입사일', max_length=10, null=False, blank=True)
    resignation_date = models.CharField(verbose_name='퇴사일', max_length=10, null=False, blank=True)
    
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
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['humanresource/', ymd_path, uuid_name])

    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="document_member", db_column="member_id", null=False)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')