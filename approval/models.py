from datetime import datetime
from django.db import models
from humanresource.models import Member
from uuid import uuid4
from common.constant import DATE_TIME_FORMAT

class Approval(models.Model):
    approval_type = models.CharField(verbose_name="결제 종류", max_length=100, null=False)
    title = models.CharField(verbose_name="결제 종류", max_length=100, null=False)
    content = models.TextField(verbose_name='내용', null=False)
    status = models.CharField(verbose_name="현황", max_length=100, null=False)
    date = models.CharField(verbose_name="등록일", max_length=100, null=False)
    current_approver_name = models.CharField(verbose_name="결재자 이름", max_length=100, null=False, default="고영이")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="approval_creator", db_column="creator_id", null=True)

    def __str__(self):
        return f"{self.approval_type} {self.title} {self.creator.name}"
    
class Approver(models.Model):
    def get_updated_at(self):
        return datetime.strftime(self.updated_at, DATE_TIME_FORMAT)

    index = models.IntegerField(verbose_name="순서", default=1)
    approval_id = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name="approver")
    content = models.TextField(verbose_name='내용', null=False, blank=True)
    status = models.CharField(verbose_name="재가여부", max_length=100, null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="approver_creator", db_column="creator_id", null=True)

class ApprovalFile(models.Model):
    def get_file_path(instance, filename):
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['approval/', ymd_path, uuid_name])

    approval_id = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name="approval_file", db_column="approval_id", null=False)
    file = models.FileField(upload_to=get_file_path, null=False)
    filename = models.TextField(null=True, verbose_name='첨부파일명')
    path = models.TextField(null=True, verbose_name='경로')
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="approval_file_user", db_column="user_id", null=True)
    def __str__(self):
        return self.approval_id.title + "_" + self.filename