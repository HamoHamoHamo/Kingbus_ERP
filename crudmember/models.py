from django.db import models
from humanresource.models import Member

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
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
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

class Category(models.Model):
    type = models.CharField(max_length=100, verbose_name='종류', null=False)
    category = models.CharField(max_length=100, verbose_name='항목', null=False)

    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="category_user", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)

    def __str__(self):
        return self.type + " " + self.category

class Client(models.Model):
    business_num = models.CharField(max_length=100, verbose_name='사업자번호', null=False, blank=True)
    name = models.CharField(max_length=100, verbose_name='거래처이름', null=False)
    representative = models.CharField(max_length=100, verbose_name='대표자명', null=False, blank=True)
    phone = models.CharField(max_length=100, verbose_name='대표전화', null=False)
    manager = models.CharField(max_length=100, verbose_name='담당자', null=False, blank=True)
    manager_phone = models.CharField(max_length=100, verbose_name='담당자번호', null=False, blank=True)
    email = models.CharField(max_length=100, verbose_name='이메일', null=False, blank=True)
    address = models.CharField(max_length=100, verbose_name='주소', null=False, blank=True)
    note = models.CharField(max_length=100, verbose_name='비고', null=False, blank=True)

    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="client_user", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    