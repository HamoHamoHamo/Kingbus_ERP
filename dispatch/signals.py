from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from common.constant import FORMAT
from django.db.models.signals import post_save, post_delete, pre_delete
from django.db.models import Sum
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import RegularlyGroup, DriverCheck, DispatchRegularlyData, DispatchOrder, DispatchOrderConnect, DispatchRegularlyConnect, DispatchCheck, DrivingHistory
from accounting.models import TotalPrice, AdditionalCollect
from humanresource.models import Salary, Member

import re
import math

@receiver(post_save, sender=DispatchOrder)
def save_order(sender, instance, created, **kwargs):
    if instance.VAT == 'y':
        total_price = int(instance.price) * int(instance.bus_cnt)
    else:
        total_price = int(instance.price) * int(instance.bus_cnt) + math.floor(int(instance.price) * int(instance.bus_cnt) * 0.1 + 0.5)
    print("TESTTTTTTTTTTTTTT", total_price)
    if created:
        total = TotalPrice(
            order_id = instance,
            total_price = total_price,
            month = instance.departure_date[:7],
            creator = instance.creator
        )
        
    else:
        total = get_object_or_404(TotalPrice, order_id=instance)
        total.month = instance.departure_date[:7]
        total.total_price = total_price
        total.creator = instance.creator

    total.save()

    # connects는 view에서 처리
    #connects = instance.info_order.all()
    #for connect in connects:
    #    connect.price = instance.price
    #    connect.driver_allowance = instance.driver_allowance
    #    connect.save()


@receiver(pre_delete, sender=DispatchOrder)
def delete_order(sender, instance, **kwargs):
    collect_list = instance.order_collect.all()
    for collect in collect_list:
        income = collect.income_id
        income.used_price = int(income.used_price) - int(collect.price)
        if int(income.total_income) == income.used_price:
            income.state = '완료'
        else:
            income.state= '미처리'
        income.save()
        collect.delete()

def error_update_total_price(month):
    group_list = RegularlyGroup.objects.order_by('number')
    for group in group_list:
        settlement_date = 1
        last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)

        if int(settlement_date) == 1:
            month2 = month
            settlement_date2 = last_date[8:10]
        else:
            month2 = datetime.strftime(datetime.strptime(f'{month}-01', FORMAT) + relativedelta(months=1), FORMAT)[:7]
            if int(settlement_date) > 9:
                settlement_date2 = int(settlement_date) -1
            else:
                settlement_date2 = f'0{int(settlement_date) -1}'

        if int(settlement_date) < 10:
            settlement_date = f'0{settlement_date}'


        total_price = 0
        date1 = f'{month}-{settlement_date}'
        date2 = f'{month2}-{settlement_date2}'
        connects = DispatchRegularlyConnect.objects.filter(regularly_id__group=group).filter(departure_date__range=(f'{date1} 00:00', f'{date2} 24:00'))
        if connects:
            price = connects.aggregate(Sum('price'))
            total_price += int(price['price__sum'])

        ######### ㅇ
        total_price += math.floor(total_price * 0.1 + 0.5)
        print("group = ", group, total_price)
        additional_list = AdditionalCollect.objects.filter(group_id=group).filter(month=month)
        additional = additional_list.aggregate(Sum('total_price'))
        if additional['total_price__sum']:
            total_additional = int(additional['total_price__sum'])
        else:
            total_additional = 0

        try:
            total = TotalPrice.objects.filter(group_id=group).get(month=month)
            total.total_price = total_price + total_additional
        except TotalPrice.DoesNotExist:
            total = TotalPrice(
                group_id = group,
                month = month,
                total_price = total_price + total_additional,
                creator = group.creator,
            )
        total.save()
    return total

##############
def update_total_price(instance):
    group = instance.regularly_id.group
    settlement_date = group.settlement_date

    if int(instance.departure_date[8:10]) < int(settlement_date):
        month = datetime.strftime(datetime.strptime(instance.departure_date[:10], FORMAT) - relativedelta(months=1), FORMAT)[:7]
    else:
        month = instance.departure_date[:7]

    last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)

    if int(settlement_date) == 1:
        month2 = month
        settlement_date2 = last_date[8:10]
    else:
        month2 = datetime.strftime(datetime.strptime(f'{month}-01', FORMAT) + relativedelta(months=1), FORMAT)[:7]
        if int(settlement_date) > 9:
            settlement_date2 = int(settlement_date) -1
        else:
            settlement_date2 = f'0{int(settlement_date) -1}'

    if int(settlement_date) < 10:
        settlement_date = f'0{settlement_date}'

    ###
    total_price = 0
    date1 = f'{month}-{settlement_date}'
    date2 = f'{month2}-{settlement_date2}'
    connects = DispatchRegularlyConnect.objects.filter(regularly_id__group=group).filter(departure_date__range=(f'{date1} 00:00', f'{date2} 24:00'))
    if connects:
        price = connects.aggregate(Sum('price'))
        total_price += int(price['price__sum'])

    total_price += math.floor(total_price * 0.1 + 0.5)

    additional_list = AdditionalCollect.objects.filter(group_id=group).filter(month=month)
    additional = additional_list.aggregate(Sum('total_price'))
    if additional['total_price__sum']:
        total_additional = int(additional['total_price__sum'])
    else:
        total_additional = 0

    try:
        total = TotalPrice.objects.filter(group_id=group).get(month=month)
        total.total_price = total_price + total_additional
    except TotalPrice.DoesNotExist:
        total = TotalPrice(
            group_id = group,
            month = month,
            total_price = total_price + total_additional,
            creator = instance.creator,
        )
    total.save()
    return total

@receiver(post_save, sender=DispatchRegularlyConnect)
def save_regularly_connect(sender, instance, created, **kwargs):
    month = instance.departure_date[:7]
    creator = instance.creator
    member = instance.driver_id
    if created:
        # DriverCheck 생성
        DriverCheck.objects.create(
            regularly_id = instance,
            creator = creator
        )
        DrivingHistory.objects.create(
            regularly_connect_id = instance,
            creator = creator,
            date = instance.departure_date[:10],
            member = instance.driver_id,
        )

    # Salary 업데이트 안함
    if hasattr(instance, 'not_update_salary'):
        return
    # Salary 업데이트
    try:
        salary = Salary.objects.filter(member_id=member).get(month=month)
        if instance.work_type == '출근':
            order = DispatchRegularlyConnect.objects.filter(work_type='출근').filter(driver_id=member).filter(departure_date__startswith=month).aggregate(Sum('driver_allowance'))
            salary.attendance = int(order['driver_allowance__sum']) if order['driver_allowance__sum'] else 0
        elif instance.work_type == '퇴근':
            order = DispatchRegularlyConnect.objects.filter(work_type='퇴근').filter(driver_id=member).filter(departure_date__startswith=month).aggregate(Sum('driver_allowance'))
            salary.leave = int(order['driver_allowance__sum']) if order['driver_allowance__sum'] else 0
        salary.total = salary.calculate_total()
        # salary.total = int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional) - int(salary.deduction)
        salary.save()
    except Salary.DoesNotExist:
        Salary.new_salary(creator, month, member)

    if not hasattr(instance, 'same_accounting') or not instance.same_accounting:
        print('create update accounting')
        # TotalPrice 업데이트
        total = update_total_price(instance)

@receiver(post_delete, sender=DispatchRegularlyConnect)
def delete_regularly_connect(sender, instance, **kwargs):
    # Salary 업데이트 안함
    if hasattr(instance, 'not_update_salary'):
        return
    
    # Salary 업데이트
    month = instance.departure_date[:7]
    try:
        member = instance.driver_id
        salary = Salary.objects.filter(member_id=member).get(month=month)
        if instance.work_type == '출근':
            order = DispatchRegularlyConnect.objects.filter(work_type='출근').filter(driver_id=member).filter(departure_date__startswith=month).aggregate(Sum('driver_allowance'))
            salary.attendance = int(order['driver_allowance__sum']) if order['driver_allowance__sum'] else 0
        elif instance.work_type == '퇴근':
            order = DispatchRegularlyConnect.objects.filter(work_type='퇴근').filter(driver_id=member).filter(departure_date__startswith=month).aggregate(Sum('driver_allowance'))
            salary.leave = int(order['driver_allowance__sum']) if order['driver_allowance__sum'] else 0
        salary.total = salary.calculate_total()
        # salary.total = int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional) - int(salary.deduction)
        salary.save()
    except Member.DoesNotExist:
        pass
        
    if not hasattr(instance, 'same_accounting') or not instance.same_accounting:
        print("delete update accounting")
        # TotalPrice 업데이트
        total = update_total_price(instance)




@receiver(post_save, sender=DispatchOrderConnect)
def save_connect(sender, instance, created, **kwargs):
    month = instance.departure_date[:7]
    creator = instance.creator
    member = instance.driver_id

    # DriverCheck 생성
    if created:
        DriverCheck.objects.create(
            order_id = instance,
            creator = creator
        )
        DrivingHistory.objects.create(
            order_connect_id = instance,
            creator = creator,
            date = instance.departure_date[:10],
            member = instance.driver_id,
        )

    # Salary 업데이트 안함
    if hasattr(instance, 'not_update_salary'):
        return
    
    
    # Salary 업데이트
    try:
        salary = Salary.objects.filter(member_id=member).get(month=month)
        order = DispatchOrderConnect.objects.filter(driver_id=member).filter(departure_date__startswith=month).filter(payment_method='n').aggregate(Sum('driver_allowance'))
        salary.order = int(order['driver_allowance__sum']) if order['driver_allowance__sum'] else 0

        salary.total = salary.calculate_total()
        # salary.total = int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional) - int(salary.deduction)
        salary.save()
    except Salary.DoesNotExist:
        Salary.new_salary(creator, month, member)
    

@receiver(post_delete, sender=DispatchOrderConnect)
def delete_connect(sender, instance, **kwargs):
    # Salary 업데이트 안함
    if hasattr(instance, 'not_update_salary'):
        return
    
    # Salary 업데이트
    month = instance.departure_date[:7]
    member = instance.driver_id
    
    try:
        salary = Salary.objects.filter(member_id=member).get(month=month)
        order = DispatchOrderConnect.objects.filter(driver_id=member).filter(departure_date__startswith=month).aggregate(Sum('driver_allowance'))
        salary.order = int(order['driver_allowance__sum']) if order['driver_allowance__sum'] else 0
        salary.total = salary.calculate_total()
        # salary.total = int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional) - int(salary.deduction)
        salary.save()
    except Salary.DoesNotExist:
        return
