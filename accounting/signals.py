from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Salary, Income, AdditionalSalary
from humanresource.models import Member

@receiver(post_save, sender=AdditionalSalary)
def create_additional(sender, instance, created, **kwargs):
    print("SIGNAL")
    salary = Salary.objects.prefetch_related('additional_salary').filter(member_id=instance.member_id.id).get(month=instance.date[:7])
    additional = salary.additional_salary.all()
    total_additional = 0
    for a in additional:
        total_additional += a.price
    salary.additional = total_additional
    salary.total = salary.attendance + salary.leave + salary.order + salary.additional
    salary.save()