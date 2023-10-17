from dispatch.models import DispatchOrder, DispatchRegularly, RegularlyGroup
from django.db import models
from humanresource.models import Member
import datetime

class Income(models.Model):
    serial = models.CharField(verbose_name='전표번호', max_length=100, null=False)
    date = models.CharField(verbose_name='날짜', max_length=20, null=False)
    depositor = models.CharField(verbose_name='입금자', max_length=100, null=False)
    payment_method = models.CharField(verbose_name='지급방식', max_length=100, null=False, default='계좌')
    bank = models.CharField(verbose_name='은행', max_length=100, null=False, blank=True)
    commission = models.CharField(verbose_name='가맹점 수수료', max_length=30, null=False, default='0')
    acc_income = models.CharField(verbose_name='입금액', max_length=30, null=False)
    total_income = models.CharField(verbose_name='총 금액', max_length=30, null=False, default='0')
    used_price = models.CharField(verbose_name='처리된 금액', max_length=30, null=False, default='0')
    state = models.CharField(verbose_name='상태', max_length=100, null=False, default='미처리')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="income_user", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    
    def __str__(self):
        return self.serial


class Collect(models.Model):
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.SET_NULL, related_name="order_collect", null=True, blank=True)
    group_id = models.ForeignKey(RegularlyGroup, on_delete=models.SET_NULL, related_name="group_collect", null=True, blank=True)
    month = models.CharField(verbose_name='월', max_length=10, null=True)
    income_id = models.ForeignKey(Income, on_delete=models.CASCADE, related_name="income_collect", null=True)
    price = models.CharField(verbose_name='처리된 금액', max_length=30, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="user_collect", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    

class TotalPrice(models.Model):
    group_id = models.ForeignKey(RegularlyGroup, on_delete=models.CASCADE, related_name="total_price_group", null=True, blank=True)
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="total_price_order", null=True, blank=True)
    month = models.CharField(verbose_name='월', max_length=10, null=False)
    total_price = models.CharField(verbose_name='총 계약금액', max_length=30, null=False, default=0)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="total_price_creator", db_column="creator_id", null=True)
    
    def __str__(self):
        if self.group_id:
            return '출퇴근 ' + self.month + ' ' + self.group_id.name
        elif self.order_id:
            return self.month + ' ' + self.order_id.route
    
class AdditionalCollect(models.Model):
    group_id = models.ForeignKey(RegularlyGroup, on_delete=models.CASCADE, related_name="regularly_additional_collect", null=True, blank=True)
    order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE, related_name="order_additional_collect", null=True, blank=True)
    month = models.CharField(verbose_name='월', max_length=10, null=False)
    category = models.CharField(verbose_name='항목', max_length=100, null=False)
    value = models.CharField(verbose_name='공급가액', max_length=30, null=False)
    VAT = models.CharField(verbose_name='부가세', max_length=30, null=False)
    total_price = models.CharField(verbose_name='합계', max_length=30, null=False)
    note = models.CharField(verbose_name='비고', max_length=100, null=False, blank=True)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="user_additional_collect", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    
    def __str__(self):
        if self.order_id:
            return self.order_id.route
        elif self.group_id:
            return self.group_id.name

class LastIncome(models.Model):
    tr_date = models.CharField(verbose_name='거래일시', max_length=20, null=False)
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="user_last_income", db_column="user_id", null=True)
    pub_date = models.DateTimeField(verbose_name='작성시간', auto_now_add=True, null=False)
    
    def __str__(self):
        return self.tr_date