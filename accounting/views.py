from accounting.forms import AdditionalForm
from crudmember.models import User
from humanresource.models import Member
from dispatch.models import DispatchOrder
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Salary, Income, AdditionalSalary
from datetime import datetime, date

TODAY = str(datetime.now())[:10]
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]




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
        creator = get_object_or_404(User, pk=self.request.session.get('user'))
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
        
        # context['monthly'] = context['member'].salary_monthly.get(month=context['selected_month'])

        a = []
        additional_list = []
        for i in range(31):
            a.append(i+1)
            additional_list.append('')

        additional = AdditionalSalary.objects.filter(member_id=get_object_or_404(Member, id=self.kwargs['pk'])).filter(date__startswith=self.month)
        for i in additional:
            additional_list[int(i.date[8:])-1] = i


        context['a'] = a
        context['additional_list'] = additional_list
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
            creator = get_object_or_404(User, pk=request.session.get('user'))
            member = get_object_or_404(Member, pk=request.POST.get('member_id'))
            month = additional_form.cleaned_data['date'][:7]
            try:
                salary = Salary.objects.filter(member_id=member).get(month=month)
                
                try:
                    additional = AdditionalSalary.objects.filter(member_id=member).get(date=additional_form.cleaned_data['date'])
                    
                    salary.additional = salary.additional - additional.price + int(additional_form.cleaned_data['price'])
                    additional.delete()
                except Exception as e:
                    salary.additional = salary.additional + int(additional_form.cleaned_data['price'])
                
            except Exception as e:
                print(e)
                salary = Salary(
                    member_id = member,
                    attendance=0,
                    leave=0,
                    order=0,
                    additional=additional_form.cleaned_data['price'],
                    total=0,
                    remark='',
                    month=month,
                    creator=creator,
                )
            salary.save()
            
            additional_salary = additional_form.save(commit=False)
            additional_salary.salary_id = salary
            additional_salary.creator = creator
            additional_salary.member_id = member
            additional_salary.save()

            return redirect('accounting:salary')
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

def income(request):
    
    return render(request, 'accounting/income.html')

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

        collection.collection_amount = request.POST.get('collection_amount', '')
        collection.collection_date = request.POST.get('collection_date', '')
        collection.collection_creator = request.POST.get('collection_creator', '')
        collection.save()
        
        return redirect('accounting:collect')
    else:
        return HttpResponseNotAllowed(['post'])
