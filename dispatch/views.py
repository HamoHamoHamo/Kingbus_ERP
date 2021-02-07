from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm
from .models import DispatchConsumer, DispatchInfo, DispatchOrder, DispatchRoute
from crudmember.models import User

from datetime import datetime, timedelta

class TodayList(generic.ListView):
    template_name = 'dispatch/today.html'
    context_object_name = 'dispatch_list'

    def get_queryset(self):
        ''' 어제 오늘 내일 배차지시서 보여줌 '''
        dispatch_list = []
        today = datetime.now().day
        tomorrow = (datetime.now() + timedelta(days=1)).day
        yesterday = (datetime.now() - timedelta(days=1)).day
        for order in DispatchOrder.objects.all():
            day = order.pub_date.day
            
            if day == today or day == yesterday or day == tomorrow:
                dispatch_list.append(order)
        #프린트 할 수 있게 파일로 만들어 줘야 됨 > JS로 프린트 할 수 있게 할 거
        return dispatch_list
        

class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_list'
    model = DispatchOrder

######
def order_create(request):
    res_data = {}
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            print("테스트",form.cleaned_data['consumer_name'])
            consumer = DispatchConsumer(
                name = form.cleaned_data['consumer_name'],
                tel = form.cleaned_data['consumer_tel'],
            )
            consumer.save()

            order = DispatchOrder(
                writer = User.objects.get(pk=request.session.get('user')),
                consumer = consumer,
                bus_cnt = form.cleaned_data['bus_cnt'],
                price = form.cleaned_data['price'],
                kinds = form.cleaned_data['kinds'],
                purpose = form.cleaned_data['purpose'],
                bus_type = form.cleaned_data['bus_type'],
                requirements = form.cleaned_data['requirements'],
                people_num = form.cleaned_data['people_num'],
                pay_type = form.cleaned_data['pay_type'],
                first_departure_date = request.POST.get('first_departure_date', None),
            )
            order.save()
            return redirect(reverse('dispatch:order_detail', args=(order.id,)))
            #return redirect('/dispatch/order/{0}/'.format(order.id))
        #form형식에 맞지 않는 POST일때
        return redirect('dispatch:order_create')
    else:
        context = {
            'form' : OrderForm(),
        }
        
    return render(request, 'dispatch/order_create.html', context)

'''
class OrderCreate(generic.FormView):
    model = DispatchOrder
    form_class = OrderForm
    context_object_name = 'order' #1
    
    template_name = 'dispatch/order_create.html' #2
    success_url = '/' #3

    def form_valid(self, form):
        print("xxxxxxxxxxxxxx")
        order = form.save()
        return super().form_valid(form)
'''

class OrderDetail(generic.DetailView):
    template_name = 'dispatch/order_detail.html'
    context_object_name = 'order'
    model = DispatchOrder

class OrderUpdate(generic.edit.UpdateView):
    model = DispatchOrder
    form_class = OrderForm
    
    context_object_name = 'order' #1
    
    template_name = 'dispatch/order_edit.html' #2
    success_url = '/' #3


'''
def order_edit(request, order_id):
    try:
        order = DispatchOrder.objects.get(pk=order_id)
    except Exception as error:
        print("\n에러:", e)
        raise 404

    if request.method == 'GET':
    
    return render(request, 'dispatch/order_edit.html')
     '''
def order_delete(request, order_id):
    return render(request, 'dispatch/order_edit.html')

def schedule(request):
    return render(request, 'dispatch/schedule.html')

def management(request):
    return render(request, 'dispatch/management.html')
def management_detail(request, order_id):
    return render(request, 'dispatch/management_detail.html')
def management_create(request, order_id):
    return render(request, 'dispatch/management_create.html')
def management_edit(request, order_id):
    return render(request, 'dispatch/management_edit.html')