from django.db import models
from uuid import uuid4
from crudmember.models import User
from datetime import datetime

class Document(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    creator = models.ForeignKey(User, related_name="document_user", verbose_name='작성자', db_column="user_id", null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, verbose_name='제목', null=False)
    content = models.TextField(max_length=3000, verbose_name='내용', null=False)
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self):
        return self.title

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'document'

class DocumentFile(models.Model):
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['document/', ymd_path, uuid_name])

    document_id = models.ForeignKey(Document, on_delete=models.SET_NULL,related_name="document_file", db_column="document_id", null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')

    class Meta:
        db_table = 'document_file'
