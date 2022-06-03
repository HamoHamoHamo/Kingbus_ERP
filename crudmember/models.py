from django.db import models



class User(models.Model):  # 장고에서 제공하는 models.Model를 상속받아야한다.
    user_id = models.CharField(max_length=64, verbose_name='사용자id')
    password = models.CharField(max_length=255, verbose_name='비밀번호')
    company = models.CharField(max_length=30, verbose_name='회사이름')
    company_tel = models.CharField(max_length=20, verbose_name='회사 전화번호')
    company_address = models.CharField(max_length=50, verbose_name='회사 주소')
    registeration_num = models.CharField(max_length=20, verbose_name='사업자등록번호')
    name = models.CharField(max_length=10, verbose_name='관리자 이름')
    manager_tel = models.CharField(verbose_name='관리자 폰 번호', max_length=11)
    manager_mail = models.CharField(verbose_name='관리자 이메일', max_length=30)
    photo = models.ImageField(upload_to='images/', blank=True)
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    # 저장되는 시점의 시간을 자동으로 삽입해준다.
    def __str__(self):
        return self.name


class UserFile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="file", db_column="user_id", null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)




class UserIP(models.Model):
    ip = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.ip