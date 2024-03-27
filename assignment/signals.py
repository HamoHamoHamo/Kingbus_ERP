from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dispatch.views import FORMAT
from django.db.models.signals import post_save, post_delete, pre_delete
from django.db.models import Sum
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import AssignmentConnect
from accounting.models import TotalPrice, AdditionalCollect
from humanresource.models import Salary, Member
from humanresource.views import new_salary

import re
import math






@receiver(post_save, sender=AssignmentConnect)
def save_connect(sender, instance, created, **kwargs):
    month = instance.start_date[:7]
    creator = instance.creator
    member = instance.member_id
    
    # Salary 업데이트
    try:
        salary = Salary.objects.filter(member_id=member).get(month=month)
        allowance = AssignmentConnect.objects.filter(member_id=member).filter(start_date__startswith=month).aggregate(Sum('allowance'))
        salary.assignment = int(allowance['allowance__sum']) if allowance['allowance__sum'] else 0
        salary.total = salary.calculate_total()
        # salary.total = int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.assignment) + int(salary.additional) - int(salary.deduction)
        salary.save()
    except Salary.DoesNotExist:
        new_salary(creator, month, member)

    if not hasattr(instance, 'same_accounting') or not instance.same_accounting:
        print('create update accounting')
        # TotalPrice 업데이트
        # total = update_total_price(instance)

@receiver(post_delete, sender=AssignmentConnect)
def delete_connect(sender, instance, **kwargs):
    # Salary 업데이트
    month = instance.start_date[:7]
    try:
        member = instance.member_id
        salary = Salary.objects.filter(member_id=member).get(month=month)
        allowance = AssignmentConnect.objects.filter(member_id=member).filter(start_date__startswith=month).aggregate(Sum('allowance'))
        salary.assignment = int(allowance['allowance__sum']) if allowance['allowance__sum'] else 0
        salary.total = salary.calculate_total()
        # salary.total = int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.assignment) + int(salary.additional) - int(salary.deduction)
        salary.save()
    except Member.DoesNotExist:
        pass
        
    if not hasattr(instance, 'same_accounting') or not instance.same_accounting:
        print("delete update accounting")
        # TotalPrice 업데이트
        # total = update_total_price(instance)

