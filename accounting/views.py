from .models import Salary, Income, AdditionalSalary, LastIncome
from .forms import AdditionalForm, IncomeForm
from dispatch.views import FORMAT
from humanresource.models import Member
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from dispatch.models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyConnect
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.core.exceptions import BadRequest
from config import settings
from popbill import EasyFinBankService, PopbillException, ContactInfo, JoinForm, CorpInfo
import time

TODAY = str(datetime.now())[:10]
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]

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


class SalaryList(generic.ListView):
    template_name = 'accounting/salary.html'
    context_object_name = 'salary_list'
    model = Salary

    def get_queryset(self):
        selected_month = self.request.GET.get('month', str(datetime.now())[:7])
        salary_list = Salary.objects.select_related('member_id').filter(month=selected_month).order_by('member_id__name')
        return salary_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_month'] = self.request.GET.get('month', str(datetime.now())[:7])

        context['member_list'] = Member.objects.all().order_by('name')
        entering_list = []
        additional_list = []
        for member in context['member_list']:
            entering_list.append(member.entering_date)
            additional_list.append(AdditionalSalary.objects.filter(member_id=member).filter(date__startswith=context['selected_month']))
        context['entering_list'] = entering_list
        context['additional_list'] = additional_list
        return context
    
class SalaryDetail(generic.ListView):
    template_name = 'accounting/salary_detail.html'
    context_object_name = 'salary'
    model = Salary
    
    def get_queryset(self):
        member = get_object_or_404(Member, id=self.kwargs['pk'])
        self.month = self.request.GET.get('month', TODAY[:7])
        creator = get_object_or_404(Member, pk=self.request.session.get('user'))
        try:
            salary = Salary.objects.filter(member_id=member).get(month=self.month)
        except:
            salary = Salary(
                member_id = member,
                attendance=0,
                leave=0,
                order=0,
                additional=0,
                total=0,
                remark='',
                month=self.month,
                creator=creator,
            )
            salary.save()
        
        return salary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_month'] = self.month
        member = get_object_or_404(Member, id=self.kwargs['pk'])
        # context['monthly'] = context['member'].salary_monthly.get(month=context['selected_month'])
        first_day = datetime.strptime(self.month + "-01", FORMAT)
        last_day = datetime.strftime(first_day + relativedelta(months=1) - timedelta(days=1), FORMAT)[8:]

        a = []
        additional_list = []
        for i in range(int(last_day)):
            a.append(i+1)
            additional_list.append('')

        additional = AdditionalSalary.objects.filter(member_id=get_object_or_404(Member, id=self.kwargs['pk'])).filter(date__startswith=self.month)
        for i in additional:
            additional_list[int(i.date[8:])-1] = i

        context['a'] = a
        context['additional_list'] = additional_list

        
        order_list = [0] * int(last_day)
        order_list_d = [''] * int(last_day)
        order_list_a = [''] * int(last_day)
        dispatches = DispatchOrderConnect.objects.prefetch_related('order_id').filter(driver_id=member).filter(departure_date__startswith=self.month).order_by('departure_date')
        for dispatch in dispatches:
            order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.driver_allowance)
            order_list_d[int(dispatch.departure_date[8:10])-1] = dispatch.order_id.departure
            order_list_a[int(dispatch.departure_date[8:10])-1] = dispatch.order_id.arrival

        e_order_list = [0] * int(last_day)
        e_order_list_d = [''] * int(last_day)
        e_order_list_a = [''] * int(last_day)
        e_dispatches = DispatchRegularlyConnect.objects.prefetch_related('regularly_id').filter(driver_id=member).filter(departure_date__startswith=self.month).filter(work_type="출근").order_by('departure_date')
        for dispatch in e_dispatches:
            e_order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.driver_allowance)
            e_order_list_d[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.departure
            e_order_list_a[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.arrival
        
        c_order_list = [0] * int(last_day)
        c_order_list_d = [''] * int(last_day)
        c_order_list_a = [''] * int(last_day)
        c_dispatches = DispatchRegularlyConnect.objects.prefetch_related('regularly_id').filter(driver_id=member).filter(departure_date__startswith=self.month).filter(work_type="퇴근").order_by('departure_date')
        for dispatch in c_dispatches:
            c_order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.driver_allowance)
            c_order_list_d[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.departure
            c_order_list_a[int(dispatch.departure_date[8:10])-1] = dispatch.regularly_id.arrival

        context['order_list'] = order_list
        context['c_order_list'] = c_order_list
        context['e_order_list'] = e_order_list

        context['order_list_d'] = order_list_d
        context['c_order_list_d'] = c_order_list_d
        context['e_order_list_d'] = e_order_list_d

        context['order_list_a'] = order_list_a
        context['c_order_list_a'] = c_order_list_a
        context['e_order_list_a'] = e_order_list_a

        total_list = [0] * int(last_day)
        for i in range(int(last_day)):
            if additional_list[i]:
                total_list[i] = int(order_list[i]) + int(c_order_list[i]) + int(e_order_list[i]) + int(additional_list[i].price)
            else:
                total_list[i] = int(order_list[i]) + int(c_order_list[i]) + int(e_order_list[i])

        context['total_list'] = total_list

        context['member_list'] = Member.objects.all().order_by('name')
        entering_list = []
        m_additional_list = []
        for member in context['member_list']:
            entering_list.append(member.entering_date)
            m_additional_list.append(AdditionalSalary.objects.filter(member_id=member).filter(date__startswith=context['selected_month']))
        context['entering_list'] = entering_list
        context['m_additional_list'] = m_additional_list
        context['member'] = get_object_or_404(Member, id=self.kwargs['pk'])
        
        return context

def salary_create(request):
    if request.method == "POST":
        additional_form = AdditionalForm(request.POST)
        if additional_form.is_valid():
            creator = get_object_or_404(Member, pk=request.session.get('user'))
            member = get_object_or_404(Member, pk=request.POST.get('member_id'))
            month = additional_form.cleaned_data['date'][:7]
            date = additional_form.cleaned_data['date']
            price = int(additional_form.cleaned_data['price'].replace(',',''))
            try:
                salary = Salary.objects.filter(member_id=member).get(month=month)
                
                additional = AdditionalSalary.objects.filter(member_id=member).get(date=date)

                salary.additional = int(salary.additional) - int(additional.price) + price
                additional.delete()
            except AdditionalSalary.DoesNotExist:
                salary.additional = int(salary.additional) + price
            except Salary.DoesNotExist:
                print("Does Not Exist")
                salary = Salary(
                    member_id = member,
                    attendance=0,
                    leave=0,
                    order=0,
                    additional=price,
                    total=price,
                    remark='',
                    month=month,
                    creator=creator,
                )

            salary.save()
            
            additional_salary = additional_form.save(commit=False)
            additional_salary.price = price
            additional_salary.salary_id = salary
            additional_salary.creator = creator
            additional_salary.member_id = member
            additional_salary.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def salary_edit(request):
    if request.method == "POST":
        additional_form = AdditionalForm(request.POST)
        if additional_form.is_valid():
            additional = get_object_or_404(AdditionalSalary, id=request.POST.get('id'))
            additional.date = additional_form.cleaned_data['date']
            additional.price = additional_form.cleaned_data['price']
            additional.remark = additional_form.cleaned_data['remark']
            additional.save()
            return redirect('accounting:salary')
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def salary_delete(request):
    if request.method == "POST":
        id_list = request.POST.getlist('check')
        salary = ''
        for id in id_list:
            additional = get_object_or_404(AdditionalSalary, id=id)
            if not salary:
                salary = additional.salary_id
            additional.delete()
        additional_list = salary.additional_salary.all()
        total_additional = 0
        for a in additional_list:
            total_additional += int(a.price)
        salary.additional = total_additional
        salary.total = int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.additional)
        salary.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def remark_edit(request):
    if request.method == "POST":
        id_list = request.POST.getlist('id')
        remark_list = request.POST.getlist('remark')

        for id, remark in zip(id_list, remark_list):
            salary = Salary.objects.get(id=id)
            salary.remark = remark
            salary.save()
        
        return redirect('accounting:salary')
    else:
        return HttpResponseNotAllowed(['post'])

class IncomeList(generic.ListView):
    template_name = 'accounting/income.html'
    context_object_name = 'dispatch_list'
    model = DispatchOrder

    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month = self.request.GET.get('month', TODAY[:7])
        first_day = datetime.strptime(month + "-01", FORMAT)
        last_day = datetime.strftime(first_day + relativedelta(months=1) - timedelta(days=1), FORMAT)[8:]

        order_list = [0] * int(last_day)
        order_list_total = 0
        collect_list = [0] * int(last_day)
        dispatches = DispatchOrderConnect.objects.select_related('order_id').filter(departure_date__startswith=month).order_by('departure_date')
        for dispatch in dispatches:
            order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.order_id.price)
            order_list_total += int(dispatch.order_id.price)
            collect_list[int(dispatch.departure_date[8:10])-1] = int(dispatch.order_id.collection_amount)
            

        e_order_list = [0] * int(last_day)
        e_order_list_total = 0
        e_dispatches = DispatchRegularlyConnect.objects.select_related('regularly_id').filter(departure_date__startswith=month).filter(work_type="출근").order_by('departure_date')
        for dispatch in e_dispatches:
            e_order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.regularly_id.price)
            e_order_list_total += int(dispatch.regularly_id.price)
        
        c_order_list = [0] * int(last_day)
        c_order_list_total = 0
        c_dispatches = DispatchRegularlyConnect.objects.select_related('regularly_id').filter(departure_date__startswith=month).filter(work_type="퇴근").order_by('departure_date')
        for dispatch in c_dispatches:
            c_order_list[int(dispatch.departure_date[8:10])-1] += int(dispatch.regularly_id.price)
            c_order_list_total += int(dispatch.regularly_id.price)

        n_collect_list = [0] * int(last_day)
        n_collect_list_total = 0
        collect_list_total = 0
        total_list = [0] * int(last_day)
        for i in range(int(last_day)):
            collect_list_total += collect_list[i]
            if order_list[i] and collect_list[i]:
                n_collect_list[i] = order_list[i] - collect_list[i]
                n_collect_list_total += n_collect_list[i]
            if order_list[i] and e_order_list[i] and c_order_list[i]:
                total_list[i] = order_list[i] + e_order_list[i] + c_order_list[i]
            

        context['order_list'] = order_list
        context['c_order_list'] = c_order_list
        context['e_order_list'] = e_order_list

        context['order_list_total'] = order_list_total
        context['c_order_list_total'] = c_order_list_total
        context['e_order_list_total'] = e_order_list_total
        context['collect_list_total'] = collect_list_total
        context['n_collect_list_total'] = n_collect_list_total

        context['collect_list'] = collect_list
        context['n_collect_list'] = n_collect_list
        context['total_list'] = total_list

        context['last_day'] = last_day
        context['month'] = month

        return context

class RegularlyCollectList(generic.ListView):
    template_name = 'accounting/regularly_collect.html'
    context_object_name = 'dispatch_list'
    model = DispatchOrder

class CollectList(generic.ListView):
    template_name = 'accounting/collect.html'
    context_object_name = 'dispatch_list'
    model = DispatchOrder

    def get_queryset(self):
        month = self.request.GET.get('month', TODAY[:7])

        dispatch_list = DispatchOrder.objects.filter(departure_date__startswith=month)

        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departure_date = []
        time = []
        num_days = []

        for order in context['dispatch_list']:
            d_y = order.departure_date[0:4]
            d_m = order.departure_date[5:7]
            d_d = order.departure_date[8:10]
            d_t = order.departure_date[11:16]
            d_date = date(int(d_y), int(d_m), int(d_d))
            d_w = WEEK[d_date.weekday()]
            d_y = d_y[2:4]

            a_y = order.arrival_date[0:4]
            a_m = order.arrival_date[5:7]
            a_d = order.arrival_date[8:10]
            a_t = order.arrival_date[11:16]
            a_date = date(int(a_y), int(a_m), int(a_d))
            a_y = a_y[2:4]
            
            date_diff = a_date - d_date
            if date_diff.days > 1:
                num_days.append(date_diff.days)
            else:
                num_days.append('')

            departure_date.append(f"{d_y}.{d_m}.{d_d} {d_w}")
            time.append(f"{d_t}~{a_t}")
            # arrival_date.append(f"{a_y}.{a_m}.{a_d} {a_w} {a_t}")

        context['departure_date'] = departure_date
        context['num_days'] = num_days
        context['time'] = time
        context['month'] = self.request.GET.get('month', TODAY[:7])

        return context

def collect_create(request):
    if request.method == "POST":
        id = request.POST.get('id')
        collection = get_object_or_404(DispatchOrder, id=id)
        collection.collection_amount = int(request.POST.get('collection_amount').replace(',',''))
        collection.collection_date = request.POST.get('collection_date', '')
        collection.collection_creator = request.POST.get('collection_creator', '')
        collection.save()
        
        return redirect('accounting:collect')
    else:
        return HttpResponseNotAllowed(['post'])

class DepositList(generic.ListView):
    template_name = 'accounting/deposit.html'
    context_object_name = 'income_list'
    model = Income

    def get_queryset(self):
        self.date1 = self.request.GET.get('date1', TODAY)
        self.date2 = self.request.GET.get('date2', TODAY)
        self.select = self.request.GET.get('select')
        self.search = self.request.GET.get('search', '')
        self.payment = self.request.GET.get('payment')
        
        income_list = Income.objects.filter(date__range=(self.date1, self.date2)).order_by('-date')
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
        context['payment'] = self.date2

        temp_list = []
        for income in context['income_list']:
            temp_list.append({
                'date': income.date,
                'payment_method': income.payment_method,
                'bank': income.bank,
                'commission': income.commission,
                'acc_income': income.acc_income,
                'depositor': income.depositor,
            })
        context['data_list'] = temp_list
        return context

def load_deposit_data(request):
    if request.method == 'POST':
        last_income = LastIncome.objects.last()
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        CorpNum = '2874900474'
        BankCode = '0003'
        AccountNumber = '15717723401016'
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
                if r.trdt > last_save_date:
                    count += 1
                    income = Income(
                        serial=f'{r.trdate}-{r.trserial}',
                        date=f'{r.trdt[:4]}-{r.trdt[4:6]}-{r.trdt[6:8]} {r.trdt[8:10]}:{r.trdt[10:12]}',
                        depositor=r.remark1,
                        bank=r.remark2,
                        acc_income=r.accIn,
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
            date = income_form.cleaned_data['data']
            income_cnt = Income.objects.filter(date__startswith=date).count()

            income.date = income_form.cleaned_data['date']
            income.depositor = income_form.cleaned_data['depositor']
            income.payment_method = income_form.cleaned_data['payment_method']
            income.bank = income_form.cleaned_data['bank']
            income.acc_income = income_form.cleaned_data['acc_income']
            income.serial = f'{date[:4]}{date[5:7]}{date[8:10]}-{int(income_cnt)+1}'
            income.commission = request.POST.get('commission', '0')
            income.creator = get_object_or_404(Member, pk=request.session.get('user'))
            income.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest('Invalid request')
    else:
        return HttpResponseNotAllowed(['post'])
        