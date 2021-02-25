from crudmember.models import User
from humanresource.models import Member
from dispatch.models import DispatchOrder
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
        outlay_list = []
        month = str(datetime.datetime.now())[:7]
        #outlay_list = Outlay.objects.filter(outlay_date=)
        for outlay in Outlay.objects.order_by('-outlay_date'):
            if str(outlay.outlay_date)[:7] == month:
                outlay_list.append(outlay)

        return outlay_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salary = 0
        welfare = 0
        company = 0
        car = 0
        total = 0
        other = 0
        
        for outlay in context['outlay_list']:
            #print("테스트 비용", outlay.price)
            total += outlay.price
            if outlay.kinds == '복리후생':
                welfare += outlay.price
            elif outlay.kinds == '급여':
                salary += outlay.price
            elif outlay.kinds == '차량비용':
                car += outlay.price
            elif outlay.kinds == '운영비용':
                company += outlay.price
            else:
                other += outlay.price

        #print("테스트", salary, car, welfare, company)
        context['salary'] = salary
        context['car'] = car
        context['welfare'] = welfare
        context['company'] = company
        context['total'] = total
        context['other'] = other

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

class OutlayDetail(generic.DetailView):
    template_name = 'accounting/outlay_detail.html'
    context_object_name = 'outlay'
    model = Outlay

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
            'outlay_form' : OutlayForm(instance=outlay),
        }
    return render(request, 'accounting/outlay_edit.html', context)

#급여
class SalaryList(generic.ListView):
    template_name = 'accounting/salary_list.html'
    context_object_name = 'salary_list'
    model = MonthlySalary

    def get_queryset(self):
        salary_list = []
        member_list = Member.objects.order_by('pk')
        month = str(datetime.datetime.now())[:7]
        #salary_list = salary.objects.filter(payment_month=)
        for member in member_list:
            for salary in member.salary_monthly.all():
                if str(salary.payment_month)[:7] == month:
                    salary_list.append(salary)
        return salary_list

def salary_create(request):
    if request.method == "POST":
        bonus_list = request.POST.getlist('bonus')
        additional_list = request.POST.getlist('additional')
        order_list = request.POST.getlist('order_id')

        cnt = 0
        month = str(datetime.datetime.now())[:7]
        login_user = get_object_or_404(User, pk=request.session.get('user'))

        for member in Member.objects.order_by('pk'):
            #lamda? 를 쓰면 더 간략하게 쓸 수 있을듯
            monthly = None
            # 만약 이번달 급여가 db에 없으면 이번달 급여를 모든 항목 0으로 넣어서 만듬
            for salary in member.salary_monthly.all():
                if str(salary.payment_month)[:7] == month:
                    monthly = salary
            if not monthly:
                monthly = MonthlySalary(
                    member_id = member,
                    base=0,
                    bonus=0,
                    additional=0,
                    deductible=0,
                    total=0,
                    payment_month=datetime.datetime.now(),
                    creator=login_user,
                )
                monthly.save()

            daily = DailySalary(
                bonus=bonus_list[cnt],
                additional=additional_list[cnt],
                creator=login_user,
                date=request.POST.get('date'),
                order_id=DispatchOrder.objects.get(brief=order_list[cnt]),
                monthly_salary=monthly,
            )
            cnt += 1
            daily.save()
            monthly.bonus = int(monthly.bonus) + int(daily.bonus)
            monthly.additional = int(monthly.additional) + int(daily.additional)
            monthly.save()
        return redirect('accounting:salary_list')

    else:
        context = {
            'daily_salary' : DailySalaryForm(),
            'member_list' : Member.objects.order_by('pk'),
            'today' : str(datetime.datetime.now())[:10],
            'daily_order' : DispatchOrder.objects.filter(first_departure_date=str(datetime.datetime.now())[:10])
        }
    return render(request, 'accounting/salary_create.html', context)

class SalaryDetail(generic.DetailView):
    template_name = 'accounting/salary_detail.html'
    context_object_name = 'salary'
    model = MonthlySalary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['']


def salary_delete(request, pk):

    return render(request, 'accounting/salary_detail.html')

def salary_edit(request, pk):

    return render(request, 'accounting/salary_edit.html')

#수입
class IncomeList(generic.ListView):
    template_name = 'accounting/income_list.html'
    context_object_name = 'income_list'
    model = Income

def income_create(request):

    return render(request, 'accounting/income_create.html')

class IncomeDetail(generic.DetailView):
    template_name = 'accounting/income_detail.html'
    context_object_name = 'income'
    model = Income

def income_delete(request, pk):

    return render(request, 'accounting/income_detail.html')

def income_edit(request, pk):

    return render(request, 'accounting/income_edit.html')

#수금
class CollectList(generic.ListView):
    template_name = 'accounting/collect_list.html'
    context_object_name = 'collect_list'
    model = Collect

class CollectDetail(generic.DetailView):
    template_name = 'accounting/collect_detail.html'
    context_object_name = 'collect'
    model = Collect

def collect_edit(request, pk):

    return render(request, 'accounting/collect_edit.html')