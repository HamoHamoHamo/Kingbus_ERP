from django.db import models
from crudmember.models import User

class Notice(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    creator = models.ForeignKey(User, related_name="user", verbose_name='작성자', db_column="user_id", null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, verbose_name='제목', null=False)
    content = models.TextField(max_length=3000, verbose_name='내용', null=False)
    kinds = models.CharField(max_length=10, verbose_name='종류', null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self):
        return self.title

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'notice'

class NoticeFile(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE,related_name="file", db_column="notice_id", null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return self.notice_id.title

    class Meta:
        db_table = 'notice_file'

class NoticeComment(models.Model):
    creator = models.ForeignKey(User, related_name="comment", verbose_name='작성자', db_column="user_id", null=False, on_delete=models.CASCADE)
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="comment_user", db_column="notice_id", null=True)
    content = models.CharField(max_length=200, verbose_name="댓글내용", null=False)
    registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')

    def __str__(self):
        return self.notice_id.title

    class Meta:
        db_table = 'notice_comment'