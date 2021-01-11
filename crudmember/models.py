from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, verbose_name = '아이디')