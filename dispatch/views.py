from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm
from .models import DispatchConsumer, DispatchInfo, DispatchOrder, DispatchRoute

class DispatchList(generic.ListView):
    template_name = 'dispatch/today.html'
    context_object_name = 'dispatch_list'

    def get_queryset(self):
        ''' 어제 오늘 내일 배차지시서 보여줌 '''

class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_lsit'
    model = DispatchOrder

######
def order_create(request):
    if request.method == "POST":
        create_data = createContext(request)

        consumer = DispatchConsumer(
            name = create_data['consumer_name'],
            tel = create_data['consumer_tel'],
        )
        consumer.save()

        order = DispatchOrder(
            writer = create_data['writer'],
            consumer = consumer,
            bus_cnt = create_data['bus_cnt'],
            price = create_data['price'],
            kinds = create_data['kinds'],
            purpose = create_data['purpose'],
            bus_type = create_data['bus_type'],
            requirements = create_data['requirements'],
            people_num = create_data['people_num'],
            pub_date = create_data['pub_date'],
            pay_type = create_data['pay_type'],
            first_departure_date = create_data['first_departure_date'],
        )
        order.save()
        return redirect(reverse('dispatch:order_detail', args=(order.pk)))
    return render(request, 'dispatch/order_create.html')
        

    return render(request, 'dispatch/order_create.html')
def createContext(request):
    context = {    
        'writer': User.objects.get(pk=request.session['user']),
        'bus_cnt': request.POST.get('bus_cnt', None),
        'price': request.POST.get('price', None),
        'kinds': request.POST.get('kinds', None),
        'purpose': request.POST.get('purpose', None),
        'bus_type': request.POST.get('bus_type', None),
        'requirements': request.POST.get('requirements', None),
        'people_num': request.POST.get('people_num', None),
        'pub_date': request.POST.get('pub_date', None),
        'pay_type': request.POST.get('pay_type', None),
        'first_departure_date': request.POST.get('first_departure_date', None),

        'consumer_name': request.POST.get('consumer_name', None),
        'consumer_tel': request.POST.get('consumer_tel', None),
    }
    return context

class OrderCreate(generic.CreateView):
    model = DispatchOrder
    fields = '__all__'
    context_object_name = 'order' #1
    
    template_name = 'dispatch/order_create.html' #2
    success_url = '/' #3
    
    #get object
    def get_object(self): 
        order = get_object_or_404(DispatchOrder, pk=self.kwargs['pk']) #4

        return order

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
    #get object
    def get_object(self): 
        order = get_object_or_404(DispatchOrder, pk=self.kwargs['pk']) #4

        return order
        '''
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