from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm, ConsumerForm, RouteForm, ConnectForm
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
        dispatch = DispatchOrder.objects.filter(departure_date__contains=self.kwargs['date'])
        return dispatch
'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dispatch = DispatchOrder.objects.filter(departure_date__contains=self.kwargs['date'])
        context['routes'] = []
        
        return context
'''
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
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)
        route_form = RouteForm(request.POST)
        consumer_form = ConsumerForm(request.POST)        
        if order_form.is_valid() and consumer_form.is_valid():
            consumer = consumer_form.save(commit=False)
            consumer.save()
            route = route_form.save(commit=False)
            route.save()
            order = order_form.save(commit=False)
            order.creator = creator
            order.consumer = consumer
            order.route = route
            order.save()
            
            return redirect('dispatch:order')
    else:
        context = {
            'order_form' : OrderForm(),
            'route_form' : RouteForm(),
            'consumer_form' : ConsumerForm(),
        }
        
    return render(request, 'dispatch/order_create.html', context)

class OrderDetail(generic.DetailView):
    template_name = 'dispatch/order_detail.html'
    context_object_name = 'order'
    model = DispatchOrder

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(OrderDetail, self).get_context_data(**kwargs)
        order = get_object_or_404(DispatchOrder, pk=self.kwargs['pk'])
        context['connects'] = order.info_order.all()

        return context

def order_edit(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    consumer = order.consumer
    route = order.route

    if request.method == 'POST':
        if User.objects.get(pk=request.session['user']).authority == "관리자":
            creator = get_object_or_404(User, pk=request.session.get('user'))
            order_form = OrderForm(request.POST)
            consumer_form = ConsumerForm(request.POST)
            route_form = RouteForm(request.POST)
            if order_form.is_valid() and consumer_form.is_valid():
                edit_consumer = consumer_form.save(commit=False)
                consumer.delete()
                edit_consumer.save()
                edit_route = route_form.save(commit=False)
                route.delete()
                edit_route.save()
                edit_order = order_form.save(commit=False)
                edit_order.creator = creator
                edit_order.consumer = edit_consumer
                edit_order.route = edit_route
                order.delete()
                edit_order.id = pk
                edit_order.save()
            return redirect(reverse('dispatch:order_detail', args=(pk,)))
    else:
        context = {
            'order_form' : OrderForm(instance=order),
            'consumer_form' : ConsumerForm(instance=consumer),
            'route_form' : RouteForm(instance=route),            
        }
        return render(request, 'dispatch/order_edit.html', context)

def order_delete(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    print("테스트ㅡㅡ", request.session['user'])
    if order.creator.pk == request.session['user']: # ?? 작성자만 지울 수 있게 하나?
        order.consumer.delete()
        order.route.delete()
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
    '''
    def get_queryset(self):
        order = DispatchOrder.objects.filter(check=False)
        return order
    '''
    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(ManagementList, self).get_context_data(**kwargs)
        context['check_order'] = DispatchOrder.objects.filter(check=True)
        context['not_check_order'] = DispatchOrder.objects.filter(check=False)
        return context

class ManagementDetail(generic.DetailView):
    template_name = 'dispatch/management_detail.html'
    context_object_name = 'order'
    model = DispatchOrder


    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(ManagementDetail, self).get_context_data(**kwargs)
        order = get_object_or_404(DispatchOrder, pk=self.kwargs['pk'])
        context['connects'] = order.info_order.all()
        context['manage_form'] = []
        
        for i in context['connects']:
            context['manage_form'].append(ConnectForm(instance=i))
        return context


def management_create(request, pk):
    context = {}
    order = get_object_or_404(DispatchOrder, pk=pk)

    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        connect_form = ConnectForm(request.POST)
        if connect_form.is_valid():
            connect = connect_form.save(commit=False)
            connect.creator=creator
            connect.order_id=order
            connect.save()
            return redirect(reverse('dispatch:order_detail',args=(pk,)))
    else:
        context = {
            'order' : order,
            'connect_form' : ConnectForm(),
        }
    return render(request, 'dispatch/management_create.html', context)


def management_edit(request, pk, c_pk):
    context = {}
    connect = get_object_or_404(DispatchConnect, pk=c_pk)
    order = connect.order_id

    if request.method == "POST":
        if User.objects.get(pk=request.session['user']).authority == "관리자":
            creator = get_object_or_404(User, pk=request.session.get('user'))
            connect_form = ConnectForm(request.POST)
            if connect_form.is_valid():
                edit_connect = connect_form.save(commit=False)
                edit_connect.pk = c_pk
                edit_connect.order_id = order
                connect.delete()
                edit_connect.save()
                return redirect(reverse('dispatch:order_detail',args=(pk,)))
    else:
        context = {
            'order' : order,
            'connect_form' : ConnectForm(instance=connect),
        }
    return render(request, 'dispatch/management_create.html', context)