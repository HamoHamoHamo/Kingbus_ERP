from django.db import models

class HourlyWage(models.Model):
    def new_wage(month, creator=None):
        horuly_wage = HourlyWage.objects.create(
            wage1 = 12500,
            wage2 = 13000,
            month = month,
            creator = creator
        )
        return horuly_wage

    def get_wage(self, minute):
        wage_condition = 60 * 30

        if minute < wage_condition:
            return self.wage1
        else:
            return self.wage2

    wage1 = models.CharField(verbose_name='주 30시간 미만', max_length=40, null=False, default='0')
    wage2 = models.CharField(verbose_name='주 30시간 이상', max_length=40, null=False, default='0')
    month = models.CharField(verbose_name='월', max_length=7, null=False)
    creator = models.ForeignKey("humanresource.Member", on_delete=models.SET_NULL, related_name="hourly_wage", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
