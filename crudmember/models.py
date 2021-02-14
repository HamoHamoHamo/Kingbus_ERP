from django.db import models

class User(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    userid = models.CharField(max_length=64,verbose_name = '사용자id', null=True)
    name = models.CharField(max_length=10, verbose_name = '이름', null=True)
    password = models.CharField(max_length=255,verbose_name = '비밀번호')
    tel = models.IntegerField(verbose_name ='폰 번호', null=True)
    photo = models.ImageField(upload_to='images/',blank=True, null=True)
    authority = models.CharField(verbose_name ='권한', max_length=3, null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self):
        return self.userid

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'my_user'

class UserFile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="file", db_column="user_id", null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    class Meta:
        db_table = 'user_files'

class UserIP(models.Model):
    ip = models.CharField(max_length=100, null=False)
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    def __str__(self):
        return self.ip