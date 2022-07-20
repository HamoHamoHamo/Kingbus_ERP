from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm, ConnectForm, RegularlyForm
from .models import DispatchOrderConnect, DispatchOrder, DispatchRegularly, RegularlyGroup, DispatchRegularlyConnect
from crudmember.models import User
from humanresource.models import Member
from vehicle.models import Vehicle

from datetime import datetime, timedelta, date
# from utill.decorator import option_year_deco

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]

def schedule(request):

    return render(request, 'dispatch/schedule.html')

class DocumentList(generic.ListView):
    template_name = 'dispatch/document.html'
    context_object_name = 'order_list'
    model = DispatchOrder

    def get_queryset(self):
        date = self.request.GET.get('date', TODAY)
        order_list = DispatchOrder.objects.filter(departure_date__lte=f'{date}T24:00').filter(arrival_date__gte=f'{date}T00:00')
        return order_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departure_date = []
        time = []
        num_days = []

        for order in context['order_list']:
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
            a_w = WEEK[d_date.weekday()]
            a_y = a_y[2:4]
            
            date_diff = (a_date - d_date) + timedelta(days=1)
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
        context['date'] = self.request.GET.get('date', TODAY)
        
        return context
    
class RegularlyDispatchList(generic.ListView):
    template_name = 'dispatch/regularly.html'
    context_object_name = 'order_list'
    paginate_by = 10
    model = DispatchRegularly

    def get_queryset(self):
        group = self.request.GET.get('group', '')
        route = self.request.GET.get('route', '')
        
        dispatch_list = []
        group_data = None
        if route or group:
            if group:
                group_data = RegularlyGroup.objects.get(name=group)
                dispatch_list = group_data.regularly_info.all()
            if route:
                if group_data:
                    dispatch_list = group_data.regularly_info.filter(route__contains=route)
                else:
                    dispatch_list = DispatchRegularly.objects.filter(route__contains=route)
        else:
            dispatch_list = DispatchRegularly.objects.all().order_by('group', 'number')
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
        
        group_name = self.request.GET.get('group', '')
        route_name = self.request.GET.get('route', '')
        date = self.request.GET.get('date', TODAY)
        context['group_list'] = RegularlyGroup.objects.all()
        context['group_name'] = group_name
        context['route_name'] = route_name
        context['date'] = date

        vehicle_list = Vehicle.objects.prefetch_related('info_regulary_bus_id', 'info_bus_id').filter(use='y')

        r_enter_cnt = []
        r_leave_cnt = []
        order_cnt = []
        for vehicle in vehicle_list:
            r_enter_cnt.append(vehicle.info_regulary_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00').filter(work_type="출근").count())
            r_leave_cnt.append(vehicle.info_regulary_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00').filter(work_type="퇴근").count())
            order_cnt.append(vehicle.info_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00').count())
            print(vehicle.info_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00'))
        
        print("ORDERCNT", order_cnt)
        context['r_enter_cnt'] = r_enter_cnt
        context['r_leave_cnt'] = r_leave_cnt
        context['order_cnt'] = order_cnt
        context['vehicle_list'] = vehicle_list

        connect_list = []
        for order in context['order_list']:
            connect_list.append(order.info_regularly.filter(departure_date__lte=f'{date} 24:59').filter(arrival_date__gte=f'{date} 00:00'))
        context['connect_list'] = connect_list
        return context

def regularly_connect_create(request):
    if request.method == "POST":
        creator = get_object_or_404(User, id=request.session.get('user'))
        order = get_object_or_404(DispatchRegularly, id=request.POST.get('id', None))
        bus_list = request.POST.getlist('vehicle')
        date = request.POST.get('date', None)

        connect = order.info_regularly.filter(departure_date__startswith=date)
        connect.delete()

        for bus in bus_list:
            vehicle = Vehicle.objects.get(id=bus)
            r_connect = DispatchRegularlyConnect(
                regularly_id = order,
                bus_id = vehicle,
                driver_id = vehicle.driver,
                departure_date = f'{date} {order.departure_time}',
                arrival_date = f'{date} {order.arrival_time}',
                work_type = order.work_type,
                driver_allowance = order.driver_allowance,
                creator = creator
            )
            r_connect.save()

        return redirect('dispatch:regularly')
    else:
        return HttpResponseNotAllowed(['post'])

class RegularlyRouteList(generic.ListView):
    template_name = 'dispatch/regularly_route.html'
    context_object_name = 'order_list'
    paginate_by = 10
    model = DispatchRegularly

    def get_queryset(self):
        group = self.request.GET.get('group', '')
        route = self.request.GET.get('route', '')
        dispatch_list = []
        group_data = None
        if route or group:
            if group:
                group_data = RegularlyGroup.objects.get(name=group)
                dispatch_list = group_data.regularly_info.all()
            if route:
                if group_data:
                    dispatch_list = group_data.regularly_info.filter(route__contains=route)
                else:
                    dispatch_list = DispatchRegularly.objects.filter(route__contains=route)
        else:
            dispatch_list = DispatchRegularly.objects.all().order_by('group', 'number')
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

        group = self.request.GET.get('group', '')
        route = self.request.GET.get('route', '')

        context['group_list'] = RegularlyGroup.objects.all()
        context['group_old'] = group
        context['route_old'] = route

        return context

def regularly_order_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = RegularlyForm(request.POST)
        print("RRRR", request.POST)

        if order_form.is_valid():
            print("VALID")
            if datetime.strptime(request.POST.get('contract_start_date'), FORMAT) > datetime.strptime(request.POST.get('contract_end_date'), FORMAT):
                context = {}
                # context['order_list'] = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')
                context['group_list'] = RegularlyGroup.objects.all()
                # context['error'] = "출발일이 도착일보다 늦습니다"
                #raise BadRequest('출발일이 도착일보다 늦습니다.')
                #return render(request, 'dispatch/regularly_order_create.html', context)
                raise Http404
            post_group = request.POST.get('group', None)
            try:
                regularly_group = RegularlyGroup.objects.get(pk=post_group)
            except Exception as e:
                regularly_group = None

            week = ' '.join(request.POST.getlist('week', None))
            # regularly = RegularlyOrder(
            #     week=week,
            #     term_begin=request.POST.get('term_begin', None),
            #     term_end=request.POST.get('term_end', None),
            #     regularly_group=regularly_group,
            # )
            # regularly.save()
            
            order = order_form.save(commit=False)
            order.week = week
            order.creator = creator
            order.group = regularly_group
            order.route = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            order.save()
            return redirect('dispatch:regularly_route')

    else:
        raise Http404

def regularly_order_edit(request):
    id = request.POST.get('id', None)
    order = get_object_or_404(DispatchRegularly, pk=id)
    
    if request.method == 'POST':
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = RegularlyForm(request.POST)
        if order_form.is_valid():
            print("VALID")
            group = get_object_or_404(RegularlyGroup, pk=request.POST.get('group'))
            week = ' '.join(request.POST.getlist('week', None))
        
            if datetime.strptime(request.POST.get('contract_start_date'), FORMAT) > datetime.strptime(request.POST.get('contract_end_date'), FORMAT):
                #raise BadRequest('출발일이 도착일보다 늦습니다.')
                raise Http404
            route_name = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            
            order.references = order_form.cleaned_data['references']
            order.departure = order_form.cleaned_data['departure']
            order.arrival = order_form.cleaned_data['arrival']
            order.departure_time = order_form.cleaned_data['departure_time']
            order.arrival_time = order_form.cleaned_data['arrival_time']
            order.bus_type = order_form.cleaned_data['bus_type']
            order.bus_cnt = order_form.cleaned_data['bus_cnt']
            order.price = order_form.cleaned_data['price']
            order.driver_allowance = order_form.cleaned_data['driver_allowance']
            order.number = order_form.cleaned_data['number']
            order.customer = order_form.cleaned_data['customer']
            order.customer_phone = order_form.cleaned_data['customer_phone']
            order.contract_start_date = order_form.cleaned_data['contract_start_date']
            order.contract_end_date = order_form.cleaned_data['contract_end_date']
            order.work_type = order_form.cleaned_data['work_type']

            order.week = week
            order.route = route_name
            order.group = group
            order.creator = creator
            order.save()
            
            return redirect('dispatch:regularly_route')
        else: 
            raise Http404
    else:
        raise Http404

def regularly_order_delete(request):
    if request.method == "POST":
        order_list = request.POST.getlist("check")
        for order_id in order_list:
            order = get_object_or_404(DispatchRegularly, pk=order_id)
            # if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
                # order.delete()
            order.delete()
        return redirect('dispatch:regularly_route')
    else:
        raise Http404

def regularly_group_create(request):
    if request.method == "POST":
        group = RegularlyGroup(
            name = request.POST.get('name'),
            creator = get_object_or_404(User, pk=request.session['user'])
        )
        group.save()
        return redirect('dispatch:regularly_route')
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_edit(request):

    if request.method == "POST":
        id_list = request.POST.getlist('group_id', None)
        name_list = request.POST.getlist('group', None)
        
        cnt = 0
        for id in id_list:
            group = get_object_or_404(RegularlyGroup, id=id)
            group.name = name_list[cnt]
            group.save()
            cnt += 1
        return redirect('dispatch:regularly_route')
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_delete(request):
    if request.method == "POST":
        group = get_object_or_404(RegularlyGroup, id=request.POST.get('group_id', None))
        group.delete()
        return redirect('dispatch:regularly_route')
    else:
        return HttpResponseNotAllowed(['POST'])

class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_list'
    model = DispatchOrder
    paginate_by = 10

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        route = self.request.GET.get('route')
        customer = self.request.GET.get('customer')
        self.next_week = datetime.strptime(TODAY, FORMAT) + timedelta(days=7)

        if start_date or end_date or route or customer:
            dispatch_list = []
            if start_date and end_date:
                dispatch_list = DispatchOrder.objects.exclude(arrival_date__lt=start_date).exclude(departure_date__gt=end_date).order_by('departure_date')
                # dispatch_list = DispatchOrder.objects.filter(departure_date__range=[start_date + "T00:00", end_date + "T24:00"]).order_by('departure_date')
            if route:
                if dispatch_list:
                    dispatch_list = dispatch_list.filter(route__contains=route).order_by('departure_date')
                else:
                    dispatch_list = DispatchOrder.objects.filter(route__contains=route).order_by('departure_date')
            if customer:
                if dispatch_list:
                    dispatch_list = dispatch_list.filter(customer__contains=customer).order_by('departure_date')
                else:
                    dispatch_list = DispatchOrder.objects.filter(customer__contains=customer).order_by('departure_date')
        else:
            
            dispatch_list = DispatchOrder.objects.exclude(arrival_date__lt=TODAY).exclude(departure_date__gt=self.next_week).order_by('departure_date')
        
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
        departure_date = []
        time = []
        num_days = []

        for order in context['order_list']:
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
            a_w = WEEK[d_date.weekday()]
            a_y = a_y[2:4]
            
            date_diff = (a_date - d_date) + timedelta(days=1)
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
        context['route_old'] = self.request.GET.get('route', '')
        context['customer_old'] = self.request.GET.get('customer', '')
        start_date_old = self.request.GET.get('start_date', TODAY)
        context['start_date_old'] = start_date_old
        end_date_old = self.request.GET.get('end_date', self.next_week.strftime(FORMAT))
        context['end_date_old'] = end_date_old

        vehicle_list = Vehicle.objects.prefetch_related('info_regulary_bus_id', 'info_bus_id').filter(use='y')

        r_enter_cnt = []
        r_leave_cnt = []
        order_cnt = []
        for vehicle in vehicle_list:
            r_enter_cnt.append(vehicle.info_regulary_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00').filter(work_type="출근").count())
            r_leave_cnt.append(vehicle.info_regulary_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00').filter(work_type="퇴근").count())
            order_cnt.append(vehicle.info_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00').count())
            print(vehicle.info_bus_id.filter(departure_date__lte=f'{TODAY} 24:59').filter(arrival_date__gte=f'{TODAY} 00:00'))
        
        print("ORDERCNT", order_cnt)
        context['r_enter_cnt'] = r_enter_cnt
        context['r_leave_cnt'] = r_leave_cnt
        context['order_cnt'] = order_cnt
        context['vehicle_list'] = vehicle_list

        connect_list = []
        for order in context['order_list']:
            connect_list.append(order.info_order.all())
        context['connect_list'] = connect_list

        return context

def order_connect_create(request):
    if request.method == "POST":
        creator = get_object_or_404(User, id=request.session.get('user'))
        order = get_object_or_404(DispatchOrder, id=request.POST.get('id', None))
        bus_list = request.POST.getlist('vehicle')
        
        connect = order.info_order.all()
        connect.delete()

        for bus in bus_list:
            vehicle = Vehicle.objects.get(id=bus)
            connect = DispatchOrderConnect(
                order_id = order,
                bus_id = vehicle,
                driver_id = vehicle.driver,
                departure_date = order.departure_date,
                arrival_date = order.arrival_date,
                driver_allowance = order.driver_allowance,
                creator = creator
            )
            connect.save()

        return redirect('dispatch:order')
    else:
        return HttpResponseNotAllowed(['post'])


def order_create(request):    
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)
        print("POST", request.POST)
        if order_form.is_valid():
            post_departure_date = request.POST.get('departure_date', None).replace('T', ' ')
            post_arrival_date = request.POST.get('arrival_date', None).replace('T', ' ')

            format = '%Y-%m-%d %H:%M'
            if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
                print("term begin > term end")
                raise Http404

            order = order_form.save(commit=False)
            order.creator = creator
            order.route = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']

            order.save()
            return redirect('dispatch:order')
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])
        
def order_edit(request):
    pk = request.POST.get('id')
    order = get_object_or_404(DispatchOrder, pk=pk)
    
    if request.method == 'POST':
        creator = get_object_or_404(User, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            post_departure_date = request.POST.get('departure_date', None).replace('T', ' ')
            post_arrival_date = request.POST.get('arrival_date', None).replace('T', ' ')

            format = '%Y-%m-%d %H:%M'
            if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
                print("term begin > term end")
                raise Http404

            order.operation_type = order_form.cleaned_data['operation_type']
            order.references = order_form.cleaned_data['references']
            order.departure = order_form.cleaned_data['departure']
            order.arrival = order_form.cleaned_data['arrival']
            order.departure_date = order_form.cleaned_data['departure_date']
            order.arrival_date = order_form.cleaned_data['arrival_date']
            order.bus_type = order_form.cleaned_data['bus_type']
            order.bus_cnt = order_form.cleaned_data['bus_cnt']
            order.price = order_form.cleaned_data['price']
            order.driver_allowance = order_form.cleaned_data['driver_allowance']
            order.contract_status = order_form.cleaned_data['contract_status']
            order.cost_type = order_form.cleaned_data['cost_type']
            order.customer = order_form.cleaned_data['customer']
            order.customer_phone = order_form.cleaned_data['customer_phone']
            order.deposit_status = order_form.cleaned_data['deposit_status']
            order.deposit_date = order_form.cleaned_data['deposit_date']
            order.bill_date = order_form.cleaned_data['bill_date']
            order.collection_type = order_form.cleaned_data['collection_type']
            
            order.payment_method = request.POST.get('payment_method', 'n')
            order.VAT = request.POST.get('VAT', 'n')
            order.route = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            order.creator = creator
            print("ORDER", order)
            order.save()

            return redirect(reverse('dispatch:order'))
        else:
            raise Http404
    else:
        raise Http404

def order_delete(request):
    if request.method == "POST":
        id_list = request.POST.getlist('id', None)
        for id in id_list:
            order = get_object_or_404(DispatchOrder, id=id)
            order.delete()

        return redirect(reverse('dispatch:order'))
    else:
        return HttpResponseNotAllowed(['post'])


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# class DispatchList(generic.ListView):
#     template_name = 'dispatch/dispatch_list.html'
#     context_object_name = 'dispatch_list'
#     model = DispatchConnect

#     def get_queryset(self):
#         twoweek = datetime.strptime(TODAY, FORMAT) + timedelta(days=14)

#         dispatch_list = DispatchConnect.objects.filter(departure_date__lte=twoweek).order_by('-departure_date')
#         print("DISPATCH_LIST", dispatch_list)
#         return dispatch_list
    
    
#     # 페이징 처리
#     #@option_year_deco
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         '''
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)
#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index
#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range
#         #페이징 끝
#         '''
#         context['date_list'] = []
#         date = None
#         for connect in context['dispatch_list']:
#             connect_date = str(connect.departure_date)[:10]
#             if date != connect_date:
#                 date = connect_date
#                 context['date_list'].append(connect_date)
            

        
        


        
#         return context

# # 날짜별-노선별 배차지시서 
# class DispatchDailyRouteList(generic.ListView):
#     template_name = 'dispatch/dispatch_daily_route.html'
#     context_object_name = 'dispatch'

#     def get_queryset(self):
#         dispatch = DispatchOrder.objects.filter(regularly=False).filter(departure_date__contains=self.kwargs['date'])
#         return dispatch

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['regularly_dispatch'] = DispatchConnect.objects.filter(date=self.kwargs['date'])
#         return context

# # 날짜별-차량별 배차지시서
# class DispatchDailyBusList(generic.ListView):
#     template_name = 'dispatch/dispatch_daily_bus.html'
#     context_object_name = 'dispatch'

#     def get_queryset(self):
#         dispatch = DispatchOrder.objects.filter(regularly=False).filter(departure_date__contains=self.kwargs['date'])
#         return dispatch

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['regularly_dispatch'] = DispatchConnect.objects.filter(date=self.kwargs['date'])
#         return context

# class OrderList(generic.ListView):
#     template_name = 'dispatch/order.html'
#     context_object_name = 'order_list'
#     model = DispatchOrder

#     def get_queryset(self):
#         dispatch_list = DispatchOrder.objects.filter(regularly=None).exclude(arrival_date__lte=TODAY).order_by('departure_date')
#         past = DispatchOrder.objects.filter(regularly=None).filter(arrival_date__lte=TODAY).order_by('-departure_date')
#         # print("order", dispatch_list, "past", past)
#         dispatch_list = dispatch_list.union(past)

#         route_name = self.request.GET.get('route_name', '')
#         start_time = self.request.GET.get('start_time', '')
#         end_time = self.request.GET.get('end_time', '')

#         print("스타트", start_time, self.request.GET.get('start_time', ''))
#         print("엔드", end_time, self.request.GET.get('end_time', ''))
#         print("그룹", route_name)
#         if route_name or start_time or end_time:
#             dispatch_list = []
#             if start_time and end_time:
#                 dispatch_list = DispatchOrder.objects.filter(departure_date__range=[start_time + " 00:00",end_time+" 24:00"])
#                 print("기간 디스패치", dispatch_list)
#             if route_name:
#                 if dispatch_list:
#                     dispatch_list = dispatch_list.filter(route_name__contains=route_name)
#                 else:
#                     dispatch_list = DispatchOrder.objects.filter(route_name__contains=route_name)
#         return dispatch_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         context['order_form'] = OrderForm()
#         context['connect_form'] = ConnectForm()
        
#         return context

# def order_create(request):
#     context = {}
    
#     if request.method == "POST":
#         creator = get_object_or_404(User, pk=request.session.get('user'))
#         order_form = OrderForm(request.POST)
#         print("POST", request.POST)
#         if order_form.is_valid():
#             post_departure_date = ' '.join(request.POST.getlist('departure_date', None))
#             post_arrival_date = ' '.join(request.POST.getlist('arrival_date', None))

#             format = '%Y-%m-%d %H:%M'
#             if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
#                 print("term begin > term end")
#                 raise Http404

#             order = order_form.save(commit=False)
#             order.creator = creator
#             order.departure_date = post_departure_date
#             order.arrival_date = post_arrival_date
            
            

#             if not request.POST.get('route_name'):
#                 print("NONNNNNNNNNN")
#                 order.route_name = order_form.cleaned_data['departure'] + ">" + order_form.cleaned_data['stopover'] + ">" + order_form.cleaned_data['arrival']

#             order.save()
#             ########## connect
#             if order.departure_date[:10] != order.arrival_date[:10]:
#                 #문자열 형식을 날짜 형식으로 변환
#                 str_date = order.departure_date[:10]
#                 date = datetime.strptime(str_date, FORMAT)
#                 end_date = datetime.strptime(order.arrival_date[:10], FORMAT) + timedelta(days=1)
#                 while str(date)[:10] != str(end_date)[:10]:
#                     print("TTTTTTTESST", str(date)[:10])

#                     if str(date)[:10] == order.departure_date[:10]:
#                         departure_date = order.departure_date
#                     else:
#                         departure_date = str(date)[:11] + "00:00"

#                     if str(date)[:10] == order.arrival_date[:10]:
#                         arrival_date = order.arrival_date
#                     else:
#                         arrival_date = str(date)[:11] + "24:00"

#                     for c in range(int(order.bus_cnt)):
#                         connect = DispatchConnect (
#                             order_id = order,
#                             departure_date = departure_date,
#                             arrival_date = arrival_date,
#                             creator = creator,
#                         )
#                         connect.save()
#                     date = date + timedelta(days=1)
#             else:
#                 connect = DispatchConnect (
#                     order_id = order,
#                     departure_date = order.departure_date,
#                     arrival_date = order.arrival_date,
#                     creator = creator,
#                 )
#                 connect.save()

#             return redirect('dispatch:order')
#         else:
#             raise Http404
#     else:
#         context = {
#             'order_list' : DispatchOrder.objects.filter(regularly=None).order_by('-pk'),
#         }
#         return render(request, 'dispatch/order_create.html', context)
        

# class OrderDetail(generic.DetailView):
#     template_name = 'dispatch/order_detail.html'
#     context_object_name = 'order'
#     model = DispatchOrder

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['order_list'] = DispatchOrder.objects.filter(regularly=None).order_by('-pk')
#         return context

# def order_edit(request, pk):
#     order = get_object_or_404(DispatchOrder, pk=pk)

#     if request.method == 'POST':
#         creator = get_object_or_404(User, pk=request.session.get('user'))
#         order_form = OrderForm(request.POST)

#         if order_form.is_valid():
#             post_departure_date = ' '.join(request.POST.getlist('departure_date', None))
#             post_arrival_date = ' '.join(request.POST.getlist('arrival_date', None))

#             format = '%Y-%m-%d %H:%M'
#             if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
#                 print("term begin > term end")
#                 raise Http404

#             order.departure = order_form.cleaned_data['departure']
#             order.arrival = order_form.cleaned_data['arrival']
#             order.stopover = order_form.cleaned_data['stopover']
#             order.route_name = order_form.cleaned_data['route_name']
#             order.price = order_form.cleaned_data['price']
#             order.driver_allowance = order_form.cleaned_data['driver_allowance']
#             order.bus_type = order_form.cleaned_data['bus_type']
#             order.bus_cnt = order_form.cleaned_data['bus_cnt']
#             order.purpose = order_form.cleaned_data['purpose']
#             order.way = order_form.cleaned_data['way']
#             order.customer = order_form.cleaned_data['customer']
#             order.customer_tel = order_form.cleaned_data['customer_tel']
#             order.reference = order_form.cleaned_data['reference']

#             order.creator = creator
#             departure_date = post_departure_date
#             arrival_date = post_arrival_date

            
#             if not request.POST.get('route_name'):
#                 order.route_name = order_form.cleaned_data['departure'] + ">" + order_form.cleaned_data['stopover'] + ">" + order_form.cleaned_data['arrival']            
            

#             if order.departure_date[:10] != departure_date[:10] or order.arrival_date[:10] != arrival_date[:10]:
                
#                 #수정 전 DispatchConnect 삭제
#                 del_list = order.info_order.all()
#                 print("DispatchConnect 삭제 후 재생성", del_list)
#                 del_list.delete()

#                 ########## connect
#                 if departure_date[:10] != arrival_date[:10]:
#                     #문자열 형식을 날짜 형식으로 변환
#                     str_date = departure_date[:10]
#                     date = datetime.strptime(str_date, FORMAT)
#                     end_date = datetime.strptime(arrival_date[:10], FORMAT) + timedelta(days=1)
#                     print("DATE", end_date)
#                     while str(date)[:10] != str(end_date)[:10]:

#                         print("TTTTTTTESST", str(date)[:10])
#                         if str(date)[:10] == departure_date[:10]:
#                             d_date = departure_date
#                         else:
#                             d_date = str(date)[:11] + "00:00"

#                         if str(date)[:10] == arrival_date[:10]:
#                             a_date = arrival_date
#                         else:
#                             a_date = str(date)[:11] + "24:00"

#                         for c in range(int(order.bus_cnt)):
#                             connect = DispatchConnect (
#                                 order_id = order,
#                                 departure_date = d_date,
#                                 arrival_date = a_date,
#                                 creator = creator,
#                             )
#                             connect.save()
#                         date = date + timedelta(days=1)
#                 else:
#                     connect = DispatchConnect (
#                         order_id = order,
#                         departure_date = departure_date,
#                         arrival_date = arrival_date,
#                         creator = creator,
#                     )
#                     connect.save()

#             order.departure_date = departure_date
#             order.arrival_date = arrival_date   
#             order.save()

#         return redirect(reverse('dispatch:order_detail', args=(pk,)))

#     else:
#         raise Http404

# def order_delete(request):
#     if request.method == "POST":
#         del_list = request.POST.getlist('delete', '')
#         for id in del_list:
#             print("aaa")
#             order = get_object_or_404(DispatchOrder, pk=id)
#             order.delete()
#         return redirect('dispatch:order_create')
#     else:
#         raise Http404

# class Management(generic.ListView):
#     template_name = 'dispatch/mgt.html'
#     context_object_name = 'connect_list'
#     model = DispatchOrder
    
#     def get_queryset(self):
#         date = self.request.GET.get('date', None)
#         group = self.request.GET.get('group', None)
#         if not date and not group:
#             queryset = DispatchConnect.objects.select_related('order_id').filter(departure_date__contains=TODAY)
#         elif date and group:
#             queryset = DispatchConnect.objects.select_related('order_id').filter(Q(departure_date__contains=date) & Q(group=group))
#             print("date and group",queryset)
#         elif date:
#             queryset = DispatchConnect.objects.select_related('order_id').filter(departure_date__contains=date)
#             print("date",queryset)
#         elif group:
#             queryset = DispatchConnect.objects.select_related('order_id').filter(group=group)
#             print("group",queryset)

#         check = ''
#         connect_list = []
#         for connect in queryset:
#             if connect.order_id.id != check:
#                 check = connect.order_id.id
#                 connect_list.append(connect)

#         return connect_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         left = []
#         width = []
#         regularly = []
#         for connect in context['connect_list']:
#             start_time = int(connect.departure_date[11:13])*60 + int(connect.departure_date[14:])
#             finish_time = int(connect.arrival_date[11:13])*60 + int(connect.arrival_date[14:])
            
#             if int(connect.departure_date[5:7]) + int(connect.departure_date[8:10]) < int(connect.arrival_date[5:7]) + int(connect.arrival_date[8:10]):
#                 wid = 1440-start_time
#             else:
#                 wid = finish_time - start_time
            

#             # 1시간에 4.5rem
#             minute = 72/1440
#             left.append(start_time*minute)
#             width.append(wid*minute)
            
#             if connect.order_id.regularly == None:
#                 regularly.append(None)
#             else:
#                 regularly.append('regularly')

#         context['left'] = left
#         context['width'] = width
#         context['regularly'] = regularly
#         context['date'] = self.request.GET.get('date', TODAY)
#         context['selected_group'] = self.request.GET.get('group', None)
#         context['group_list'] = RegularlyGroup.objects.all()
#         print(context['left'], context['connect_list'])

#         return context

# def management_create(request):
    
#     if request.method == 'POST':
#         connect = get_object_or_404(DispatchConnect, pk=request.POST.get('id'))
#         date_list = request.POST.getlist('date', None)
#         post_driver = request.POST.getlist('driver', None)
#         post_bus = request.POST.getlist('bus', None)
#         bus_cnt = connect.order_id.bus_cnt
#         print(date_list, "Aaasdasda")
#         if not date_list:
#             print("NOT")
#             return redirect('dispatch:mgt')

#         for date in date_list:
#             date_connect = connect.order_id.info_order.filter(departure_date__startswith=date)
#             #print("aadaddddddddd", date, date_connect)
#             for i in range(bus_cnt):
#                 dc = date_connect[i]

#                 if not post_driver[i]:
#                     driver = None
#                 else:
#                     driver = Member.objects.get(pk=post_driver[i])
#                 if not post_bus[i]:
#                     bus = None
#                 else:
#                     bus = Vehicle.objects.get(pk=post_bus[i])
#                 dc.driver_id = driver
#                 dc.bus_id = bus
#                 dc.save()
        
#         return redirect(reverse('dispatch:mgt_detail', args=(connect.id,)))
    


#     raise Http404

# class ManagementDetail(generic.DetailView):
#     template_name = 'dispatch/mgt_detail.html'
#     context_object_name = 'connect'
#     model = DispatchConnect

#     def get_template_names(self):
#         if get_object_or_404(DispatchConnect, pk=self.kwargs['pk']).order_id.regularly:
#             template = 'dispatch/mgt_detail_r.html'
#         else:
#             template = 'dispatch/mgt_detail.html'
#         return template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['driver_list'] = Member.objects.filter(role="기사")
#         context['bus_list'] = Vehicle.objects.all()
#         context['bus_cnt'] = context['connect'].order_id.bus_cnt
        
#         get_date = self.request.GET.get('date', None)
#         if not get_date:
#             get_date = context['connect'].departure_date[:10]

#         date_connect = DispatchConnect.objects.filter(departure_date__startswith=get_date)
#         context['schedule_list'] = []
#         bus_connect = []

#         #버스 기준으로 스케쥴 보여줄 때
#         context['kinds'] = self.request.GET.get('kinds', "bus")
#         if context['kinds'] == "bus" or context['kinds'] == None:
#             context['list'] = context['bus_list']
#         #기사 기준으로 스케쥴 보여줄 때
#         else:
#             context['list'] = context['driver_list']

#         for driver_or_bus in context['list']:
#             if context['kinds'] == "bus" or context['kinds'] == None:
#                 connect_list = date_connect.filter(bus_id=driver_or_bus)
#             else:
#                 connect_list = date_connect.filter(driver_id=driver_or_bus)

#             schedule_list = []

#             for connect in connect_list:
#                 schedule = {}

#                 start_time = int(connect.departure_date[11:13])*60 + int(connect.departure_date[14:])
#                 finish_time = int(connect.arrival_date[11:13])*60 + int(connect.arrival_date[14:])
#                 wid = finish_time - start_time

#                 # 1시간에 2rem
#                 minute = 64/1440

#                 schedule['connect'] = connect
#                 schedule['left'] = start_time*minute
#                 schedule['width'] = wid*minute
#                 if connect.order_id.regularly == None:
#                     schedule['regularly'] = False
#                 else:
#                     schedule['regularly'] = True
#                 schedule_list.append(schedule)
                
#             context['schedule_list'].append(schedule_list)
        

#         #print(context['schedule_list'])
#         #print("LIST", context['list'])
#         # 오른쪽 스케쥴표 끝
#         # 왼쪽 달력
#         ###############################
#         calendar = []
#         connect_bus = []
#         connect_driver = []

#         select_date = datetime.strptime(context['connect'].departure_date[:10], FORMAT)
#         weekday = select_date.weekday()
#         if weekday == 6: weekday = -1
#         date = select_date - timedelta(days=weekday+1)

#         for i in range(14):
#             today_connect = context['connect'].order_id.info_order.filter(departure_date__contains=str(date)[:10])
#             if today_connect:
#                 calendar.append(str(date)[:10])

#                 temp_bus = []
#                 temp_driver = []
#                 for cc in today_connect:
#                     if cc.bus_id: temp_bus.append(cc.bus_id.vehicle_num)
#                     else: temp_bus.append('')

#                     if cc.driver_id: temp_driver.append(cc.driver_id.name)
#                     else: temp_driver.append('')

#                 connect_bus.append(temp_bus)
#                 connect_driver.append(temp_driver)
#             else:
#                 calendar.append('')
#                 connect_bus.append('')
#                 connect_driver.append('')
            
#             date = date + timedelta(days=1)
        
#         #print("CALENDAR", calendar)
#         print("AAAAA", "bus", connect_bus, "driver", connect_driver)
#         context['calendar'] = calendar
#         context['connect_bus'] = connect_bus
#         context['connect_driver'] = connect_driver

#         return context

# # 스케줄표 - 버스에 등록된 기사이름, 버스번호로 리스트 만들어줌, 
# # 만약 connect의 기사가 버스에 등록된 기사랑 다를경우 다른색으로 표시해주기 - if로 클래스명 바꿔주면 될듯
# # title 태그로 마우스 hover 했을때 표시해줄 정보 정하기

# class ScheduleDetail(generic.ListView):
#     template_name = 'dispatch/schedule_detail.html'
#     context_object_name = 'connect'
#     model = DispatchOrder

#     def get_queryset(self):
#         ''' 지정한 날짜 배차지시서 보여줌 '''
#         connect = DispatchConnect.objects.filter(date=self.kwargs['date'])
#         print("CONNECT", connect)
#         return connect

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         context['schedule_list'] = []
#         #정기주문
#         context['bus_list'] = Vehicle.objects.all()
#         for bus in context['bus_list']:
#             connect_bus = context['connect'].filter(bus_id=bus)

#             schedule = {}
#             schedule['bus'] = []
#             schedule['driver'] = []
#             schedule['start_time'] = []
#             schedule['end_time'] = []
#             schedule['width'] = []
#             schedule['connect'] = []
            
#             for connect in connect_bus:
#                 order = connect.order_id
#                 start_time = int(order.departure_date[11:13])*60 + int(order.departure_date[14:])
#                 end_time = int(order.arrival_date[11:13])*60 + int(order.arrival_date[14:])

#                 schedule['connect'].append(connect)
#                 schedule['bus'].append(connect.bus_id.vehicle_num)
#                 schedule['driver'].append(connect.driver_id.name)
#                 schedule['start_time'].append(start_time)
#                 schedule['end_time'].append(end_time)
#                 if end_time > start_time:
#                     schedule['width'].append(end_time-start_time)
#                 else:
#                     schedule['width'].append(start_time-end_time)

#             context['schedule_list'].append(schedule)
#         print(context['schedule_list'])
#         return context

# '''
# ##############
#         for connect in context['connect']:
#             order = connect.order_id
#             start_time = int(order.departure_date[11:13])*60 + int(order.departure_date[14:])
#             end_time = int(order.arrival_date[11:13])*60 + int(order.arrival_date[14:])

#             schedule['bus'].append(connect.bus_id.vehicle_num)
#             schedule['driver'].append(connect.driver_id.name)
#             schedule['start_time'].append(start_time)
#             schedule['end_time'].append(end_time)
#             if end_time > start_time:
#                 schedule['width'].append(end_time-start_time)
#             else:
#                 schedule['width'].append(start_time-end_time)

#         context['schedule'] = schedule
#         print(context['schedule'])
#         return context
# '''

# #######

# class RegularlyOrderList(generic.ListView):
#     template_name = 'dispatch/regularly_order_list.html'
#     context_object_name = 'order_list'
#     model = DispatchOrder

#     def get_queryset(self):
#         dispatch_list = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')


#         group_name = self.request.GET.get('group_name', '')
#         start_time = self.request.GET.get('start_time', '')
#         end_time = self.request.GET.get('end_time', '')

#         print("스타트", start_time, self.request.GET.get('start_time', ''))
#         print("엔드", end_time, self.request.GET.get('end_time', ''))
#         print("그룹", group_name)
#         if group_name or start_time or end_time:
#             dispatch_list = []
#             if start_time and end_time:
#                 dispatch_list = DispatchOrder.objects.filter(departure_date__range=[start_time,end_time])
#                 print("기간 디스패치", dispatch_list)
#             if group_name:
#                 if dispatch_list:
#                     temp = []
#                     for dispatch in dispatch_list:
#                         if dispatch.regularly.regularly_group.name == group_name:
#                             temp.append(dispatch)
#                     dispatch_list = temp
#                 else:
#                     try:
#                         for regularly in RegularlyGroup.objects.get(name__contains=group_name).regularly_info.all():
#                             dispatch_list.append(regularly.order_info.all()[0])
#                     except Exception as e:
#                         print("ERROR", e)
#         return dispatch_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         '''
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)
#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index
#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range
#         '''
#         #페이징 끝

#         group_name = self.request.GET.get('group_name', '')
#         start_time = self.request.GET.get('start_time', '')
#         end_time = self.request.GET.get('end_time', '')

#         context['group_list'] = RegularlyGroup.objects.all()
#         context['group_name'] = group_name
#         context['start_time'] = start_time
#         context['end_time'] = end_time
#         return context

# class RegularlyOrderDetail(generic.DetailView):
#     template_name = 'dispatch/regularly_order_detail.html'
#     context_object_name = 'order_detail'
#     model = DispatchOrder

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['order_list'] = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')
#         context['group_list'] = RegularlyGroup.objects.all()
#         return context
    

# def regularly_order_create(request):
#     context = {}
#     if request.method == "POST":
#         creator = get_object_or_404(User, pk=request.session.get('user'))
#         order_form = OrderForm(request.POST)
#         print("RRRR", request.POST)

#         if order_form.is_valid():
#             print("VALID")
#             if datetime.strptime(request.POST.get('term_begin'), FORMAT) > datetime.strptime(request.POST.get('term_end'), FORMAT):
#                 print("출발일이 도착일보다 늦습니다")
#                 context = {}
#                 context['order_list'] = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')
#                 context['group_list'] = RegularlyGroup.objects.all()
#                 context['error'] = "출발일이 도착일보다 늦습니다"
#                 #raise BadRequest('출발일이 도착일보다 늦습니다.')
#                 #return render(request, 'dispatch/regularly_order_create.html', context)
#                 raise Http404
#             post_group = request.POST.get('regularly_group', None)
#             try:
#                 regularly_group = RegularlyGroup.objects.get(pk=post_group)
#             except Exception as e:
#                 regularly_group = None

#             week = ''.join(request.POST.getlist('week', None))
#             regularly = RegularlyOrder(
#                 week=week,
#                 term_begin=request.POST.get('term_begin', None),
#                 term_end=request.POST.get('term_end', None),
#                 regularly_group=regularly_group,
#             )
#             regularly.save()

#             order = order_form.save(commit=False)
#             order.creator = creator
#             order.regularly = regularly
            
#             if request.POST.get('route_name') == '':
#                 print("NONNNNNNNNNN")
#                 order.route_name = order_form.cleaned_data['departure'] + ">" + order_form.cleaned_data['stopover'] + ">" + order_form.cleaned_data['arrival']
#             order.save()

#             # 기간만큼 for 돌면서 설정한 요일에 맞게 dispatchConnect생성 해줌
#             ########## connect
#             # 정기주문 departure_date는 시간만 받아서 term으로 while 돌리면서 넣어줘야됨
#             str_week = week
#             week = weekday_to_numlist(str_week)
            
#             print("요일", week)
#             if regularly.term_begin[:10] != regularly.term_end[:10]:
#                 #문자열 형식을 날짜 형식으로 변환
#                 begin_date = regularly.term_begin[:10]
#                 # term_end + 1일, while문 탈출용
#                 date = datetime.strptime(begin_date, FORMAT)
#                 end_date = str(datetime.strptime(regularly.term_end, FORMAT) + timedelta(days=1))
                
#                 print("DATE", str(date)[:10], end_date[:10])
#                 while str(date)[:10] != end_date[:10]:

#                     weekday = date.weekday()
#                     flag = False
#                     for wd in week:
#                         if weekday == wd:
#                             flag = True
#                     if flag == True:
#                         #print("TTTTTTTESST", str(date)[:10])
#                         #요일이 맞으면
#                         departure_date = str(date)[:10] + " " + order.departure_date                    

#                         arrival_date = str(date)[:10] + " " + order.arrival_date
#                         for j in range(int(order.bus_cnt)):
#                             connect = DispatchConnect (
#                                 order_id = order,
#                                 departure_date = departure_date,
#                                 arrival_date = arrival_date,
#                                 creator = creator,
#                             )
#                             connect.save()
#                     date = date + timedelta(days=1)
#             else:
#                 connect = DispatchConnect (
#                     order_id = order,
#                     departure_date = regularly.term_begin,
#                     arrival_date = regularly.term_end,
#                     creator = creator,
#                 )
#                 connect.save()

#             return redirect('dispatch:regularly_order_create')
#     else:
#         # print("스타트", request.GET.get('start_name', '')) name 똑바로 안보냐 븅신아
#         # print("엔드", request.GET.get('end_time', ''))
#         # print("그룹", request.GET.get('group', ''))
#         #raise BadRequest('asdffd')
#         context = {
#             'order_list' : DispatchOrder.objects.exclude(regularly=None).order_by('-pk'),
#             'group_list' : RegularlyGroup.objects.all()
#         }
#         group_name = request.GET.get('group_name', '')
#         start_time = request.GET.get('start_time', '')
#         end_time = request.GET.get('end_time', '')

#         print("스타트", start_time, request.GET.get('start_time', ''))
#         print("엔드", end_time, request.GET.get('end_time', ''))
#         print("그룹", group_name)
#         if group_name or start_time or end_time:
#             dispatch_list = []
#             if start_time and end_time:
#                 dispatch_list = DispatchOrder.objects.filter(departure_date__range=[start_time,end_time])
#                 print("기간 디스패치", dispatch_list)
#             if group_name:
#                 if dispatch_list:
#                     print("있잖아", dispatch_list)
#                     temp = []
#                     for dispatch in dispatch_list:
#                         if dispatch.regularly.regularly_group.name == group_name:
#                             temp.append(dispatch)
#                     dispatch_list = temp
#                 else:
#                     print("ㅁㄴㄹㅇㅁㄴㅇㄻㄻㄹㅇ")
#                     try:
#                         for regularly in RegularlyGroup.objects.get(name__contains=group_name).regularly_info.all():
#                             dispatch_list.append(regularly.order_info.all()[0])
#                     except Exception as e:
#                         print("ERROR", e)
#             context['order_list'] = dispatch_list
#             context['group_name'] = group_name
#             context['start_time'] = start_time
#             context['end_time'] = end_time
#     return render(request, 'dispatch/regularly_order_create.html', context)


# ###########################################

# def regularly_order_edit(request, pk):
#     order = get_object_or_404(DispatchOrder, pk=pk)
#     regularly = order.regularly

#     if request.method == 'POST':
#         creator = get_object_or_404(User, pk=request.session.get('user'))
        
#         order_form = OrderForm(request.POST)
#         if order_form.is_valid():
#             print("VALID")
#             if datetime.strptime(request.POST.get('term_begin'), FORMAT) > datetime.strptime(request.POST.get('term_end'), FORMAT):
#                 print("출발일이 도착일보다 늦습니다")
#                 context = {}
#                 context['order_detail'] = get_object_or_404(DispatchOrder, pk=pk)
#                 context['order_list'] = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')
#                 context['group_list'] = RegularlyGroup.objects.all()
#                 context['error'] = "출발일이 도착일보다 늦습니다"
#                 #raise BadRequest('출발일이 도착일보다 늦습니다.')
#                 #return render(request, 'dispatch/regularly_order_detail.html', context)
#                 raise Http404
#             route_name = order_form.cleaned_data['departure'] + ">" + order_form.cleaned_data['stopover'] + ">" + order_form.cleaned_data['arrival']
#             if order_form.cleaned_data['route_name'] == '' or route_name == order_form.cleaned_data['route_name']:
#                 order.route_name = route_name
#             else:
#                 order.route_name = route_name

#             before_bus_cnt = order.bus_cnt

#             order.departure = order_form.cleaned_data['departure']
#             order.arrival = order_form.cleaned_data['arrival']
#             order.departure_date = order_form.cleaned_data['departure_date']
#             order.arrival_date = order_form.cleaned_data['arrival_date']
#             order.stopover = order_form.cleaned_data['stopover']
#             order.price = order_form.cleaned_data['price']
#             order.driver_allowance = order_form.cleaned_data['driver_allowance']
#             order.bus_type = order_form.cleaned_data['bus_type']
#             order.bus_cnt = order_form.cleaned_data['bus_cnt']
#             order.purpose = order_form.cleaned_data['purpose']
#             order.way = order_form.cleaned_data['way']
#             order.customer = order_form.cleaned_data['customer']
#             order.customer_tel = order_form.cleaned_data['customer_tel']
#             order.reference = order_form.cleaned_data['reference']
#             order.creator = creator

#             #원래 값 변수에 저장
#             before_begin = regularly.term_begin
#             before_end = regularly.term_end
#             before_week = regularly.week
            

#             term_begin = request.POST.get('term_begin', None)
#             term_end = request.POST.get('term_end', None)

#             week = ''.join(request.POST.getlist('week', None))
#             regularly.week =  week
#             regularly.term_begin = term_begin
#             regularly.term_end = term_end
            
#             print(request.POST.get('regularly_group', None))
#             try:
#                 regularly_group = RegularlyGroup.objects.get(pk=request.POST.get('regularly_group', None))
#             except Exception as e:
#                 print("EXCEPT", e)
#                 regularly_group = None
#             regularly.regularly_group = regularly_group
            
#             order.save()
#             regularly.save()

#             ##############
#             print("BUSCNT", before_bus_cnt, order.bus_cnt)
#             #수정 시 DispatchConnect 삭제 후 다시 생성 짜야됨
#             if before_week != week or before_begin != term_begin or before_end != term_end or before_bus_cnt != order.bus_cnt:
#                 # 오늘기준부터 term_end 까지 원래 있던 DispatchConnect 삭제 후 재생성
#                 end_date = datetime.strptime(term_end, FORMAT) + timedelta(days=1)

#                 del_list = order.info_order.filter(departure_date__range=(TODAY, end_date))
#                 print("삭제 DispatchConnect 리스트", del_list)
#                 del_list.delete()

#                 ########## connect
#                 str_week = week
#                 week = weekday_to_numlist(str_week)
#                 print("요일", week)
                
#                 #문자열 형식을 날짜 형식으로 변환
#                 # TODAY부터 end_date까지 새로 DispatchConnect 만들어줌
#                 date = datetime.strptime(TODAY, FORMAT)
#                 # term_end + 1일, while문 탈출용
#                 end_date = str(datetime.strptime(regularly.term_end, FORMAT) + timedelta(days=1))
                
#                 while str(date)[:10] != end_date[:10]:
#                     weekday = date.weekday()
#                     flag = False
#                     for wd in week:
#                         if weekday == wd:
#                             flag = True
#                     if flag == True:
#                         print("TTTTTTTESST", str(date)[:10])
#                         #요일이 맞으면
#                         departure_date = str(date)[:10] + " " + order.departure_date                    

#                         arrival_date = str(date)[:10] + " " + order.arrival_date

#                         for j in range(int(order.bus_cnt)):
#                             connect = DispatchConnect (
#                                 order_id = order,
#                                 departure_date = departure_date,
#                                 arrival_date = arrival_date,
#                                 creator = creator,
#                             )
#                             connect.save()
#                     date = date + timedelta(days=1)

#             return redirect('dispatch:regularly_order_create')
#         else:
#             print("not valid")
#             return Http404
#     else:
#         raise Http404

# def regularly_order_delete(request):
#     if request.method == "POST":
#         order_list = request.POST.getlist("order_check")
#         for order_id in order_list:        
#             order = get_object_or_404(DispatchOrder, pk=order_id)
#             if order.creator.pk == request.session['user'] or User.objects.get(pk=request.session['user']).authority == "관리자": # ?? 작성자만 지울 수 있게 하나?
#                 order.regularly.delete()
#                 order.delete()
#         return redirect(reverse('dispatch:regularly_order_create'))
#     else:
#         raise Http404

# class RegularlyOrderGroup(generic.ListView):
#     template_name = 'dispatch/regularly_order_group.html'
#     context_object_name = 'group_list'
#     model = RegularlyGroup


#     # 그룹생성
#     def post(self, request, *args, **kwargs):
#         """
#         그룹 추가하는 인풋 하나 따로 만들어서 그룹 추가해서 셀렉트 박스에 보여주기
#         """
#         group = RegularlyGroup(
#             name = request.POST.get('name'),
#             company = request.POST.get('company'),
#             creator = get_object_or_404(User, pk=self.request.session['user'])
#         )
#         group.save()
        
#         return redirect('dispatch:regularly_order_group')

# def regularly_group_create(request):

#     if request.method == "POST":
#         """
#         그룹 추가하는 인풋 하나 따로 만들어서 그룹 추가해서 셀렉트 박스에 보여주기
#         """
#         group = RegularlyGroup(
#             name = request.POST.get('name'),
#             company = request.POST.get('company'),
#             creator = get_object_or_404(User, pk=request.session['user'])
#         )
#         group.save()
#         return redirect('dispatch:regularly_order_group')
#     else:
#         raise Http404

# def regularly_group_delete(request):
    
#     if request.method == "POST":
#         group_list = request.POST.getlist('group')

#         for g in group_list:
#             get_object_or_404(RegularlyGroup, pk=g).delete()

#         return redirect('dispatch:regularly_order_group')
#     raise Http404
    
# class RegularlyOrderGroupDetail(generic.ListView):
#     template_name = 'dispatch/regularly_order_group_detail.html'
#     context_object_name = 'routes'
#     model = DispatchOrder

#     def get_queryset(self):
#         dispatch_list = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')

#         group_name = self.request.GET.get('group_name', '')
#         start_time = self.request.GET.get('start_time', '')
#         end_time = self.request.GET.get('end_time', '')

#         print("스타트", start_time, self.request.GET.get('start_time', ''))
#         print("엔드", end_time, self.request.GET.get('end_time', ''))
#         print("그룹", group_name)
#         if group_name or start_time or end_time:
#             dispatch_list = []
#             if start_time and end_time:
#                 dispatch_list = DispatchOrder.objects.filter(departure_date__range=[start_time,end_time])
#                 print("기간 디스패치", dispatch_list)
#             if group_name:
#                 if dispatch_list:
#                     temp = []
#                     for dispatch in dispatch_list:
#                         if dispatch.regularly.regularly_group.name == group_name:
#                             temp.append(dispatch)
#                     dispatch_list = temp
#                 else:
#                     try:
#                         for regularly in RegularlyGroup.objects.get(name__contains=group_name).regularly_info.all():
#                             dispatch_list.append(regularly.order_info.all()[0])
#                     except Exception as e:
#                         print("ERROR", e)
#         return dispatch_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['group_list'] = RegularlyGroup.objects.all()
#         context['group'] = get_object_or_404(RegularlyGroup, pk=self.kwargs['pk'])
#         context['group_order_list'] = RegularlyOrder.objects.filter(regularly_group=context['group'])
#         context['order_list'] = DispatchOrder.objects.exclude(regularly=None)

#         group_name = self.request.GET.get('group_name', '')
#         start_time = self.request.GET.get('start_time', '')
#         end_time = self.request.GET.get('end_time', '')
#         context['group_name'] = group_name
#         context['start_time'] = start_time
#         context['end_time'] = end_time
#         return context

#     #그룹정보 수정
#     def post(self, request, *args, **kwargs):
#         """
#         그룹 추가하는 인풋 하나 따로 만들어서 그룹 추가해서 셀렉트 박스에 보여주기
#         """
#         group = get_object_or_404(RegularlyGroup, pk=kwargs['pk'])
        
#         group.name = request.POST.get('name', None)
#         group.company = request.POST.get('company', None)
#         group.creator = get_object_or_404(User, pk=self.request.session['user'])        
#         group.save()

#         return redirect('dispatch:regularly_order_group')


        

# def regularly_order_group_create(request, pk):
#         """
#         셀렉트 박스로 그룹 선택해서 그룹에 추가, 
#         만약 그룹을 새로 만드려면 맨밑에 그룹추가 선택하면 그룹이름이랑 업체명 인풋 생김
#         """
#         if request.method == "POST":
#             routes = request.POST.getlist('route')
            
#             group = get_object_or_404(RegularlyGroup, pk=request.POST.get('group'))
#             print("aaaaaaaaaaaaaaaa", routes, group)
#             for i in routes:
#                 route = get_object_or_404(DispatchOrder, pk=i)
#                 route.regularly.regularly_group = group
#                 route.regularly.save()
#             return redirect(reverse('dispatch:regularly_order_group_detail', args=(pk,)))
#         else:
#             raise Http404
# #############

    

# def regularly_order_group_delete(request, pk):

#     if request.method == "POST":
#         order_list = request.POST.getlist('order_list')
#         for g in order_list:
#             order = get_object_or_404(RegularlyOrder, pk=g)
#             order.regularly_group = None
#             order.save()

#         return redirect(reverse('dispatch:regularly_order_group_detail', args=(pk,)))
#     raise Http404

# # ex) week = '월화'
# def weekday_to_numlist(week):
#     list_week = list(week)
#     result = []
#     for w in list_week:
#         if w == "월":
#             result.append(0)
#         elif w == "화":
#             result.append(1)
#         elif w == "수":
#             result.append(2)
#         elif w == "목":
#             result.append(3)
#         elif w == "금":
#             result.append(4)
#         elif w == "토":
#             result.append(5)
#         elif w == "일":
#             result.append(6)
#     return result