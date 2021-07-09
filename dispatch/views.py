from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm, ConsumerForm, ConnectForm, RegularlyOrderForm
from .models import DispatchConsumer, DispatchConnect, DispatchOrder, RegularlyGroup
from crudmember.models import User
from utill.decorator import option_year_deco

from datetime import datetime, timedelta

class DispatchList(generic.ListView):
    template_name = 'dispatch/dispatch_list.html'
    context_object_name = 'dispatch_list'
    paginate_by = 10
    model = DispatchOrder

    
    def get_queryset(self):
        self.selected_year = self.request.GET.get('year', str(datetime.now())[:4])
        self.selected_month = self.request.GET.get('month', str(datetime.now())[5:7])
        
        month = self.selected_year +"-" + self.selected_month
        dispatch_list = DispatchOrder.objects.filter(check=True).filter(departure_date__startswith=month).order_by('-departure_date')
        return dispatch_list
    
    # 페이징 처리
    @option_year_deco
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
        #페이징 끝
        
        
        date = []
        for order in context['dispatch_list']:
            date.append(order.departure_date[:10])

        context['date'] = set(date) #중복값 제거
        context['selected_year'] = self.selected_year
        context['selected_month'] = self.selected_month
        context['int_selected_year'] = int(self.selected_year)
        context['int_selected_month'] = int(self.selected_month)
        return context

# 날짜별-노선별 배차지시서 
class DispatchDailyRouteList(generic.ListView):
    template_name = 'dispatch/dispatch_daily_route.html'
    context_object_name = 'dispatch'

    def get_queryset(self):
        dispatch = DispatchOrder.objects.filter(departure_date__contains=self.kwargs['date']).filter(check=True)
        return dispatch

# 날짜별-차량별 배차지시서
class DispatchDailyBusList(generic.ListView):
    template_name = 'dispatch/dispatch_daily_bus.html'
    context_object_name = 'dispatch'

    def get_queryset(self):
        dispatch = DispatchOrder.objects.filter(departure_date__contains=self.kwargs['date']).filter(check=True)
        return dispatch

class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_list'
    model = DispatchOrder

def order_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)
        consumer_form = ConsumerForm(request.POST)        
        if order_form.is_valid() and consumer_form.is_valid():
            consumer = consumer_form.save(commit=False)
            consumer.save()
            order = order_form.save(commit=False)
            order.creator = creator
            order.consumer = consumer
            order.save()
            
            return redirect('dispatch:order')
    else:
        context = {
            'order_form' : OrderForm(),
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

    if request.method == 'POST':
        if User.objects.get(pk=request.session['user']).authority == "관리자":
            creator = get_object_or_404(User, pk=request.session.get('user'))
            order_form = OrderForm(request.POST)
            consumer_form = ConsumerForm(request.POST)
            if order_form.is_valid() and consumer_form.is_valid():
                edit_consumer = consumer_form.save(commit=False)
                consumer.delete()
                edit_consumer.save()
                edit_order = order_form.save(commit=False)
                edit_order.creator = creator
                edit_order.consumer = edit_consumer
                order.delete()
                edit_order.id = pk
                edit_order.save()
            return redirect(reverse('dispatch:order_detail', args=(pk,)))
    else:
        context = {
            'order_form' : OrderForm(instance=order),
            'consumer_form' : ConsumerForm(instance=consumer),         
        }
        return render(request, 'dispatch/order_edit.html', context)

def order_delete(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    print("테스트ㅡㅡ", request.session['user'])
    if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
        if order.info_order.all():
            order.info_order.all().delete()
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

def management_delete(request, pk, c_pk):
    connect = get_object_or_404(DispatchConnect, pk=c_pk)
    order = get_object_or_404(DispatchOrder, pk=pk)
    if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
        connect.delete()
    return redirect(reverse('dispatch:order_detail', args=(pk,)))

#######

class RegularlyOrderList(generic.ListView):
    template_name = 'dispatch/regularly_order_list.html'
    context_object_name = 'dispatch_list'
    paginate_by = 10
    model = DispatchOrder

    def get_queryset(self):
        dispatch_list = DispatchOrder.objects.filter(regularly=True)
        return dispatch_list

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
        #페이징 끝

        return context



def regularly_order_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = RegularlyOrderForm(request.POST)
        consumer_form = ConsumerForm(request.POST)
        if order_form.is_valid() and consumer_form.is_valid():
            consumer = consumer_form.save(commit=False)
            consumer.save()
            order = order_form.save(commit=False)
            order.creator = creator
            order.consumer = consumer
            order.regularly = True
            order.save()
            
            return redirect('dispatch:regularly_order_create')
    else:
        context = {
            'order_form' : RegularlyOrderForm(),
            'consumer_form' : ConsumerForm(),
        }
        
    return render(request, 'dispatch/regularly_order_create.html', context)


###########################################

def regularly_order_edit(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    consumer = order.consumer

    if request.method == 'POST':
        creator = get_object_or_404(User, pk=request.session.get('user'))
        if User.objects.get(pk=request.session['user']).authority == "관리자" or order.creator == creator:
            order_form = RegularlyOrderForm(request.POST)
            consumer_form = ConsumerForm(request.POST)
            if order_form.is_valid() and consumer_form.is_valid():
                edit_consumer = consumer_form.save(commit=False)
                consumer.delete()
                edit_consumer.save()
                edit_order = order_form.save(commit=False)
                edit_order.creator = creator
                edit_order.consumer = edit_consumer
                order.delete()
                edit_order.regularly = True
                edit_order.id = pk
                edit_order.save()
                return redirect('dispatch:regularly_order_create')
    else:
        context = {
            'order_form' : RegularlyOrderForm(instance=order),
            'consumer_form' : ConsumerForm(instance=consumer),
        }
        return render(request, 'dispatch/regularly_order_edit.html', context)

def regularly_order_delete(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    print("테스트ㅡㅡ", request.session['user'])
    if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
        if order.info_order.all():
            order.info_order.all().delete()
        order.delete()
        return redirect('dispatch:regularly_order_list')
    return redirect(reverse('dispatch:regularly_order_list', args=(pk,)))


class RegularlyOrderGroup(generic.ListView):
    template_name = 'dispatch/regularly_order_group.html'
    context_object_name = 'routes'
    model = DispatchOrder

    def get_queryset(self):
        route_list = DispatchOrder.objects.filter(regularly=True).order_by('-regularly_group')
        return route_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_group_route'] = DispatchOrder.objects.filter(regularly=True).filter(regularly_group=None)
        context['group_list'] = RegularlyGroup.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        """
        그룹 추가하는 인풋 하나 따로 만들어서 그룹 추가해서 셀렉트 박스에 보여주기
        """
        group = RegularlyGroup(
            name = request.POST.get('name'),
            company = request.POST.get('company')
        )
        group.save()
        
        return redirect('dispatch:regularly_order_group')
#####

def regularly_order_group_create(request):
        """
        셀렉트 박스로 그룹 선택해서 그룹에 추가, 
        만약 그룹을 새로 만드려면 맨밑에 그룹추가 선택하면 그룹이름이랑 업체명 인풋 생김
        """
        if request.method == "POST":
            group_pk = request.POST.get('group')
            routes = request.POST.getlist('route')
            if group_pk:
                group = get_object_or_404(RegularlyGroup, pk=group_pk)

                for i in routes:
                    route = get_object_or_404(DispatchOrder, pk=i)
                    route.regularly_group = group
                    route.save()
            
            else:
                for i in routes:
                    route = get_object_or_404(DispatchOrder, pk=i)
                    route.regularly_group = None
                    route.save()
            return redirect('dispatch:regularly_order_group')    
        else:
            raise Http404
        
def regularly_order_group_edit(request, pk):
    context = {}
    order = get_object_or_404(DispatchOrder, pk=pk)

    if request.method == "POST":
        print("POST")
    else:
        context = {
            'order' : order,
            'connect_form' : ConnectForm(),
        }
    return render(request, 'dispatch/regularly_order_group_edit.html', context)

def regularly_order_group_delete(request, pk):
    order = get_object_or_404(DispatchOrder, pk=pk)
    print("테스트ㅡㅡ", request.session['user'])
    if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
        if order.info_order.all():
            order.info_order.all().delete()
        order.delete()
        return redirect('dispatch:regularly')
    return redirect(reverse('dispatch:regularly_order_group_create', args=(pk,)))


def regularly_order_management_create(request, pk):
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
            return redirect(reverse('dispatch:regularly_order_detail',args=(pk,)))
    else:
        context = {
            'order' : order,
            'connect_form' : ConnectForm(),
        }
    return render(request, 'dispatch/regularly_order_management_create.html', context)


def regularly_order_management_edit(request, pk, c_pk):
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
                return redirect(reverse('dispatch:regularly_order_detail',args=(pk,)))
    else:
        context = {
            'order' : order,
            'connect_form' : ConnectForm(instance=connect),
        }
    return render(request, 'dispatch/regularly_order_management_create.html', context)

def regularly_order_management_delete(request, pk, c_pk):
    connect = get_object_or_404(DispatchConnect, pk=c_pk)
    order = get_object_or_404(DispatchOrder, pk=pk)
    if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
        connect.delete()
    return redirect(reverse('dispatch:regularly_order_detail', args=(pk,)))
