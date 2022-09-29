from django.db import models
from datetime import datetime
from humanresource.models import Member
from uuid import uuid4

# Create your models here.
class DocumentGroup(models.Model):
    name = models.CharField(verbose_name='그룹이름', max_length=50, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="document_group_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)

    def __str__(self):
        return self.name
class Document(models.Model):
    def get_file_path(instance, filename):
    
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['document/', ymd_path, f'{uuid_name}_{filename}'])

    group_id = models.ForeignKey(DocumentGroup, on_delete=models.CASCADE,related_name="group_file", db_column="vehicle_id", null=False)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="document_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
