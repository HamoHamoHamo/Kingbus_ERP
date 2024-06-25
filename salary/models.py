from django.db import models
from humanresource.models import Member

class HourlyWage(models.Model):
    def new_wage(month, creator):
        horuly_wage = HourlyWage.objects.create(
            wage1 = 0,
            wage2 = 0,
            wage3 = 0,
            wage4 = 0,
            month = month,
            creator = creator
        )
        return horuly_wage

    def get_wage(self, minute):
        wage1_condition = 60 * 4
        wage2_condition = 60 * 6
        wage3_condition = 60 * 8

        if minute <= wage1_condition:
            return self.wage1
        if minute <= wage2_condition:
            return self.wage2
        if minute <= wage3_condition:
            return self.wage3
        if minute > wage3_condition:
            return self.wage4
        return None

    wage1 = models.CharField(verbose_name='4시간 이하', max_length=40, null=False, default='0')
    wage2 = models.CharField(verbose_name='4시간 초과 6시간 이하', max_length=40, null=False, default='0')
    wage3 = models.CharField(verbose_name='6시간 초과 8시간 이하', max_length=40, null=False, default='0')
    wage4 = models.CharField(verbose_name='8시간 초과', max_length=40, null=False, default='0')
    month = models.CharField(verbose_name='월', max_length=7, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="hourly_wage", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
