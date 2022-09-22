from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyConnect, DispatchCheck
from accounting.models import Salary
from humanresource.models import Member

@receiver(post_save, sender=DispatchOrder)
def save_order(sender, instance, created, **kwargs):
    check_list = DispatchCheck.objects.filter(date=instance.departure_date[:10])
    for check in check_list:
        check.dispatch_check = 'n'
        check.member_id1 = None
        check.member_id2 = None
        check.save()        

@receiver(post_save, sender=DispatchRegularlyConnect)
def create_regularly_connect(sender, instance, created, **kwargs):
    if created:
        if instance.regularly_id.work_type == '출근':
            attendance = int(instance.driver_allowance)
            leave = 0
        elif instance.regularly_id.work_type == '퇴근':
            attendance = 0
            leave = int(instance.driver_allowance)
        try:
            salary = Salary.objects.filter(member_id=instance.bus_id.driver).get(month=instance.departure_date[:7])
            salary.attendance = int(salary.attendance) + int(attendance)
            salary.leave = int(salary.leave) + int(leave)
            salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)

        except Salary.DoesNotExist:
            print("Does Not Exist")
            salary = Salary(
                member_id = instance.bus_id.driver,
                attendance=attendance,
                leave=leave,
                order=0,
                additional=0,
                total=attendance + leave,
                remark='',
                month=instance.departure_date[:7],
                creator=instance.creator,
            )
        salary.save()

        check_list = DispatchCheck.objects.filter(date=instance.departure_date[:10])
        for check in check_list:
            check.dispatch_check = 'n'
            check.member_id1 = None
            check.member_id2 = None
            check.save()


@receiver(post_delete, sender=DispatchRegularlyConnect)
def delete_regularly_connect(sender, instance, **kwargs):
    print("test")
    if instance.regularly_id.work_type == '출근':
        attendance = int(instance.driver_allowance)
        leave = 0
    elif instance.regularly_id.work_type == '퇴근':
        attendance = 0
        leave = int(instance.driver_allowance)
    
    try:
        salary = Salary.objects.filter(member_id=instance.bus_id.driver).get(month=instance.departure_date[:7])
        salary.attendance = int(salary.attendance) - int(attendance)
        salary.leave = int(salary.leave) - int(leave)
        salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)
        salary.save()
    except Exception as e:
        print("Error", e)

    check_list = DispatchCheck.objects.filter(date=instance.departure_date[:10])
    for check in check_list:
        check.dispatch_check = 'n'
        check.member_id1 = None
        check.member_id2 = None
        check.save()

# @receiver(post_save, sender=DispatchOrderConnect)
# def create_order_connect(sender, instance, created, **kwargs):
#     price = instance.driver_allowance
#     try:
#         salary = Salary.objects.filter(member_id=instance.bus_id.driver).get(month=instance.departure_date[:7])
#         salary.order = int(salary.order) + int(price)
#         salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)

#     except Salary.DoesNotExist:
#         print("Does Not Exist")
#         salary = Salary(
#             member_id = instance.bus_id.driver,
#             attendance=0,
#             leave=0,
#             order=price,
#             additional=0,
#             total=price,
#             remark='',
#             month=instance.departure_date[:7],
#             creator=instance.creator,
#         )
#     salary.save()

#     check_list = DispatchCheck.objects.filter(date__range=(instance.departure_date[:10], instance.arrival_date[:10]))
#     for check in check_list:
#         check.dispatch_check = 'n'
#         check.member_id1 = None
#         check.member_id2 = None
#         check.save()


# @receiver(post_delete, sender=DispatchOrderConnect)
# def delete_order_connect(sender, instance, **kwargs):
#     print("test")
#     price = instance.driver_allowance
#     try:
#         salary = Salary.objects.filter(member_id=instance.bus_id.driver).get(month=instance.departure_date[:7])
#         salary.order = int(salary.order) - int(price)
#         salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)
#         salary.save()
#     except Exception as e:
#         print("Error", e)

#     check_list = DispatchCheck.objects.filter(date__range=(instance.departure_date[:10], instance.arrival_date[:10]))
#     for check in check_list:
#         check.dispatch_check = 'n'
#         check.member_id1 = None
#         check.member_id2 = None
#         check.save()
