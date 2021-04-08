from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm, ConsumerForm
from .models import DispatchConsumer, DispatchConnect, DispatchOrder
from crudmember.models import User

from datetime import datetime, timedelta

class DispatchList(generic.ListView):
    template_name = 'dispatch/dispatch_list.html'
    context_object_name = 'dispatch_list'
    paginate_by = 10
    model = DispatchOrder


    def get_queryset(self):
        '''
        dispatch_list = []
        today = datetime.now().day
        tomorrow = (datetime.now() + timedelta(days=1)).day
        yesterday = (datetime.now() - timedelta(days=1)).day
        for order in DispatchOrder.objects.all():
            day = order.pub_date.day
            if day == today or day == yesterday or day == tomorrow:
                dispatch_list.append(order)
        '''
        dispatch_list = DispatchOrder.objects.order_by('-id')
        #프린트 할 수 있게 파일로 만들어 줘야 됨 > JS로 프린트 할 수 있게 할 거        
        return dispatch_list

    # 페이징 처리
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context

# 날짜별-노선별 배차지시서 
class DispatchDailyRouteList(generic.ListView):
    template_name = 'dispatch/dispatch_daily_route.html'
    context_object_name = 'dispatch'

    def get_queryset(self):
        dispatch = DispatchOrder.objects.filter(first_departure_date__contains=self.kwargs['date'])
        return dispatch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dispatch = DispatchOrder.objects.filter(first_departure_date__contains=self.kwargs['date'])
        context['routes'] = []
        for i in dispatch:
            context['routes'].append(DispatchRoute.objects.filter(order_id=i))
        return context

# 날짜별-차량별 배차지시서
class DispatchDailyBusList(generic.ListView):
    template_name = 'dispatch/dispatch_daily_bus.html'
    context_object_name = 'dispatch'

    def get_queryset(self):
        dispatch = DispatchOrder.objects.filter(first_departure_date__contains=self.kwargs['date'])
        return dispatch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dispatch = DispatchOrder.objects.filter(first_departure_date__contains=self.kwargs['date'])
        context['routes'] = []
        for i in dispatch:
            context['routes'].append(DispatchRoute.objects.filter(order_id=i))
        return context


class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_list'
    model = DispatchOrder

def order_create(request):
    '''
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        #print("teststsestsetst", request.POST, type(request.POST))
        update = 'create'
        order = update_order(request, update)
        if order:
            return redirect(reverse('dispatch:order_detail', args=(order.id,)))
            #return redirect('/dispatch/order/{0}/'.format(order.id))
        #form형식에 맞지 않는 POST일때
        return redirect('dispatch:order_create')
    '''
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)
        consumer_form = ConsumerForm(request.POST)        
        if order_form.is_valid() and consumer_form.is_valid():
            order = order_form.save(commit=False)
            order.creator = creator
            print(order)
            order.save()
            consumer = consumer_form.save(commit=False)
            consumer.save()
            
            return redirect('accounting:outlay_list')
    else:
        context = {
            'order_form' : OrderForm(),
            'consumer_form' : ConsumerForm(),
        }
        
    return render(request, 'dispatch/order_create.html', context)


def update_order(request, update):
    order_form = OrderForm(request.POST)
    consumer_form = ConsumerForm(request.POST)
    if order_form.is_valid() and consumer_form.is_valid():
        if update == 'create':
            consumer = DispatchConsumer(
                name = consumer_form.cleaned_data['name'],
                tel = consumer_form.cleaned_data['tel'],
            )
            consumer.save()

            order = order_form.save(commit=False) #commit 설정을 해줘야 되나? >> 값 불러오는 용도라 저장은 안하려고 False해줌
            order.consumer=consumer
            order.writer = User.objects.get(pk=request.session.get('user'))
            order.save()
            return order
        else:
            update.consumer.name = consumer_form.cleaned_data['name']
            update.consumer.tel = consumer_form.cleaned_data['tel']
            update.consumer.save()

            update.writer = User.objects.get(pk=request.session.get('user'))
            update.consumer = update.consumer
            

            update.bus_cnt = order_form.cleaned_data['bus_cnt']
            update.price = order_form.cleaned_data['price']
            update.kinds = order_form.cleaned_data['kinds']
            update.purpose = order_form.cleaned_data['purpose']
            update.bus_type = order_form.cleaned_data['bus_type']
            update.requirements = order_form.cleaned_data['requirements']
            update.people_num = order_form.cleaned_data['people_num']
            update.pay_type = order_form.cleaned_data['pay_type']
            update.departure_date = order_form.cleaned_data['departure_date']
            update.save()
            return update


    return False

class OrderCreate(generic.edit.CreateView):
    context_object_name = 'order' #1
    form_class = OrderForm
    
    template_name = 'dispatch/order_create.html' #2
    success_url = '/' #3


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
    


def order_edit(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)

    if request.method == 'GET':
        context = {
            'order_form' : OrderForm(instance=order),
            'consumer_form' : ConsumerForm(instance=order.consumer),
            'order' : order,
        }
        return render(request, 'dispatch/order_edit.html', context)
    elif request.method == 'POST':
        order_edit = update_order(request, order)
        if order_edit:
            return redirect(reverse('dispatch:order_detail', args=(pk,)))
        return redirect(reverse('dispatch:order_edit', args=(pk,)))

    
def order_delete(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    print("테스트ㅡㅡ", request.session['user'])
    if order.writer.pk == request.session['user']: # ?? 작성자만 지울 수 있게 하나?
        order.consumer.delete()
        order.delete()
        return redirect('dispatch:order')
    return redirect(reverse('dispatch:order_detail', args=(pk,)))

class ScheduleList(generic.ListView):
    template_name = 'dispatch/schedule.html'
    context_object_name = 'order_list'
    model = DispatchOrder
    
class ScheduleDetail(generic.ListView):
    template_name = 'dispatch/schedule_detail.html'
    context_object_name = 'order'
    model = DispatchOrder

    def get_queryset(self):
        ''' 지정한 날짜 배차지시서 보여줌 '''
        dispatch_list = []
        date = self.kwargs['date']
        for order in DispatchOrder.objects.all():
            order_date = str(order.departure_date)[:10]
            print(order_date)
            if date == order_date:
                dispatch_list.append(order)
        return dispatch_list

class ManagementList(generic.ListView):
    template_name = 'dispatch/management.html'
    context_object_name = 'order_list'
    model = DispatchOrder

class ManagementDetail(generic.DetailView):
    template_name = 'dispatch/management_detail.html'
    context_object_name = 'order'
    model = DispatchOrder

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(ManagementDetail, self).get_context_data(**kwargs)
        order = get_object_or_404(DispatchOrder, pk=self.kwargs['pk'])
        context['routes'] = DispatchRoute.objects.filter(order_id=order)
        context['connect'] = DispatchRoute.objects.filter(order_id=order)
        return context


# 차량관리, 인사관리 완료 후 작성
def management_create(request, order_id):
    return render(request, 'dispatch/management_create.html')
def management_edit(request, order_id):
    return render(request, 'dispatch/management_edit.html')