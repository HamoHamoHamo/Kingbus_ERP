from crudmember.models import User
from humanresource.models import Member
from dispatch.models import DispatchOrder, DispatchConnect
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import MonthlySalaryForm, DailySalaryForm, OutlayForm, CollectForm, IncomeForm
from .models import MonthlySalary, DailySalary, Outlay, Collect, Income
import datetime

#지출
class OutlayList(generic.ListView):
    template_name = 'accounting/outlay_list.html'
    context_object_name = 'outlay_list'
    model = Outlay

    def get_queryset(self):
        selected_year = self.request.GET.get('year', None)
        selected_month = self.request.GET.get('month', None)
        if selected_year is None and selected_month is None:
            month = str(datetime.datetime.now())[:7]
        else:
            month = selected_year +"-" + selected_month
        #outlay_list = Outlay.objects.filter(outlay_date=)
        outlay_list = Outlay.objects.filter(outlay_date__startswith=month)
        return outlay_list
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salary = 0
        welfare = 0
        company = 0
        car = 0
        total = 0
        other = 0

        context['daily_list'] = []

        for i in range(1,32):
            daily_price = {}
            if i < 10:
                date = "0" + str(i)
            else:
                date = str(i)
            daily_outlay = context['outlay_list'].filter(outlay_date__endswith=date)
            daily_total = 0
            daily_car = 0
            daily_welfare = 0
            daily_company = 0
            daily_other = 0

            for outlay in daily_outlay:
                total += outlay.price

                daily_price['date'] = date
                daily_total += outlay.price

                #print("테스트 비용", outlay.price)
                if outlay.kinds == '복리후생':
                    welfare += outlay.price
                    daily_welfare += outlay.price
                elif outlay.kinds == '차량':
                    car += outlay.price
                    daily_car += outlay.price
                elif outlay.kinds == '운영':
                    company += outlay.price
                    daily_company += outlay.price
                else:
                    other += outlay.price
                    daily_other += outlay.price

            daily_price['car'] = daily_car
            daily_price['other'] = daily_other
            daily_price['welfare'] = daily_welfare
            daily_price['company'] = daily_company
            daily_price['total'] = daily_total
            context['daily_list'].append(daily_price)
            
        
        for monthly in MonthlySalary.objects.filter(payment_month=str(datetime.datetime.now())[:7]):
            salary += monthly.total

        #print("테스트", salary, car, welfare, company)
        context['salary'] = salary
        context['car'] = car
        context['welfare'] = welfare
        context['company'] = company
        context['total'] = total
        context['other'] = other

        year = []  # 년도 selector 옵션값 배열
        now_year = int(str(datetime.datetime.now())[:4])  
        for i in range(20):
            if i <11:
                year.append(now_year - i)
            else:
                year.append(now_year + i-10)
        context['option_year'] = sorted(year)
        context['year'] = str(datetime.datetime.now())[:4]
        context['month'] = str(datetime.datetime.now())[5:7]
        context['int_selected_year'] = int(self.request.GET.get('year', context['year']))
        context['int_selected_month'] = int(self.request.GET.get('month', context['month']))
        context['str_selected_year'] = str(self.request.GET.get('year', context['year']))
        context['str_selected_month'] = str(self.request.GET.get('month', context['month']))

        return context

def outlay_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        
        outlay_form = OutlayForm(request.POST)
        if outlay_form.is_valid():
            outlay = outlay_form.save(commit=False)
            outlay.creator = creator
            outlay.save()
            return redirect('accounting:outlay_list')
    else:
        context = {
            'outlay_form' : OutlayForm(),
        }
    return render(request, 'accounting/outlay_create.html', context)

class OutlayDetailList(generic.ListView):
    template_name = 'accounting/outlay_detail.html'
    context_object_name = 'outlay'
    model = Outlay

    def get_queryset(self):
        outlay = Outlay.objects.filter(outlay_date=self.kwargs['date'])
        return outlay

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.kwargs['date']


        context['total'] = 0
        context['car'] = 0
        context['welfare'] = 0
        context['company'] = 0
        context['other'] = 0

        for outlay in context['outlay']:
            context['total'] += outlay.price
            #print("테스트 비용", outlay.price)
            if outlay.kinds == '복리후생':
                context['welfare'] += outlay.price
            elif outlay.kinds == '차량':
                context['car'] += outlay.price
            elif outlay.kinds == '운영':
                context['company'] += outlay.price
            else:
                context['other'] += outlay.price

        return context



def outlay_delete(request, pk):
    outlay = get_object_or_404(Outlay, pk=pk)
    if User.objects.get(pk=request.session['user']).authority == "관리자":
        outlay.delete()
    return redirect('accounting:outlay_list')

def outlay_edit(request, pk):
    outlay = get_object_or_404(Outlay, pk=pk)
    context = {}
    if request.method == "POST":
        if User.objects.get(pk=request.session['user']).authority == "관리자":
            creator = get_object_or_404(User, pk=request.session.get('user'))
            outlay_form = OutlayForm(request.POST)
            if outlay_form.is_valid():
                edit_outlay = outlay_form.save(commit=False)
                edit_outlay.creator = creator
                outlay.delete()
                edit_outlay.id = pk
                edit_outlay.save()
                return redirect('accounting:outlay_list')
    else:
        context = {
            'outlay' : outlay,
        }
    return render(request, 'accounting/outlay_edit.html', context)

#급여
class SalaryList(generic.ListView):
    template_name = 'accounting/salary_list.html'
    context_object_name = 'salary_list'
    model = MonthlySalary

    def get_queryset(self):
        self.selected_year = self.request.GET.get('year', str(datetime.datetime.now())[:4])
        self.selected_month = self.request.GET.get('month', str(datetime.datetime.now())[5:7])
        
        month = self.selected_year +"-" + self.selected_month
        
        salary_list = MonthlySalary.objects.filter(payment_month__startswith=month)
        return salary_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_year'] = self.selected_year
        context['selected_month'] = self.selected_month
        context['int_selected_year'] = int(self.selected_year)
        context['int_selected_month'] = int(self.selected_month)
        
        return context

def salary_create(request):
    get_date = request.GET.get('date')
    if not get_date:
        get_date=str(datetime.datetime.now())[:10]
    if request.method == "POST":
        remove = DailySalary.objects.filter(date=get_date)
        print("remove", len(remove))
        base_list = request.POST.getlist('base')
        deductible_list = request.POST.getlist('deductible')
        bonus_list = request.POST.getlist('bonus')
        additional_list = request.POST.getlist('additional')
        #connect_list = request.POST.getlist('connect_id')

        cnt = 0
        month = get_date[:7]
        login_user = get_object_or_404(User, pk=request.session.get('user'))

        # 만약 POST에서 에러가 나면 값은 저장안되고 이전값만 다 지워질 수 있음
        for r in remove:
            print("테스트", r)
            r.delete()
            
        for member in Member.objects.order_by('pk'):
            try:
                monthly = member.salary_monthly.get(payment_month__startswith=month)
                print("aaaaaaaaaaaaaaaaaaaaaaaaa", monthly)

            except Exception as e:
                # 만약 이번달 급여가 db에 없으면 이번달 급여를 모든 항목 0으로 넣어서 만듬
                monthly = MonthlySalary(
                    member_id = member,
                    base=0,
                    bonus=0,
                    additional=0,
                    deductible=0,
                    total=0,
                    payment_month=month,
                    creator=login_user,
                )
                monthly.save()

            if base_list[cnt]:
                monthly.base = int(base_list[cnt])
            if deductible_list[cnt]:                
                monthly.deductible = int(deductible_list[cnt])

            monthly.save()

            try:
                daily_bonus = int(bonus_list[cnt])
                daily_additional = int(additional_list[cnt])
            except:
                daily_bonus=0
                daily_additional=0

            daily = DailySalary(
                bonus=daily_bonus,
                additional=daily_additional,
                creator=login_user,
                date=get_date,
                monthly_salary=monthly,
                total=daily_bonus + daily_additional
            )
            #if connect_list[cnt]:
            #    daily.connect_id=DispatchConnect.objects.get(pk=connect_list[cnt])
            cnt += 1
            daily.save()

            
            monthly.bonus = 0
            monthly.additional = 0
            monthly.total = 0
            monthly.save()
            for daily in monthly.salary_daily.all():
                monthly.bonus = int(monthly.bonus) + int(daily.bonus)
                monthly.additional = int(monthly.additional) + int(daily.additional)
            monthly.total = monthly.bonus + monthly.additional + monthly.base - monthly.deductible
            monthly.save()
        
        
        
            '''
            for daily in remove:
                print("ㅁㅇㅇㅁ", daily, len(remove))
                if daily in monthly.salary_daily.all():
                    print("테스트", daily, member.name)
                    monthly.bonus = int(monthly.bonus) - int(daily.bonus)
                    monthly.additional = int(monthly.additional) - int(daily.additional)
                    monthly.save()                    
                    daily.delete()
            print("for끝")
            '''
        return redirect('accounting:salary_list')

    elif request.method == 'GET':
        member_list = []
        for member in Member.objects.order_by('pk'):
            try:
                monthly = MonthlySalary.objects.filter(payment_month=get_date[:7]).get(member_id=member)
                #print("ttttttttttttttttttttttttttttt", monthly.base)
                daily = DailySalary.objects.filter(date=get_date).get(monthly_salary=monthly)
            except Exception as e:
                daily = member
            #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa", daily)
            member_list.append(daily)

        context = {
            'date' : get_date,
            'member_list' : member_list
            #'daily_order' : DispatchOrder.objects.filter(first_departure_date=str(datetime.datetime.now())[:10])
        }
    return render(request, 'accounting/salary_create.html', context)

class SalaryDetail(generic.DetailView):
    template_name = 'accounting/salary_detail.html'
    context_object_name = 'member'
    model = Member
    
    def get_context_data(self, **kwargs):
        month = str(datetime.datetime.now())[:7]
        context = super().get_context_data(**kwargs)
        context['daily_salary'] = Member.objects.get(pk=self.kwargs['pk']).salary_monthly.get(payment_month=month).salary_daily.all()
        
        return context

'''
def salary_delete(request, pk):
    # delete를 따로 안만들고 create에서 0으로 수정하게
    return render(request, 'accounting/salary_detail.html')

def salary_edit(request, pk):
    # edit도 따로 안만들고 create에서 edit기능 통합 사용
    return render(request, 'accounting/salary_edit.html')
'''

#수입
class IncomeList(generic.ListView):
    template_name = 'accounting/income_list.html'
    context_object_name = 'income_list'
    model = Income

    def get_queryset(self):
        income_list = []
        month = str(datetime.datetime.now())[:7]
        #income_list = income.objects.filter(income_date=)
        for income in Income.objects.order_by('-income_date'):
            if income.income_date[:7] == month:
                income_list.append(income)
        return income_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collect = 0
        other = 0

        for income in context['income_list']:
            #print("테스트 비용", outlay.price)
            if income.kinds == '수금':
                collect += income.price
            elif income.kinds == '기타':
                other += income.price
        total = other + collect

        #print("테스트", salary, car, welfare, company)
        context['collect'] = collect
        context['other'] = other
        context['total'] = total
        return context

def income_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.creator = creator
            income.save()
            return redirect('accounting:income_list')
    else:
        context = {
            'income_form' : IncomeForm(),
        }
    return render(request, 'accounting/income_create.html', context)

class IncomeDetail(generic.DetailView):
    template_name = 'accounting/income_detail.html'
    context_object_name = 'income'
    model = Income

def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if User.objects.get(pk=request.session['user']).authority == "관리자":
        income.delete()    
    return render(request, 'accounting/income_list.html')

def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk)
    context = {}
    if request.method == "POST":
        if User.objects.get(pk=request.session['user']).authority == "관리자":
            creator = get_object_or_404(User, pk=request.session.get('user'))
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                edit_income = income_form.save(commit=False)
                edit_income.creator = creator
                income.delete()
                edit_income.id = pk
                edit_income.save()
                return redirect('accounting:income_list')
    else:
        context = {
            'income_form' : IncomeForm(instance=income),
        }
    return render(request, 'accounting/income_edit.html', context)

#수금
class CollectList(generic.ListView):
    template_name = 'accounting/collect_list.html'
    context_object_name = 'collect_list'
    model = Collect

    def get_queryset(self):
        collect_list = []
        month = str(datetime.datetime.now())[:7]
        for order in DispatchOrder.objects.order_by('-first_departure_date'):
            if order.first_departure_date[:7] == month:
                for connect in order.info_order.all():
                    collect_list.append(connect.collect_connect.get(connect_id=connect))
        return collect_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['check'] = [i for i in context['collect_list'] if i.check==True]
        #print("테스트", context['check'])
        context['nocheck'] = [i for i in context['collect_list'] if i.check==False]
        #print("테스트 nocheck", context['check'])
        return context

class CollectDetail(generic.DetailView):
    template_name = 'accounting/collect_detail.html'
    context_object_name = 'collect'
    model = Collect

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = context['collect'].connect_id.order_id
        context['connect'] = context['collect'].connect_id
        return context
        
def collect_edit(request, pk):
    collect = get_object_or_404(Collect, pk=pk)
    context = {}
    if request.method == 'POST':
        if User.objects.get(pk=request.session['user']).authority == "관리자":
            collect_form = CollectForm(request.POST)
            if collect_form.is_valid():
                edit_collect = collect_form.save(commit=False)
                edit_collect.connect_id = collect.connect_id
                edit_collect.creator = collect.creator
                edit_collect.pub_date = collect.pub_date
                collect.delete()
                edit_collect.id = pk
                edit_collect.save()
                return redirect(reverse('accounting:collect_detail', args=(pk,)))
            else:
                return redirect(reverse('accounting:collect_edit', args=(pk,)))
    elif request.method == "GET":
        context = {
            'collect_form' : CollectForm(instance=collect)
        }
        return render(request, 'accounting/collect_edit.html', context)



   