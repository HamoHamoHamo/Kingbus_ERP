from datetime import datetime
from uuid import uuid4
from django.db import models
from crudmember.models import User

class Member(models.Model):
    num = models.IntegerField(verbose_name='번호', null=False, default=1)
    user_id = models.CharField(max_length=64, verbose_name='사용자id', unique=True, null=False)
    password = models.CharField(max_length=255, verbose_name='비밀번호')
    name = models.CharField(verbose_name='이름', max_length=10, null=False)
    role = models.CharField(verbose_name='업무', max_length=10, null=False)
    birthdate = models.CharField(verbose_name='생년월일', max_length=10, null=False)
    address = models.CharField(verbose_name='주소', max_length=50, null=False)
    phone_num = models.CharField(verbose_name='전화번호', max_length=25, null=False, blank=True)
    entering_date = models.CharField(verbose_name='입사일', max_length=10, null=False, blank=True)
    pub_date = models.DateTimeField(verbose_name="등록날짜", auto_now_add=True, null=False)
    creator = models.CharField(verbose_name='작성자 이름', max_length=30, null=False, blank=True)

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
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')
    type = models.CharField(max_length=30, null=False, verbose_name='면허증, 버스운전자격증')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="member_file_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
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
