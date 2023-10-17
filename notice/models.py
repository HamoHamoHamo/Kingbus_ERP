from django.db import models
from uuid import uuid4
from datetime import datetime

from humanresource.models import Member

class Notice(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    title = models.CharField(max_length=64, verbose_name='제목', null=False)
    content = models.TextField(verbose_name='내용', null=False)
    kinds = models.CharField(max_length=10, verbose_name='종류', null=False)
    view_cnt = models.IntegerField(verbose_name='조회수', null=False, default=0)
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    creator = models.ForeignKey(Member, related_name="notice_user", verbose_name='작성자', db_column="user_id", null=True, on_delete=models.SET_NULL)
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self):
        return self.title

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'notice'

class NoticeFile(models.Model):
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['notice/', ymd_path, uuid_name])

    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE,related_name="notice_file", db_column="notice_id", null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')

    class Meta:
        db_table = 'notice_file'

    def __str__(self):
        return self.notice_id.title



class NoticeComment(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="comment_user", db_column="notice_id", null=True)
    content = models.TextField(max_length=200, verbose_name="댓글내용", null=False)
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    creator = models.ForeignKey(Member, related_name="comment", verbose_name='작성자', db_column="user_id", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.notice_id.title

    class Meta:
        db_table = 'notice_comment'

class NoticeViewCnt(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE, db_column="notice_id", null=False)
    user_id = models.ForeignKey(Member, verbose_name='작성자', db_column="user_id", null=True, on_delete=models.SET_NULL)
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='조회시간')