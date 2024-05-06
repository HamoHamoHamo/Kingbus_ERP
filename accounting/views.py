import json
import my_settings
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from dispatch.models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyConnect, DispatchRegularly, RegularlyGroup, DispatchRegularlyData
from django.db.models import Sum, F
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import BadRequest
from config import settings
from popbill import EasyFinBankService
import math
import time

from common.constant import TODAY, WEEK
from common.datetime import *

from .models import Income, LastIncome, AdditionalCollect, Collect, TotalPrice
from .forms import IncomeForm, AdditionalCollectForm
from crudmember.models import Category
from dispatch.views import FORMAT
from humanresource.models import Member, Salary

TODAY = str(datetime.now())[:10]
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]
WEEK2 = ['월', '화', '수', '목', '금', '토', '일', ]

# settings.py 작성한 LinkID, SecretKey를 이용해 EasyFinBankService 서비스 객체 생성
easyFinBankService = EasyFinBankService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
easyFinBankService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
easyFinBankService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
easyFinBankService.UseStaticIP = settings.UseStaticIP

#로컬시스템 시간 사용여부, 권장(True)
easyFinBankService.UseLocalTimeYN = settings.UseLocalTimeYN


class SalesList(generic.ListView):
    template_name = 'accounting/income.html'
    context_object_name = 'dispatch_list'
    model = DispatchOrder

    def get_queryset(self):
        month = self.request.GET.get('month', TODAY[:7])
        dispatch_list = DispatchOrder.objects.filter(departure_date__startswith=month).exclude(contract_status='취소')

        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        get_month = self.request.GET.get('month', TODAY[:7])

        yearly_sales = []
        for i in range(12):
            if i+1 < 10:
                month = f'{get_month[:4]}-0{i+1}'
            else:
                month = f'{get_month[:4]}-{i+1}'

            regularly_sales = TotalPrice.objects.filter(month=month).exclude(group_id=None).aggregate(Sum('total_price'))['total_price__sum']
            order_sales = TotalPrice.objects.filter(month=month).exclude(order_id__contract_status='취소').exclude(order_id=None).aggregate(Sum('total_price'))['total_price__sum']
            regularly_collect = Collect.objects.filter(month=month).exclude(group_id=None).aggregate(Sum('price'))['price__sum']
            order_collect = Collect.objects.filter(month=month).exclude(order_id=None).aggregate(Sum('price'))['price__sum']


            regularly_sales_price = 0
            order_sales_price = 0
            

            if regularly_sales:
                regularly_sales_price = int(regularly_sales)
            if order_sales:
                order_sales_price = int(order_sales)

            regularly_outstanding_price = regularly_sales_price
            order_outstanding_price = order_sales_price

            if regularly_collect:
                regularly_outstanding_price = regularly_sales_price - int(regularly_collect)
            if order_collect:
                order_outstanding_price = order_sales_price - int(order_collect)


            total_sales_price = regularly_sales_price + order_sales_price
            
            yearly_sales.append({
                'total_sales': total_sales_price,
                'regularly_sales': regularly_sales_price,
                'order_sales': order_sales_price,
            })

            if month == get_month:
                monthly_sales = {
                'total_sales': total_sales_price,
                'regularly_sales': regularly_sales_price,
                'order_sales': order_sales_price,
                'regularly_outstanding': regularly_outstanding_price,
                'order_outstanding': order_outstanding_price,
                }

        context['monthly_sales'] = monthly_sales
        context['yearly_sales'] = yearly_sales
        #########
        
        category_list = Category.objects.filter(type='유형')
        type_cnt = {}
        bus_cnt = {}
        sales = {}
        for category in category_list:
            type_cnt[category.category] = 0
            bus_cnt[category.category] = 0
            sales[category.category] = 0

        # 운행 유형 선택 안된 
        type_cnt['x'] = 0
        bus_cnt['x'] = 0
        sales['x'] = 0

        payment = {}

        for order in context['dispatch_list']:
            if order.order_type :
                type_cnt[order.order_type] += 1
                bus_cnt[order.order_type] += int(order.bus_cnt)
                sales[order.order_type] += int(order.bus_cnt) * int(order.price)
            else:
                type_cnt['x'] += 1
                bus_cnt['x'] += int(order.bus_cnt)
                sales['x'] += int(order.bus_cnt) * int(order.price)
            try:
                payment[order.payment_method] += 1
            except KeyError:
                payment[order.payment_method] = 1

        context['payment'] = payment

        order_type = {
            'type_cnt': type_cnt,
            'bus_cnt': bus_cnt,
            'sales': sales,
        }
        context['order_type'] = order_type

        work_type_cnt = {
            'attendance': DispatchRegularlyConnect.objects.filter(departure_date__startswith=get_month).filter(work_type='출근').count(),
            'leave': DispatchRegularlyConnect.objects.filter(departure_date__startswith=get_month).filter(work_type='퇴근').count(),
            'order': context['dispatch_list'].count(),
        }
        context['work_type_cnt'] = work_type_cnt

        context['month'] = get_month
        return context

class RegularlyCollectList(generic.ListView):
    template_name = 'accounting/regularly_collect.html'
    context_object_name = 'group_list'
    model = RegularlyGroup

    def get_queryset(self):
        group_list = RegularlyGroup.objects.prefetch_related('regularly_monthly').all().order_by('number', 'name')
        
        return group_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #쿼리 줄일 방법 생각
        month = self.request.GET.get('date', TODAY[:7])
        context['month'] = month
        creator = get_object_or_404(Member, pk=self.request.session.get('user'))

        contract_price_list = []
        settlement_list = []
        additional_list = []

        value_list = []
        VAT_list = []
        additional_price_list = []
        total_list = []
        state_list = []
        outstanding_list = []
        #
        income_list = []
        

        last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
        

        for group in context['group_list']:
            collect_list = Collect.objects.filter(group_id=group).filter(month=month)
            temp_list = []
            price_total = 0

            for collect in collect_list:
                temp_list.append({
                    'serial': collect.income_id.serial,
                    'date': collect.income_id.date,
                    'payment_method': collect.income_id.payment_method,
                    'bank': collect.income_id.bank,
                    'commission': collect.income_id.commission,
                    'acc_income': collect.income_id.acc_income,
                    'depositor': collect.income_id.depositor,
                    'state': collect.income_id.state,
                    'price': collect.price,
                    'id': collect.id,
                })
                price_total += int(collect.price)
            income_list.append(temp_list)
            
            # 정산기간
            settle_date = group.settlement_date
            if int(settle_date) < 10:
                settle_date = f'0{settle_date}'
            settle_month = month[5:7]

            
            if group.settlement_date == '1':
                
                n_settle_date = last_date[8:]
                n_settle_month = settle_month
                settlement = f'{month[2:4]}/{settle_month}/{settle_date} ~ {month[2:4]}/{n_settle_month}/{n_settle_date}'

            else:
                if int(settle_month) > 8:
                    n_settle_month = int(settle_month) + 1
                else:
                    n_settle_month = f'0{int(settle_month) + 1}'
                
                if int(settle_date) > 9:
                    n_settle_date = int(settle_date) - 1
                else:
                    n_settle_date = f'0{int(settle_date) - 1}'
                                        
                settlement = f'{month[2:4]}/{settle_month}/{settle_date} ~ {month[2:4]}/{n_settle_month}/{n_settle_date}'

            settlement_list.append(settlement)
            ##
            ##########RegularlyTotalPrice에서 불러오게 수정
            # regularly_list = group.regularly_info.all()
            # temp_t_price = 0
            
            # for regularly in regularly_list:
            #     date1 = f'{month[:4]}-{settle_month}-{settle_date}'
            #     date2 = f'{month[:4]}-{n_settle_month}-{n_settle_date}'
            #     connects = regularly.info_regularly.filter(departure_date__range=(date1, date2))
            #     if connects:
            #         price = connects.aggregate(Sum('regularly_id__price'))
            #         temp_t_price += int(price['regularly_id__price__sum'])
            # ######### ㅇ
            
            # contract_price_list.append(temp_t_price)
            
            #########################
            # if temp_t_price != 0:
            #     total = TotalPrice(
            #         group_id = group,
            #         month = month,
            #         total_price = temp_t_price,
            #         creator = creator
            #     )
            #     total.save()
            #######################
            additionals = AdditionalCollect.objects.filter(group_id=group).filter(month=month)
            
            temp_value = 0
            temp_VAT = 0
            temp_additional = 0

            temp_list = []
            for additional in additionals:
                temp_additional += int(additional.total_price)
                

                temp_list.append({
                    'category': additional.category,
                    'value': additional.value,
                    'VAT': additional.VAT,
                    'total_price': additional.total_price,
                    'note': additional.note,
                    'id': additional.id
                })
                
            try:
                total = TotalPrice.objects.filter(group_id=group).get(month=month)
                total_list.append(int(total.total_price))
                contract_price_list.append(math.floor((total_list[-1] - temp_additional) / 1.1 + 0.5))
            except TotalPrice.DoesNotExist:
                total_list.append(0)
                contract_price_list.append(0)

            additional_price_list.append(temp_additional)
            value_list.append(temp_value + contract_price_list[-1])
            VAT_list.append(temp_VAT + math.floor(contract_price_list[-1] * 0.1 + 0.5))
            

            additional_list.append(temp_list)

            if price_total == total_list[-1]:
                state_list.append('완료')
                outstanding_list.append(0)
            else:
                state_list.append('미처리')
                outstanding_list.append(total_list[-1] - price_total)

        context['additional_price_list'] = additional_price_list
        context['value_list'] = value_list
        context['VAT_list'] = VAT_list
        context['total_list'] = total_list    
        
        context['income_list'] = income_list
        context['contract_price_list'] = contract_price_list
        context['settlement_list'] = settlement_list
        context['additional_list'] = additional_list
        context['state_list'] = state_list
        context['outstanding_list'] = outstanding_list
        
        return context

def r_collect_create(request):
    if request.method == 'POST':
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        group_id_list = request.POST.getlist('group_id')
        income_id = request.POST.get('income_id')
        income = get_object_or_404(Income, id=income_id)
        month = request.POST.get('month')
        for group_id in group_id_list:
            group = get_object_or_404(RegularlyGroup, id=group_id)

            try:
                total = TotalPrice.objects.filter(group_id=group).get(month=month)
            except TotalPrice.DoesNotExist:
                total = TotalPrice(
                    group_id = group,
                    month = month,
                    total_price = 0,
                    creator = creator
                )
                total.save()
            collect_list = Collect.objects.filter(group_id=group)
            collect_price = collect_list.aggregate(Sum('price'))['price__sum']

            if collect_price:
                n_total_price = int(total.total_price) - int(collect_price)
            else:
                n_total_price = int(total.total_price)

            if n_total_price < int(income.total_income) - int(income.used_price):
                price = n_total_price
            else:
                price = int(income.total_income) - int(income.used_price)

            collect = Collect(
                group_id = group,
                income_id = income,
                price = price,
                month = month,
                creator = creator
            )
            collect.save()
            used_price = int(income.used_price) + int(price)
            income.used_price = used_price
            if int(used_price) == int(income.total_income):
                income.state = '완료'
            income.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
    
        return HttpResponseNotAllowed(['post'])

def r_additional_collect_create(request):
    if request.method == 'POST':
        r_additional_form = AdditionalCollectForm(request.POST)
        if r_additional_form.is_valid():
            id = request.POST.get('id')
            month = request.POST.get('month')
            group = get_object_or_404(RegularlyGroup, id=id)
            creator = get_object_or_404(Member, pk=request.session.get('user'))
            
            r_additional = r_additional_form.save(commit=False)
            r_additional.group_id = group
            r_additional.total_price = int(r_additional.value) + int(r_additional.VAT)
            r_additional.month = month
            r_additional.creator = creator
            r_additional.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest
    else:
        return HttpResponseNotAllowed(['post'])


def r_additional_collect_delete(request):
    if request.method == 'POST':
        id_list = request.POST.getlist('id')

        for id in id_list:
            additional = get_object_or_404(AdditionalCollect, id=id)
            additional.delete()
        

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def regularly_load(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        group_id = post_data['group_id']
        date1 = post_data['date1']
        date2 = post_data['date2']

        group = get_object_or_404(RegularlyGroup, id=group_id)

        regularly_list = DispatchRegularlyData.objects.filter(group=group)

        # regularly_list = DispatchRegularly.objects.prefetch_related('info_regularly').filter(group=group)
        
        temp_list = []
        try:
            for regularly_data in regularly_list:
                regularly = regularly_data.monthly.filter(edit_date__lte=date2).order_by('-edit_date').first()
                if not regularly:
                    regularly = regularly_data.monthly.filter(edit_date__gte=date2).order_by('edit_date').first()
                
                cnt = DispatchRegularlyConnect.objects.filter(regularly_id__regularly_id=regularly_data).filter(departure_date__range=(f'{date1} 00:00', f'{date2} 24:00')).count()
                # cnt = regularly.info_regularly.filter(departure_date__range=(f'{date1} 00:00', f'{date2} 24:00')).count(),
                # cnt = cnt[0]
                supply_price = int(regularly.price) * int(cnt)
                VAT = math.floor(supply_price * 0.1 + 0.5)

                temp_list.append({
                    'duration': f'{date1} ~ {date2}',
                    'week': regularly.week,
                    'type': regularly.work_type,
                    'route': regularly.route,
                    'cnt': cnt,
                    'contract_price': regularly.price,
                    'supply_price': int(regularly.price) * int(cnt),
                    'VAT': VAT,
                })
            

            # for regularly in regularly_list:
            #     cnt = regularly.info_regularly.filter(departure_date__range=(f'{date1} 00:00', f'{date2} 24:00')).count(),
            #     cnt = cnt[0]
            #     supply_price = int(regularly.price) * int(cnt)
            #     print(supply_price)
            #     VAT = math.floor(supply_price * 0.1 + 0.5)

            #     temp_list.append({
            #         'duration': f'{date1} ~ {date2}',
            #         'week': regularly.week,
            #         'type': regularly.work_type,
            #         'route': regularly.route,
            #         'cnt': cnt,
            #         'contract_price': regularly.price,
            #         'supply_price': int(regularly.price) * int(cnt),
            #         'VAT': VAT,
            #     })
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': f'{e}'})
            
        return JsonResponse({'status': 'success', 'dataList': temp_list})
    else:
        return HttpResponseNotAllowed(['post'])


class CollectList(generic.ListView):
    template_name = 'accounting/collect.html'
    context_object_name = 'dispatch_list'
    model = DispatchOrder

    def get_queryset(self):
        date1 = self.request.GET.get('date1', f'{TODAY[:7]}-01')
        date2 = self.request.GET.get('date2', TODAY)
        select = self.request.GET.get('select', '')
        search = self.request.GET.get('search', '')

        dispatch_list = DispatchOrder.objects.prefetch_related('order_collect').exclude(contract_status='취소').filter(departure_date__lte=f'{date2} 24:00').filter(arrival_date__gte=f'{date1} 00:00').order_by('departure_date')
        if search and select == '예약자':
            dispatch_list = dispatch_list.filter(customer__contains=search)
        elif search and select == '노선':
            dispatch_list = dispatch_list.filter(route__contains=search)
        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date1'] = self.request.GET.get('date1', f'{TODAY[:7]}-01')
        context['date2'] = self.request.GET.get('date2', TODAY)
        context['search'] = self.request.GET.get('search', '')
        context['select'] = self.request.GET.get('select', '')

        dispatch_count = context['dispatch_list'].count()
        income_list = []
        value_list = [0] * dispatch_count
        VAT_list = [0] * dispatch_count
        total_list = []
        state_list = []
        outstanding_list = []
        additional_list = []
        additional_total_list = [0] * dispatch_count
        cnt = 0
        for order in context['dispatch_list']:
            total_price = int(get_object_or_404(TotalPrice, order_id=order).total_price)
            total_list.append(total_price)
            order_total = int(order.price) * int(order.bus_cnt)
            if order.VAT == 'y':
                value_list[cnt] = math.floor(order_total / 1.1 + 0.5)
                VAT_list[cnt] = math.floor(value_list[cnt] * 0.1 + 0.5)
                total = value_list[cnt] + VAT_list[cnt]
                zero = order_total - total
                if zero != 0:
                    VAT_list[cnt] += zero
            else:
                value_list[cnt] = int(order.price) * int(order.bus_cnt)
                VAT_list[cnt] = math.floor(value_list[cnt] * 0.1 + 0.5)
            
            collect_list = order.order_collect.select_related('income_id').all()
            temp_list = []
            price_total = 0
            for collect in collect_list:
                temp_list.append({
                    'serial': collect.income_id.serial,
                    'date': collect.income_id.date,
                    'payment_method': collect.income_id.payment_method,
                    'bank': collect.income_id.bank,
                    'commission': collect.income_id.commission,
                    'acc_income': collect.income_id.acc_income,
                    'depositor': collect.income_id.depositor,
                    'state': collect.income_id.state,
                    'price': collect.price,
                    'id': collect.id,
                })
                price_total += int(collect.price)
            income_list.append(temp_list)
            
            additionals = AdditionalCollect.objects.filter(order_id=order)
            
            temp_list = []
            for additional in additionals:
                temp_list.append({
                    'category': additional.category,
                    'value': additional.value,
                    'VAT': additional.VAT,
                    'total_price': additional.total_price,
                    'note': additional.note,
                    'id': additional.id
                })
                
                additional_total_list[cnt] += int(additional.total_price)
            additional_list.append(temp_list)

            if int(price_total) == total_list[cnt]:
                state_list.append('완료')
                outstanding_list.append('0')
            else:
                state_list.append('미처리')
                outstanding_list.append(total_list[cnt] - int(price_total))

            cnt += 1

        context['month'] = self.request.GET.get('month', TODAY[:7])
        context['income_list'] = income_list
        context['value_list'] = value_list
        context['VAT_list'] = VAT_list
        context['total_list'] = total_list
        context['additional_list'] = additional_list
        context['additional_total_list'] = additional_total_list
        context['state_list'] = state_list
        context['outstanding_list'] = outstanding_list

        return context


def collect_create(request):
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_id_list = request.POST.getlist('order_id')
        income_id = request.POST.get('income_id')
        income = get_object_or_404(Income, id=income_id)
        for order_id in order_id_list:
            order = get_object_or_404(DispatchOrder, id=order_id)
            total = TotalPrice.objects.get(order_id=order)
            collect_list = Collect.objects.filter(order_id=order)
            collect_price = collect_list.aggregate(Sum('price'))['price__sum']
            
            if collect_price:
                n_total_price = int(total.total_price) - int(collect_price)
            else:
                n_total_price = int(total.total_price)

            if n_total_price < int(income.total_income) - int(income.used_price):
                price = n_total_price
            else:
                price = int(income.total_income) - int(income.used_price)
            collect = Collect(
                order_id = order,
                income_id = income,
                price = price,
                month = order.departure_date[:7],
                creator = creator
            )
            collect.save()
            used_price = int(income.used_price) + int(price)
            income.used_price = used_price
            if int(used_price) == int(income.total_income):
                income.state = '완료'
            income.save()
        
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def collect_delete(request):
    if request.method == "POST":
        id_list = request.POST.getlist('id')
        for id in id_list:
            collect = get_object_or_404(Collect, id=id)
            income = collect.income_id
            income.used_price = int(income.used_price) - int(collect.price)
            if income.used_price == income.total_income:
                income.state = '완료'
            else:
                income.state = '미처리'
            income.save()
            collect.delete()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def collect_load(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        date1 = post_data['date1']
        date2 = post_data['date2']
        depositor = post_data['depositor']
        income_list = Income.objects.filter(date__range=(f'{date1} 00:00', f'{date2} 24:00')).exclude(state='삭제')
        if depositor:
            income_list = income_list.filter(depositor__contains=depositor)

        temp_list = []
        for income in income_list:
            if income.used_price != income.total_income:
                temp_list.append({
                    'serial': income.serial,
                    'date': income.date,
                    'payment_method': income.payment_method,
                    'commission': income.commission,
                    'total_income': income.total_income,
                    'used_price': income.used_price,
                    'depositor': income.depositor,
                    'state': income.state,
                    'id': income.id,
                })
        return JsonResponse({
            'deposit': temp_list,
            'status': 'success',
            })
    else:
        return HttpResponseNotAllowed(['post'])

def additional_collect_create(request):
    if request.method == "POST":
        additional_form = AdditionalCollectForm(request.POST)
        if additional_form.is_valid():
            id = request.POST.get('id')
            order = get_object_or_404(DispatchOrder, id=id)
            creator = get_object_or_404(Member, pk=request.session.get('user'))
            
            additional = additional_form.save(commit=False)
            additional.order_id = order
            additional.total_price = int(additional.value) + int(additional.VAT)
            additional.creator = creator
            additional.month = order.departure_date[:7]
            additional.save()
            
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest
    else:
        return HttpResponseNotAllowed(['post'])

def additional_collect_delete(request):
    if request.method == "POST":
        # order_id = request.POST.get('order_id')
        id_list = request.POST.getlist('id')

        for id in id_list:
            additional = get_object_or_404(AdditionalCollect, id=id)
            order = additional.order_id
            
            additional.delete()

        

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])



class DepositList(generic.ListView):
    template_name = 'accounting/deposit.html'
    context_object_name = 'income_list'
    model = Income

    def get_queryset(self):
        self.date1 = self.request.GET.get('date1', f'{TODAY[:7]}-01')
        self.date2 = self.request.GET.get('date2', TODAY)
        self.select = self.request.GET.get('select')
        self.search = self.request.GET.get('search', '')
        self.payment = self.request.GET.get('payment')
        
        income_list = Income.objects.filter(date__range=(f'{self.date1} 00:00', f'{self.date2} 24:00')).order_by('-serial', '-date')
        if self.search:
            if self.select == 'depositor':
                income_list = income_list.filter(depositor__contains=self.search)
            elif self.select == 'bank':
                income_list = income_list.filter(bank__contains=self.search)
            elif self.select == 'acc_income':
                income_list = income_list.filter(acc_income__contains=self.search)
        if self.payment:
            income_list = income_list.filter(payment_method=self.payment)

        return income_list
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date1'] = self.date1
        context['date2'] = self.date2
        context['select'] = self.select
        context['search'] = self.search
        context['payment'] = self.payment

        data_list = []

        collect_list = []

        for income in context['income_list']:
            data_list.append({
                'date': income.date,
                'payment_method': income.payment_method,
                'bank': income.bank,
                'commission': income.commission,
                'acc_income': income.acc_income,
                'depositor': income.depositor,
                'state': income.state,
            })
            collects = Collect.objects.select_related('order_id', 'group_id').filter(income_id=income)
            temp_collect = []
            for collect in collects:
                order = collect.order_id
                group = collect.group_id
                if order:
                    total_price = get_object_or_404(TotalPrice, order_id=order)
                    temp_collect.append({
                        'type': '일반',
                        'name': order.route,
                        'date1': order.departure_date,
                        'date2': order.arrival_date,
                        'price': total_price.total_price,
                        'used_price': collect.price
                    })
                else:
                    # 정산기간
                    month = collect.month
                    last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
                    settle_date = group.settlement_date
                    if int(settle_date) < 10:
                        settle_date = f'0{settle_date}'
                    settle_month = month[5:7]

                    
                    if group.settlement_date == '1':
                        
                        n_settle_date = last_date[8:]
                        n_settle_month = settle_month
                        settlement = f'{month[2:4]}-{settle_month}-{settle_date}'
                        settlement2 = f'{month[2:4]}-{n_settle_month}-{n_settle_date}'

                    else:
                        if int(settle_month) > 8:
                            n_settle_month = int(settle_month) + 1
                        else:
                            n_settle_month = f'0{int(settle_month) + 1}'
                        
                        if int(settle_date) > 9:
                            n_settle_date = int(settle_date) - 1
                        else:
                            n_settle_date = f'0{int(settle_date) - 1}'
                                                
                        settlement = f'{month[2:4]}-{settle_month}-{settle_date}'
                        settlement2 = f'{month[2:4]}-{n_settle_month}-{n_settle_date}'
                    #
                    total_price = TotalPrice.objects.filter(group_id=group).get(month=collect.month).total_price
                    temp_collect.append({
                        'type': '출/퇴근',
                        'name': group.name,
                        'date1': "20" + settlement,
                        'date2': "20" + settlement2,
                        'price': total_price,
                        'used_price': collect.price,
                    })
            collect_list.append(temp_collect)

        context['collect_list'] = collect_list
        context['data_list'] = data_list
        return context

def load_deposit_data(request):
    if request.method == 'POST':
        last_income = LastIncome.objects.last()
        creator = get_object_or_404(Member, pk=request.session.get('user'))

        result = []
        cnt_list = []
        for i in range(my_settings.ACC_CNT):
                
            CorpNum = my_settings.CORPNUM
            BankCode = my_settings.BANKCODE[i]
            AccountNumber = my_settings.ACCOUNTNUMBER[i]
            if last_income:
                SDate = last_income.tr_date[:8]
                last_save_date = last_income.tr_date
            else:
                SDate = datetime.strftime(datetime.strptime(TODAY, FORMAT) - relativedelta(months=1), '%Y%m%d')
                last_save_date = SDate
            EDate = TODAY

            jobID = easyFinBankService.requestJob(CorpNum, BankCode, AccountNumber, SDate, EDate, UserID=None)
            state = easyFinBankService.getJobState(CorpNum, jobID, UserID=None)
            count = 0
            while state.jobState == 2 and count < 10:
                time.sleep(2)
                state = easyFinBankService.getJobState(CorpNum, jobID, UserID=None)
                print('wait...........')
                print('errorcode', state.errorCode)
                print('jobState', state.jobState)
                
                count += 1
            if count > 9:
                return JsonResponse(
                    {
                        'status': 'timeout',
                        'errorReason': state.errorReason,
                        'jobState': state.jobState,
                        'errorCode': state.errorCode,
                    }
                )
            if state.jobState == 3 and state.errorCode == 1:
                temp_result = easyFinBankService.search(CorpNum, jobID, TradeType='I', SearchString='', Page=1, PerPage=100, Order='D', UserID=None)
                count = 0
                cnt_list.append(temp_result.total)
                result += temp_result.list

            else:
                return JsonResponse(
                    {
                        'status': state.errorReason,
                        'errorReason': state.errorReason,
                        'jobState': state.jobState,
                        'errorCode': state.errorCode,
                    }
                )
        ########### 데이터 불러오기 완료
        data_list = []
        cnt = 1
        list_cnt = 0
        result_cnt = cnt_list[list_cnt]
        for r in result:
            if cnt > result_cnt:
                list_cnt += 1
                cnt = 0
                result_cnt = cnt_list[list_cnt]

            serial=f'{r.trdate}-{r.trserial}'
            date=f'{r.trdt[:4]}-{r.trdt[4:6]}-{r.trdt[6:8]} {r.trdt[8:10]}:{r.trdt[10:12]}'
            depositor=r.remark1
            bank=my_settings.BANK[list_cnt]
            acc_income=r.accIn

            
            data_list.append({
                'serial': serial,
                'date': date,
                'depositor': depositor,
                'bank': bank,
                'acc_income': acc_income,
                'total_income': acc_income,
                'trdt': r.trdt,
            })
            cnt += 1

            # print('id', r.tid)
            # print('serial', serial)
            # print('date', date)
            # print('depositor', depositor)
            # print('bank', bank)
            # print('acc_income', acc_income, '\n')
        
        if data_list:
            data_list = sorted(data_list, key= lambda x: x['date'])
            last = LastIncome(
                tr_date=data_list[-1]['trdt'],
                creator=creator 
            )
            last.save()
            
            latest_date = data_list[0]['trdt'][:8]
            date_cnt = 1 + Income.objects.filter(serial__startswith=latest_date).count()
        
            cnt = 0
        for data in data_list:
            if data['trdt'] > last_save_date:
                cnt += 1
                if latest_date != data['trdt'][:8]:
                    latest_date = data['trdt'][:8]
                    date_cnt = 1 + Income.objects.filter(serial__startswith=latest_date).count()
                # print("AAAA", date_cnt)
                income = Income(
                    serial = f'{latest_date[2:4]}/{latest_date[4:6]}/{latest_date[6:8]}-{date_cnt}',
                    date = data['date'],
                    depositor = data['depositor'],
                    bank = data['bank'],
                    acc_income = data['acc_income'],
                    total_income = data['acc_income'],
                    creator = creator,
                )
                income.save()
                # print(income)
                date_cnt += 1

        return JsonResponse({
            'count': cnt,
            'status': 'success',
        })
    else:
        return HttpResponseNotAllowed(['post'])

def deposit_create(request):
    if request.method == "POST":
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            date = income_form.cleaned_data['date']
            income_cnt = Income.objects.filter(date__startswith=date).count()
            commission = request.POST.get('commission', 0)
            if not commission:
                commission = 0
            
            income = income_form.save(commit=False)
            income.serial = f'{date[:4]}{date[5:7]}{date[8:10]}-{int(income_cnt)+1}'
            income.commission = commission
            income.total_income = int(income.acc_income) + int(commission)
            income.creator = get_object_or_404(Member, pk=request.session.get('user'))
            income.save()
        else:
            raise BadRequest('Invalid request')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def deposit_hide(request):
    if request.method == "POST":
        check_list = request.POST.getlist('check')

        for check in check_list:
            income = get_object_or_404(Income, id=check)
            income.state='삭제'
            income.save()
       
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def deposit_delete(request):
    if request.method == "POST":
        check_list = request.POST.getlist('check')

        for check in check_list:
            income = get_object_or_404(Income, id=check)
            income.delete()
       
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def deposit_edit(request):
    if request.method == "POST":
        income = get_object_or_404(Income, id=request.POST.get('id'))
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            date = income_form.cleaned_data['date']
            income_cnt = Income.objects.filter(date__startswith=date).count()

            income.date = income_form.cleaned_data['date']
            income.depositor = income_form.cleaned_data['depositor']
            income.payment_method = income_form.cleaned_data['payment_method']
            income.bank = income_form.cleaned_data['bank']
            income.acc_income = income_form.cleaned_data['acc_income']
            income.serial = f'{date[:4]}{date[5:7]}{date[8:10]}-{int(income_cnt)+1}'
            income.commission = request.POST.get('commission', '0')
            income.total_income = int(income_form.cleaned_data['acc_income']) + int(request.POST.get('commission', '0'))
            income.creator = get_object_or_404(Member, pk=request.session.get('user'))
            income.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest('Invalid request')
    else:
        return HttpResponseNotAllowed(['post'])
        
class MemberEfficiencyList(generic.ListView):
    template_name = 'accounting/member_efficiency.html'
    context_object_name = 'member_list'
    model = Member

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        # route = self.request.GET.get('route', '')

        member_list = Member.objects.filter(use='사용').order_by('-authority', 'name')
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creator = Member.objects.get(pk=self.request.session.get('user'))
        FUEL = 1600         #기름값
        EFFICIENCY = 2.5    # 연비

        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        
        month = date1[:7] #  급여날짜 어떻게 할 지 확인 필요

        last_day = last_day_of_month(date1)
        date_period = calculate_date_difference(date1, date2)
        date_period = date_period if date_period > 0 else 1

        date_type = self.request.GET.get('dateType', '')
        # if date_type == 'monthly':
        #     date1 = f'{month}-01'
        #     date2 = f'{month}-{last_day}'
        # elif date_type == 'weekly':
        #     date2 = add_days_to_date(date1, 7)
        # elif date_type == 'daily':
        #     date2 = date1

        context['date1'] = date1
        context['date2'] = date2
        context['date_type'] = date_type
        datetime1 = f'{date1} 00:00'
        datetime2 = f'{date2} 24:00'
        

        data_list = []
        total_data = {
            'salary' : 0,
            'price' : 0,
            'driving_cnt' : 0,
            'distance' : 0,
            'driving_distance' : 0,
            'minutes' : 0,
            'driving_minutes' : 0,
            'fuel_cost' : 0,
            'driving_fuel_cost' : 0,
            'tolerance_distance' : 0,
            'tolerance_time' : 0,
        }
        for member in context['member_list']:
            data = {}

            # 노선운행량
            order_connect_list = member.info_driver_id.exclude(arrival_date__lt=datetime1).exclude(departure_date__gt=datetime2).values('price', 'driver_allowance', 'departure_date', 'arrival_date')
            regularly_connect_list = member.info_regularly_driver_id.exclude(arrival_date__lt=datetime1).exclude(departure_date__gt=datetime2).values('price', 'regularly_id__distance', 'driver_allowance', 'departure_date', 'arrival_date')
            if not order_connect_list and not regularly_connect_list:
                continue
            
            driving_history_list = member.driving_history_member.exclude(date__lt=date1).exclude(date__gt=date2).values('departure_date', 'arrival_date', 'departure_km', 'arrival_km')

            data['member'] = member

            # 급여
            try:
                salary = Salary.objects.filter(member_id=member).get(month=month)
            except Salary.DoesNotExist:
                creator = creator
                salary = Salary.new_salary(creator, month, member)

            driving_minutes = 0
            driving_distance = 0

            for history in driving_history_list:
                if history['departure_date'] and history['arrival_date']:
                    driving_minutes += calculate_time_difference(history['departure_date'], history['arrival_date'])
                if history['arrival_km'] and history['departure_km']:
                    driving_distance += int(history['arrival_km']) - int(history['departure_km'])
            
            data['driving_distance'] = driving_distance
            data['driving_minute'] = driving_minutes % 60
            data['driving_hour'] = driving_minutes // 60

            price = 0
            allowance = 0
            minutes = 0
            distance = 0

            for connect in order_connect_list:
                price += int(connect['price'])
                allowance += int(connect['driver_allowance'])
                # distance += connect['order_id__distance']
                minutes += calculate_time_difference(connect['departure_date'], connect['arrival_date'])

            for connect in regularly_connect_list:
                price += int(connect['price'])
                allowance += int(connect['driver_allowance'])
                distance += float(connect['regularly_id__distance']) if connect['regularly_id__distance'] else 0
                minutes += calculate_time_difference(connect['departure_date'], connect['arrival_date'])

            data['distance'] = round(distance, 1)
            data['minute'] = minutes % 60
            data['hour'] = math.floor(minutes / 60)
            
            data['driving_cnt'] = order_connect_list.count() + regularly_connect_list.count()
            data['price'] = price

            fixed_personnel_expense = salary.calculate_fixed() * int(date_period) // int(last_day)
            data['salary'] = fixed_personnel_expense + allowance
            data['driving_fuel_cost'] = round(data['driving_distance'] / EFFICIENCY * FUEL)
            data['fuel_cost'] = round(data['distance'] / EFFICIENCY * FUEL)
            data['tolerance_distance'] = round(data['driving_distance'] - data['distance'], 1)
            data['tolerance_time'] = get_hour_minute(driving_minutes - minutes)

            # 등급(효율) 매출액에서-유류비-사고-인건비-차량비-부대비용=순이익, 순이익/임금*100=
            # 100% S,90% A,80%B,70%C,60%D,50%E,40%이하F 

            # 순이익
            profit = (price - data['fuel_cost'] - allowance)


            
            
            if data['salary'] == 0:
                data['grade'] = ''
            else:
                grade_percent = profit / data['salary'] * 100
                if grade_percent > 90:
                    data['grade'] = 'S' + " " + str(round(grade_percent, 1))
                elif grade_percent > 80:
                    data['grade'] = 'A' + " " + str(round(grade_percent, 1))
                elif grade_percent > 70:
                    data['grade'] = 'B' + " " + str(round(grade_percent, 1))
                elif grade_percent > 60:
                    data['grade'] = 'C' + " " + str(round(grade_percent, 1))
                elif grade_percent > 50:
                    data['grade'] = 'D' + " " + str(round(grade_percent, 1))
                elif grade_percent > 40:
                    data['grade'] = 'E' + " " + str(round(grade_percent, 1))
                elif grade_percent <= 40:
                    data['grade'] = 'F' + " " + str(round(grade_percent, 1))

            data_list.append(data)

            context['data_list'] = data_list

            total_data['salary'] += data['salary']
            total_data['price'] += data['price']
            total_data['driving_cnt'] += data['driving_cnt']
            total_data['distance'] += data['distance']
            total_data['driving_distance'] += data['driving_distance']
            total_data['minutes'] += minutes
            total_data['driving_minutes'] += driving_minutes
            total_data['fuel_cost'] += data['fuel_cost']
            total_data['driving_fuel_cost'] += data['driving_fuel_cost']
            total_data['tolerance_distance'] += data['tolerance_distance']

        total_data['distance'] = round(total_data['distance'], 1)
        total_data['tolerance_distance'] = round(total_data['tolerance_distance'], 1)
        total_data['time'] = get_hour_minute(total_data['minutes'])
        total_data['driving_time'] = get_hour_minute(total_data['driving_minutes'])
        total_data['tolerance_time'] = get_hour_minute(total_data['driving_minutes'] - total_data['minutes'])
        context['total_data'] = total_data

        # 인당평균
        data_list_size = len(data_list) if data_list else 1
        context['person_avg_data'] = self.calculate_avg_data(total_data, data_list_size)

        # 월별일때만 일별평균 계산
        if date_type == 'monthly':
            context['date_avg_data'] = self.calculate_avg_data(total_data, last_day)

        return context

    def calculate_avg_data(self, total_data, last_day):
        avg_data = self.get_avg_data(total_data, last_day)
        avg_data['time'] = get_hour_minute(avg_data['minutes'])
        avg_data['driving_time'] = get_hour_minute(avg_data['driving_minutes'])
        avg_data['tolerance_time'] = get_hour_minute(avg_data['driving_minutes'] - avg_data['minutes'])

        return avg_data

    # def calculate_person_avg_data(self, total_data, data_size):
    #     person_avg_data = self.get_avg_data(total_data, data_size)
    #     person_avg_data['time'] = get_hour_minute(person_avg_data['minutes'])
    #     person_avg_data['driving_time'] = get_hour_minute(person_avg_data['driving_minutes'])
    #     person_avg_data['tolerance_time'] = get_hour_minute(person_avg_data['driving_minutes'] - person_avg_data['minutes'])

    #     return person_avg_data

    def get_avg_data(self, total_data, divisor):
        avg_data = {}
        except_list = [
            'time',
            'driving_time',
            'tolerance_time',
        ]

        # total_data의 각 필드에 대해 반복하면서 평균값 계산
        for key, value in total_data.items():
            if key in except_list:
                continue
            # 평균값 계산
            avg_value = value / divisor
            # 평균값을 avg_data 딕셔너리에 추가
            avg_data[key] = round(avg_value)

        return avg_data