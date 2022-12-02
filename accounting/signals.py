from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Income, AdditionalCollect, TotalPrice
from humanresource.models import Member

# @receiver(post_save, sender=AdditionalSalary)
# def create_additional_salary(sender, instance, created, **kwargs):
#     print("SIGNAL")
#     salary = Salary.objects.prefetch_related('additional_salary').filter(member_id=instance.member_id.id).get(month=instance.date[:7])
#     additional = salary.additional_salary.all()
#     total_additional = 0
#     for a in additional:
#         total_additional += int(a.price)
#     salary.additional = total_additional
#     salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)
#     salary.save()

############
@receiver(post_save, sender=AdditionalCollect)
def create_additional_collect(sender, instance, created, **kwargs):
    if instance.group_id:
        try:
            total = TotalPrice.objects.filter(group_id=instance.group_id).get(month=instance.month)

        except TotalPrice.DoesNotExist:
            total = TotalPrice(
                group_id = instance.group_id,
                month = instance.month,
                total_price = 0,
                creator = instance.creator,
            )
            total.save()
    else:
        total = TotalPrice.objects.filter(order_id=instance.order_id).get(month=instance.month)

    total.total_price = int(total.total_price) + int(instance.total_price)
    total.save()

@receiver(pre_delete, sender=AdditionalCollect)
def delete_additional_collect(sender, instance, **kwargs):
    
    if instance.order_id:
        total = TotalPrice.objects.filter(order_id=instance.order_id).get(month=instance.month)
    else:
        total = TotalPrice.objects.filter(group_id=instance.group_id).get(month=instance.month)
    total.total_price = int(total.total_price) - int(instance.total_price)
    total.save()


    
