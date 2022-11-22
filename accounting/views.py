import json
import my_settings
from .models import Income, LastIncome, AdditionalCollect, Collect, TotalPrice
from .forms import IncomeForm, AdditionalCollectForm
from dispatch.views import FORMAT
from humanresource.models import Member
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from dispatch.models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyConnect, DispatchRegularly, RegularlyGroup
from django.db.models import Sum
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import BadRequest
from config import settings
from popbill import EasyFinBankService
import math
import time

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


# class SalaryList(generic.ListView):
#     template_name = 'accounting/salary.html'
#     context_object_name = 'salary_list'
#     model = Salary

#     def get_queryset(self):
#         selected_month = self.request.GET.get('month', str(datetime.now())[:7])
#         salary_list = Salary.objects.select_related('member_id').filter(month=selected_month).order_by('member_id__name')
#         return salary_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['selected_month'] = self.request.GET.get('month', str(datetime.now())[:7])

#         context['member_list'] = Member.objects.all().order_by('name')
#         entering_list = []
#         additional_list = []
#         for member in context['member_list']:
#             entering_list.append(member.entering_date)
#             additional_list.append(AdditionalSalary.objects.filter(member_id=member).filter(date__startswith=context['selected_month']))
#         context['entering_list'] = entering_list
#         context['additional_list'] = additional_list
#         return context
    
# class SalaryDetail(generic.ListView):
#     template_name = 'accounting/salary_detail.html'
#     context_object_name = 'salary'
#     model = Salary
    
#     def get_queryset(self):
#         member = get_object_or_404(Member, id=self.kwargs['pk'])
#         self.month = self.request.GET.get('month', TODAY[:7])
#         creator = get_object_or_404(Member, pk=self.request.session.get('user'))
#         try:
#             salary = Salary.objects.filter(member_id=member).get(month=self.month)
#         except:
#             salary = Salary(
#                 member_id = member,
#                 attendance=0,
#                 leave=0,
#                 order=0,
#                 additional=0,
#                 total=0,
#                 remark='',
#                 month=self.month,
#                 creator=creator,
#             )
#             salary.save()
        
#         return salary

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['selected_month'] = self.month
#         member = get_object_or_404(Member, id=self.kwargs['pk'])
#         # context['monthly'] = context['member'].salary_monthly.get(month=context['selected_month'])
#         first_day = datetime.strptime(self.month + "-01", FORMAT)
#         last_day = datetime.strftime(first_day + relativedelta(months=1) - timedelta(days=1), FORMAT)[8:]

#         a = []
#         additional_list = []
#         for i in range(int(last_day)):
#             a.append(i+1)
#             additional_list.append('')

#         additional = AdditionalSalary.objects.filter(member_id=get_object_or_404(Member, id=self.kwargs['pk'])).filter(date__startswith=self.month)
#         for i in additional:
#             additional_list[int(i.date[8:])-1] = i

#         context['a'] = a
#         context['additional_list'] = additional_list

        
#         order_list = [0] * int(last_day)
#         order_list_d = [''] * int(last_day)
#         order_list_a = [''] * int(last_day)
#         dispatches = DispatchOrderConnect.objects.prefetch_related('order_id').filter(driver_id=member).filter(departure_date__startswith=self.month).order_by('departure_date')
#         for dispatch in dispatches:
#             order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.driver_allowance)
#             order_list_d[int(dispatch.departure_date[8:10])-1] = dispatch.order_id.departure
#             order_list_a[int(dispatch.departure_date[8:10])-1] = dispatch.order_id.arrival

#         e_order_list = [0] * int(last_day)
#         e_order_list_d = [''] * int(last_day)
#         e_order_list_a = [''] * int(last_day)
#         e_dispatches = DispatchRegularlyConnect.objects.prefetch_related('regularly_id').filter(driver_id=member).filter(departure_date__startswith=self.month).filter(work_type="출근").order_by('departure_date')
#         for dispatch in e_dispatches:
#             e_order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.driver_allowance)
#             e_order_list_d[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.departure
#             e_order_list_a[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.arrival
        
#         c_order_list = [0] * int(last_day)
#         c_order_list_d = [''] * int(last_day)
#         c_order_list_a = [''] * int(last_day)
#         c_dispatches = DispatchRegularlyConnect.objects.prefetch_related('regularly_id').filter(driver_id=member).filter(departure_date__startswith=self.month).filter(work_type="퇴근").order_by('departure_date')
#         for dispatch in c_dispatches:
#             c_order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.driver_allowance)
#             c_order_list_d[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.departure
#             c_order_list_a[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.arrival

#         context['order_list'] = order_list
#         context['c_order_list'] = c_order_list
#         context['e_order_list'] = e_order_list

#         context['order_list_d'] = order_list_d
#         context['c_order_list_d'] = c_order_list_d
#         context['e_order_list_d'] = e_order_list_d

#         context['order_list_a'] = order_list_a
#         context['c_order_list_a'] = c_order_list_a
#         context['e_order_list_a'] = e_order_list_a

#         total_list = [0] * int(last_day)
#         for i in range(int(last_day)):
#             if additional_list[i]:
#                 total_list[i] = int(order_list[i]) + int(c_order_list[i]) + int(e_order_list[i]) + int(additional_list[i].price)
#             else:
#                 total_list[i] = int(order_list[i]) + int(c_order_list[i]) + int(e_order_list[i])

#         context['total_list'] = total_list

#         context['member_list'] = Member.objects.all().order_by('name')
#         entering_list = []
#         m_additional_list = []
#         for member in context['member_list']:
#             entering_list.append(member.entering_date)
#             m_additional_list.append(AdditionalSalary.objects.filter(member_id=member).filter(date__startswith=context['selected_month']))
#         context['entering_list'] = entering_list
#         context['m_additional_list'] = m_additional_list
#         context['member'] = get_object_or_404(Member, id=self.kwargs['pk'])
        
#         return context

# def salary_create(request):
#     if request.method == "POST":
#         additional_form = AdditionalForm(request.POST)
#         if additional_form.is_valid():
#             creator = get_object_or_404(Member, pk=request.session.get('user'))
#             member = get_object_or_404(Member, pk=request.POST.get('member_id'))
#             month = additional_form.cleaned_data['date'][:7]
#             date = additional_form.cleaned_data['date']
#             price = int(additional_form.cleaned_data['price'].replace(',',''))
#             try:
#                 salary = Salary.objects.filter(member_id=member).get(month=month)
                
#                 additional = AdditionalSalary.objects.filter(member_id=member).get(date=date)

#                 salary.additional = int(salary.additional) - int(additional.price) + price
#                 additional.delete()
#             except AdditionalSalary.DoesNotExist:
#                 salary.additional = int(salary.additional) + price
#             except Salary.DoesNotExist:
#                 print("Does Not Exist")
#                 salary = Salary(
#                     member_id = member,
#                     attendance=0,
#                     leave=0,
#                     order=0,
#                     additional=price,
#                     total=price,
#                     remark='',
#                     month=month,
#                     creator=creator,
#                 )

#             salary.save()
            
#             additional_salary = additional_form.save(commit=False)
#             additional_salary.price = price
#             additional_salary.salary_id = salary
#             additional_salary.creator = creator
#             additional_salary.member_id = member
#             additional_salary.save()

#             return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
#         else:
#             raise Http404
#     else:
#         return HttpResponseNotAllowed(['post'])

# def salary_edit(request):
#     if request.method == "POST":
#         additional_form = AdditionalForm(request.POST)
#         if additional_form.is_valid():
#             additional = get_object_or_404(AdditionalSalary, id=request.POST.get('id'))
#             additional.date = additional_form.cleaned_data['date']
#             additional.price = additional_form.cleaned_data['price']
#             additional.remark = additional_form.cleaned_data['remark']
#             additional.save()
#             return redirect('accounting:salary')
#         else:
#             raise Http404
#     else:
#         return HttpResponseNotAllowed(['post'])

# def salary_delete(request):
#     if request.method == "POST":
#         id_list = request.POST.getlist('check')
#         salary = ''
#         for id in id_list:
#             additional = get_object_or_404(AdditionalSalary, id=id)
#             if not salary:
#                 salary = additional.salary_id
#             additional.delete()
#         additional_list = salary.additional_salary.all()
#         total_additional = 0
#         for a in additional_list:
#             total_additional += int(a.price)
#         salary.additional = total_additional
#         salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)
#         salary.save()

#         return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
#     else:
#         return HttpResponseNotAllowed(['post'])

# def remark_edit(request):
#     if request.method == "POST":
#         id_list = request.POST.getlist('id')
#         remark_list = request.POST.getlist('remark')

#         for id, remark in zip(id_list, remark_list):
#             salary = Salary.objects.get(id=id)
#             salary.remark = remark
#             salary.save()
        
#         return redirect('accounting:salary')
#     else:
#         return HttpResponseNotAllowed(['post'])

class SalesList(generic.ListView):
    template_name = 'accounting/income.html'
    context_object_name = 'dispatch_list'
    model = DispatchOrder

    def get_queryset(self):
        month = self.request.GET.get('month', TODAY[:7])
        dispatch_list = DispatchOrder.objects.filter(departure_date__startswith=month)

        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        get_month = self.request.GET.get('month', TODAY[:7])

        yearly_sales = []
        for i in range(12):
            if i < 10:
                month = f'{get_month[:4]}-0{i}'
            else:
                month = f'{get_month[:4]}-{i}'

            regularly_sales = TotalPrice.objects.filter(month=month).exclude(group_id=None).aggregate(Sum('total_price'))['total_price__sum']
            order_sales = TotalPrice.objects.filter(month=month).exclude(order_id=None).aggregate(Sum('total_price'))['total_price__sum']
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
        
        type_cnt = {}
        bus_cnt = {}
        sales = {}
        payment = {}

        for order in context['dispatch_list']:
            try:
                type_cnt[order.order_type] += 1
                bus_cnt[order.order_type] += int(order.bus_cnt)
                sales[order.order_type] += int(order.bus_cnt) * int(order.price)
            except KeyError:
                type_cnt[order.order_type] = 1
                bus_cnt[order.order_type] = int(order.bus_cnt)
                sales[order.order_type] = int(order.bus_cnt) * int(order.price)

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

        context['month'] = month
        return context

class RegularlyCollectList(generic.ListView):
    template_name = 'accounting/regularly_collect.html'
    context_object_name = 'group_list'
    model = RegularlyGroup

    def get_queryset(self):
        group_list = RegularlyGroup.objects.prefetch_related('regularly_info').all().order_by('number', 'name')
        
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
                temp_value += int(additional.value)
                temp_VAT += int(additional.VAT)

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

            total = TotalPrice.objects.filter(group_id=group).get(month=month)
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
            print("TEST", used_price)
            print("total", income.total_income)
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
        regularly_list = DispatchRegularly.objects.prefetch_related('info_regularly').filter(group=group)
        
        temp_list = []
        try:
            for regularly in regularly_list:
                cnt = regularly.info_regularly.filter(departure_date__range=(f'{date1} 00:00', f'{date2} 24:00')).count(),
                cnt = cnt[0]
                supply_price = int(regularly.price) * int(cnt)
                print(supply_price)
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
        customer = self.request.GET.get('search', '')
        print('date1', date1)
        print('date1', date2)

        dispatch_list = DispatchOrder.objects.prefetch_related('order_collect').exclude(contract_status='취소').filter(departure_date__lte=f'{date2} 24:00').filter(arrival_date__gte=f'{date1} 00:00').order_by('departure_date')
        if customer:
            dispatch_list = dispatch_list.filter(customer__contains=customer)
        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date1'] = self.request.GET.get('date1', f'{TODAY[:7]}-01')
        context['date2'] = self.request.GET.get('date2', TODAY)
        context['customer'] = self.request.GET.get('search', '')

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
            total_list.append(int(get_object_or_404(TotalPrice, order_id=order).total_price))
            if order.VAT == 'y':
                value_list[cnt] = math.floor(int(order.price) / 1.1 + 0.5)
                VAT_list[cnt] = math.floor(value_list[cnt] * 0.1 + 0.5)
                total = value_list[cnt] + VAT_list[cnt]
                zero = int(order.price) - total
                if zero != 0:
                    VAT_list[cnt] += zero
            else:
                value_list[cnt] = int(order.price)
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
                value_list[cnt] += int(additional.value)
                VAT_list[cnt] += int(additional.VAT)
                additional_total_list[cnt] += int(additional.total_price)
            additional_list.append(temp_list)
            # print('aaaaaaaaaaaaaaadditional', additional_list)

            # total price save
            # total = TotalPrice(
            #     order_id = order,
            #     month = order.departure_date[:7],
            #     total_price = total_list[cnt],
            #     creator = get_object_or_404(Member, pk=self.request.session.get('user'))
            # )
            # total.save()
            # 

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
            print("TEST", used_price)
            print("total", income.total_income)
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
        
        income_list = Income.objects.filter(date__range=(f'{self.date1} 00:00', f'{self.date2} 24:00')).order_by('-date')
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
        CorpNum = my_settings.CORPNUM
        BankCode = my_settings.BANKCODE
        AccountNumber = my_settings.ACCOUNTNUMBER
        if last_income:
            print('last_incomeeee')
            SDate = last_income.tr_date[:8]
            last_save_date = last_income.tr_date
        else:
            SDate = datetime.strftime(datetime.strptime(TODAY, FORMAT) - relativedelta(months=1), '%Y%m%d')
            last_save_date = SDate
        print("SDATEE", SDate)        
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
            result = easyFinBankService.search(CorpNum, jobID, TradeType='I', SearchString='', Page=1, PerPage=100, Order='D', UserID=None)
            count = 0
            for r in result.list:
                # 은행명 괄호 제거
                if r.remark2[0] == '(' and r.remark2[-1] == ')':
                    bank = r.remark2[1:-1]
                else:
                    bank = r.remark2

                if r.trdt > last_save_date:
                    count += 1
                    income = Income(
                        serial=f'{r.trdate}-{r.trserial}',
                        date=f'{r.trdt[:4]}-{r.trdt[4:6]}-{r.trdt[6:8]} {r.trdt[8:10]}:{r.trdt[10:12]}',
                        depositor=r.remark1,
                        bank=bank,
                        acc_income=r.accIn,
                        total_income=r.accIn,
                        creator=creator,
                    )
                    income.save()
                else:
                    continue
                # print('trserial', r.trserial)
                # print('trdt', r.trdt)
                # print('accIn', r.accIn)
                # print('accOut', r.accOut)
                # print('balance', r.balance)
                # print('regDT', r.regDT)
                # print('remark1', r.remark1)
                # print('remark2', r.remark2)
                # print('remark3', r.remark3)
                # print('remark4', r.remark4,'\n')
            if result.list:
                last = LastIncome(
                    tr_date=result.list[0].trdt,
                    creator=creator 
                )
                last.save()
            return JsonResponse({'status': 'success', 'count': count})
        else:
            return JsonResponse(
                {
                    'status': state.errorReason,
                    'errorReason': state.errorReason,
                    'jobState': state.jobState,
                    'errorCode': state.errorCode,
                }
            )
    else:
        return HttpResponseNotAllowed(['post'])

def deposit_create(request):
    if request.method == "POST":
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            date = income_form.cleaned_data['date']
            income_cnt = Income.objects.filter(date__startswith=date).count()

            
            income = income_form.save(commit=False)
            income.serial = f'{date[:4]}{date[5:7]}{date[8:10]}-{int(income_cnt)+1}'
            income.commission = request.POST.get('commission', '0')
            income.total_income = int(income.acc_income) + int(income.commission)
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
        