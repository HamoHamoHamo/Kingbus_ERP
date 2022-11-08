import json
import pandas as pd
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import OrderForm, ConnectForm, RegularlyForm
from .models import DispatchCheck, DispatchOrderConnect, DispatchOrder, DispatchRegularly, RegularlyGroup, DispatchRegularlyConnect, DispatchOrderWaypoint
from accounting.models import Salary
from humanresource.models import Member
from itertools import chain
from vehicle.models import Vehicle

from datetime import datetime, timedelta, date
# from utill.decorator import option_year_deco



TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"
WEEK = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)', ]
WEEK2 = ['월', '화', '수', '목', '금', '토', '일', ]

class RegularlyPrintList(generic.ListView):
    template_name = 'dispatch/regularly_print.html'
    context_object_name = 'order_list'
    model = DispatchRegularly

    def get_queryset(self):
        
        date = self.request.GET.get('date', TODAY)
        group_id = self.request.GET.get('group', '')

        weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        

        group = RegularlyGroup.objects.get(id=group_id)
        dispatch_list = group.regularly_info.filter(week__contains=weekday).order_by('number1', 'number2')

        return dispatch_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)
        group_bus_list = []
        group_driver_list = []
        group_outsourcing_list = []
        departure_time_list = []
        arrival_time_list = []
        for order in context['order_list']:
            connect = order.info_regularly.filter(departure_date__contains=date)
            if connect:
                connect = connect[0]
                c_bus = connect.bus_id
                c_outsourcing = ''
                c_driver = ''
                if connect.outsourcing == 'y':
                    c_outsourcing = connect.driver_id
                else:
                    c_driver = connect.driver_id
                
                departure_time_list.append(connect.departure_date[11:])
                arrival_time_list.append(connect.arrival_date[11:])
                group_bus_list.append(c_bus)
                group_driver_list.append(c_driver)
                group_outsourcing_list.append(c_outsourcing)
            else:
                departure_time_list.append('')
                arrival_time_list.append('')
                group_bus_list.append('')
                group_driver_list.append('')
                group_outsourcing_list.append('')
        
        context['departure_time_list'] = departure_time_list
        context['arrival_time_list'] = arrival_time_list
        context['group_bus_list'] = group_bus_list
        context['group_driver_list'] = group_driver_list
        context['group_outsourcing_list'] = group_outsourcing_list
        return context


def order_print(request):
    
    date1 = request.GET.get('date1', TODAY)
    date2 = request.GET.get('date2', TODAY)
    order_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{date1} 00:00').exclude(departure_date__gt=f'{date2} 24:00').order_by('departure_date')
    
    context = {
        'date1': date1,
        'date2': date2,
        'order_list': order_list,
    }
    return render(request, 'dispatch/order_print.html', context)

def calendar_create(request):
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        date = request.POST.get('date', None)
        try:
            check = get_object_or_404(DispatchCheck, date=date)
            if check.member_id1:
                check.member_id2 = creator
                check.dispatch_check = 'y'
            else:
                check.member_id1 = creator
                check.dispatch_check = 'n'
                
        except:
            check = DispatchCheck(
                member_id1 = creator,
                date = date,
                dispatch_check = 'n',
                creator = creator,
            )
        check.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def calendar_delete_1(request):
    if request.method == "POST":
        date = request.POST.get('date', None)
        check = get_object_or_404(DispatchCheck, date=date)
        check.member_id1 = check.member_id2
        check.member_id2 = None
        check.dispatch_check = 'n'
        check.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def calendar_delete_2(request):
    if request.method == "POST":
        date = request.POST.get('date', None)
        check = get_object_or_404(DispatchCheck, date=date)
        check.member_id2 = None
        check.dispatch_check = 'n'
        check.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


class ScheduleList(generic.ListView):
    template_name = 'dispatch/schedule.html'
    context_object_name = 'vehicle_list'
    model = Vehicle

    def get_queryset(self):
        select = self.request.GET.get('select', None)
        search_d = self.request.GET.get('search_d', None)
        search_v = self.request.GET.get('search_v', None)

        if select == 'driver':
            vehicle_list = Vehicle.objects.prefetch_related('info_bus_id', 'info_regulary_bus_id').filter(driver_name__contains=search_d).filter(use='y')
        elif select == 'vehicle':
            vehicle_list = Vehicle.objects.prefetch_related('info_bus_id', 'info_regulary_bus_id').filter(vehicle_num__contains=search_v).filter(use='y')
        else:
            vehicle_list = Vehicle.objects.prefetch_related('info_bus_id', 'info_regulary_bus_id').filter(use='y')
        return vehicle_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', TODAY)

        schedule_list = []

        for vehicle in context['vehicle_list']:
            temp = []
            order_list = vehicle.info_bus_id.exclude(arrival_date__lte=f'{date} 00:00').exclude(departure_date__gte=f'{date} 24:00')
            e_regulary_list = vehicle.info_regulary_bus_id.exclude(arrival_date__lte=f'{date} 00:00').exclude(departure_date__gte=f'{date} 24:00').filter(work_type='출근')
            l_regulary_list = vehicle.info_regulary_bus_id.exclude(arrival_date__lte=f'{date} 00:00').exclude(departure_date__gte=f'{date} 24:00').filter(work_type='퇴근')
            for o in order_list:
                temp.append({
                    'work_type': '일반',
                    'departure_date': o.departure_date,
                    'arrival_date': o.arrival_date,
                    'departure': o.order_id.departure,
                    'arrival': o.order_id.arrival,
                })
            for o in e_regulary_list:
                temp.append({
                    'work_type': '출근',
                    'departure_date': o.departure_date,
                    'arrival_date': o.arrival_date,
                    'departure': o.regularly_id.departure,
                    'arrival': o.regularly_id.arrival,
                })
            for o in l_regulary_list:
                temp.append({
                    'work_type': '퇴근',
                    'departure_date': o.departure_date,
                    'arrival_date': o.arrival_date,
                    'departure': o.regularly_id.departure,
                    'arrival': o.regularly_id.arrival,
                })

            schedule_list.append(temp)
        print(schedule_list)
        context['schedule_list'] = schedule_list

        context['datalist_vehicle'] = Vehicle.objects.filter(use='y')
        context['datalist_driver'] = Member.objects.filter(role='운전원')
        
        context['select'] = self.request.GET.get('select', '')
        context['search_d'] = self.request.GET.get('search_d', '')
        context['search_v'] = self.request.GET.get('search_v', '')
        context['date'] = date
        return context


class DocumentList(generic.ListView):
    template_name = 'dispatch/document.html'
    context_object_name = 'order_list'
    model = DispatchOrder

    def get_queryset(self):
        date = self.request.GET.get('date', TODAY)
        order_list = DispatchOrder.objects.prefetch_related('info_order').filter(departure_date__lte=f'{date}T24:00').filter(arrival_date__gte=f'{date}T00:00')
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

        connect_list = []
        for order in context['order_list']:
            connect_list.append(order.info_order.all())
        print("CONNETCTT", connect_list)
        context['connect_list'] = connect_list
        context['departure_date'] = departure_date
        context['num_days'] = num_days
        context['time'] = time
        context['date'] = self.request.GET.get('date', TODAY)
        
        return context
    
class RegularlyDispatchList(generic.ListView):
    template_name = 'dispatch/regularly.html'
    context_object_name = 'order_list'
    model = DispatchRegularly

    def get_queryset(self):
        
        date = self.request.GET.get('date', TODAY)
        group_id = self.request.GET.get('group', '')

        weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        
        if group_id:
            group = RegularlyGroup.objects.get(id=group_id)
            dispatch_list = group.regularly_info.filter(week__contains=weekday).order_by('num1', 'num2')
        else:
            dispatch_list = DispatchRegularly.objects.filter(week__contains=weekday).order_by('group', 'num1', 'num2')
        return dispatch_list


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date = self.request.GET.get('date', TODAY)
        selected_group = self.request.GET.get('group', '')
        detail_id = self.request.GET.get('id')
        if detail_id:
            context['detail'] = get_object_or_404(DispatchRegularly, id=detail_id)

            # 지난 배차내역 불러오기
            date_type = datetime.strptime(date, FORMAT)
            start_date = date_type - timedelta(days=int(date_type.weekday()) + 7)
            str_end_date = datetime.strftime(start_date + timedelta(days=13), FORMAT)

            str_start_date = datetime.strftime(start_date, FORMAT)
            

            dispatch_history = context['detail'].info_regularly.filter(departure_date__range=(str_start_date, str_end_date))

            history_list = []
            date_list = []
            block_list = []

            departure_date = f'{date} {context["detail"].departure_time}'
            arrival_date = f'{date} {context["detail"].arrival_time}'

            for i in range(14):
                
                list_date = datetime.strftime(start_date + timedelta(days=i), FORMAT)
                date_list.append(f'{list_date} {WEEK[datetime.strptime(list_date, FORMAT).weekday()]}')
                
                try:
                    connect_history = context['detail'].info_regularly.get(departure_date__startswith=list_date)
                    history_list.append(connect_history)

                    h_driver = connect_history.driver_id
                    h_bus = connect_history.bus_id

                    


                    if DispatchRegularlyConnect.objects.filter(driver_id=h_driver).exclude(departure_date__gt=arrival_date).exclude(arrival_date__lt=departure_date).exists():
                        block_list.append('y')
                    elif DispatchRegularlyConnect.objects.filter(bus_id=h_bus).exclude(departure_date__gt=arrival_date).exclude(arrival_date__lt=departure_date).exists():
                        block_list.append('y')
                    else:
                        block_list.append('')



                except DispatchRegularlyConnect.DoesNotExist:
                    history_list.append('')
                    block_list.append('')
                    continue

            context['history_list'] = history_list
            context['date_list'] = date_list
            context['block_list'] = block_list
            print('block_listsssssss', context['block_list'])

        if selected_group:
            context['group'] = get_object_or_404(RegularlyGroup, id=selected_group)
        context['date'] = date

        driver_list = Member.objects.filter(role='운전원').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]
        outsourcing_list = Member.objects.filter(role='용역').values_list('id', 'name')
        context['outsourcing_dict'] = {}
        for outsourcing in outsourcing_list:
            context['outsourcing_dict'][outsourcing[0]] = outsourcing[1]

        r_connect_list = DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        dispatch_list = []
        for rc in r_connect_list:
            dispatch = rc.regularly_id
            data = {
                'work_type': dispatch.work_type,
                'departure_date': rc.departure_date,
                'arrival_date': rc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': rc.week,
                'bus_id': rc.bus_id.id,
                'bus_num': rc.bus_id.vehicle_num,
                'driver_id': rc.driver_id.id,
                'driver_name': rc.driver_id.name,
                'outsourcing': rc.outsourcing,
            }
            dispatch_list.append(data)
        connect_list = DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        for cc in connect_list:
            dispatch = cc.order_id
            data = {
                'work_type': '일반',
                'departure_date': cc.departure_date,
                'arrival_date': cc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': cc.week,
                'bus_id': cc.bus_id.id,
                'bus_num': cc.bus_id.vehicle_num,
                'driver_id': cc.driver_id.id,
                'driver_name': cc.driver_id.name,
                'outsourcing': cc.outsourcing,
            }
            dispatch_list.append(data)

        context['dispatch_list'] = dispatch_list
        #

        context['vehicles'] = Vehicle.objects.filter(use='y').order_by('vehicle_num', 'driver_name')
        context['group_list'] = RegularlyGroup.objects.all().order_by('number')
        
        #
        group_bus_list = []
        group_driver_list = []
        group_outsourcing_list = []
        departure_time_list = []
        arrival_time_list = []
        for order in context['order_list']:
            connect = order.info_regularly.filter(departure_date__contains=date)
            if connect:
                connect = connect[0]
                c_bus = connect.bus_id
                c_outsourcing = ''
                c_driver = ''
                if connect.outsourcing == 'y':
                    c_outsourcing = connect.driver_id
                else:
                    c_driver = connect.driver_id
                
                departure_time_list.append(connect.departure_date[11:])
                arrival_time_list.append(connect.arrival_date[11:])
                group_bus_list.append(c_bus)
                group_driver_list.append(c_driver)
                group_outsourcing_list.append(c_outsourcing)
            else:
                departure_time_list.append('')
                arrival_time_list.append('')
                group_bus_list.append('')
                group_driver_list.append('')
                group_outsourcing_list.append('')
        
        context['departure_time_list'] = departure_time_list
        context['arrival_time_list'] = arrival_time_list
        context['group_bus_list'] = group_bus_list
        context['group_driver_list'] = group_driver_list
        context['group_outsourcing_list'] = group_outsourcing_list
        return context


def regularly_connect_create(request):
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        order = get_object_or_404(DispatchRegularly, id=request.POST.get('id', None))
        bus = request.POST.get('bus')
        outsourcing_id = request.POST.get('outsourcing')
        driver_id = request.POST.get('driver')
        
        if outsourcing_id:
            outsourcing = 'y'
            driver = get_object_or_404(Member, id=outsourcing_id)
        else:
            outsourcing = 'n'
            driver = get_object_or_404(Member, id=driver_id)
            
        date = request.POST.get('date', None)
        vehicle = get_object_or_404(Vehicle, id=bus)

        old_connect = order.info_regularly.filter(departure_date__startswith=date)
        old_connect.delete()

        r_connect = DispatchRegularlyConnect(
            regularly_id = order,
            bus_id = vehicle,
            driver_id = driver,
            departure_date = f'{date} {order.departure_time}',
            arrival_date = f'{date} {order.arrival_time}',
            work_type = order.work_type,
            driver_allowance = order.driver_allowance,
            outsourcing = outsourcing,
            creator = creator
        )
        r_connect.save()
        group = request.POST.get('group')
        date = request.POST.get('date')
        return redirect(reverse('dispatch:regularly') + f'?group={group}&date={date}')
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_connect_load(request, week):
    if week != 1 and week != 2:
        raise Http404
    creator = get_object_or_404(Member, id=request.session.get('user'))
    check_list = request.POST.getlist('check', '')
    if not check_list:
        return JsonResponse({'status': 'check'})
    req_date = request.POST.get('date', TODAY)

    minus_week = 7 if week == 1 else 14
    date = datetime.strftime(datetime.strptime(req_date, FORMAT) - timedelta(days=minus_week), FORMAT)

    bus_list = []
    driver_list = []
    outsourcing_list = []
    regularly_list = []
    for check in check_list:
        regularly = DispatchRegularly.objects.get(id=check)
        cur_connect = DispatchRegularlyConnect.objects.select_related('regularly_id', 'bus_id', 'driver_id').filter(regularly_id=regularly).filter(departure_date__startswith=req_date)
        if cur_connect.exists():
            cur_connect_id = cur_connect[0].id
        else:
            # 체크된 노선의 선택된 날짜에 배차가 없을 경우
            cur_connect_id = 0
        try:
            connect = DispatchRegularlyConnect.objects.select_related('regularly_id', 'bus_id', 'driver_id').filter(regularly_id=regularly).get(departure_date__startswith=date)
            bus = connect.bus_id
            driver = connect.driver_id
            outsourcing = connect.outsourcing
            
            order_arrival_time = f'{req_date} {regularly.arrival_time}'
            order_departure_time = f'{req_date} {regularly.departure_time}'
            ##################### 노선 정보가 수정됐을때는?
            if DispatchRegularlyConnect.objects.exclude(id=cur_connect_id).filter(driver_id=driver).exclude(departure_date__gt=order_arrival_time).exclude(arrival_date__lt=order_departure_time).exists():
                return JsonResponse({'status': 'overlap', 'route': f'{regularly.number1}-{regularly.number2} {regularly.route}'})

            if DispatchRegularlyConnect.objects.exclude(id=cur_connect_id).filter(bus_id=bus).exclude(departure_date__gt=order_arrival_time).exclude(arrival_date__lt=order_departure_time).exists():
                return JsonResponse({'status': 'overlap', 'route': f'{regularly.number1}-{regularly.number2} {regularly.route}'})
            bus_list.append(bus)
            driver_list.append(driver)
            outsourcing_list.append(outsourcing)
            regularly_list.append(regularly)

        except DispatchRegularlyConnect.DoesNotExist:
            print('does not exists')
            bus_list.append('')
            driver_list.append('')
            regularly_list.append(regularly)
            continue
        except MultipleObjectsReturned:
            raise Http404

    
    for i in range(len(check_list)):
        DispatchRegularlyConnect.objects.filter(regularly_id=regularly_list[i]).filter(departure_date__startswith=req_date).delete()

        if bus_list[i]:
            connect = DispatchRegularlyConnect(
                regularly_id = regularly_list[i],
                bus_id = bus_list[i],
                driver_id = driver_list[i],
                outsourcing = outsourcing_list[i],
                departure_date = f'{req_date} {regularly_list[i].departure_time}',
                arrival_date = f'{req_date} {regularly_list[i].arrival_time}',
                work_type = regularly_list[i].work_type,
                driver_allowance = regularly_list[i].driver_allowance,
                creator = creator
            )
            connect.save()


    return JsonResponse({'status': 'success'})



def regularly_connect_delete(request):
    if request.method == "POST":
        check_list = request.POST.getlist('check')
        date = request.POST.get('date')

        for order_id in check_list:
            order = DispatchRegularly.objects.prefetch_related('info_regularly').get(id=order_id)
            connect = order.info_regularly.get(departure_date__startswith=date)
            connect.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


class RegularlyRouteList(generic.ListView):
    template_name = 'dispatch/regularly_route.html'
    context_object_name = 'order_list'
    # paginate_by = 10
    model = DispatchRegularly

    def get_queryset(self):
        group_id = self.request.GET.get('group', '')
        search = self.request.GET.get('search', '')


        if not group_id:
            if search:
                return DispatchRegularly.objects.filter(Q(departure__contains=search) | Q(arrival__contains=search)).order_by('num1', 'num2')

            return DispatchRegularly.objects.all().order_by('num1', 'num2')
        else:
            group = get_object_or_404(RegularlyGroup, id=group_id)
            if search:
                return DispatchRegularly.objects.filter(group=group).filter(Q(departure__contains=search) | Q(arrival__contains=search)).order_by('num1', 'num2')
            return DispatchRegularly.objects.filter(group=group).order_by('num1', 'num2')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        id = self.request.GET.get('id')
        context['search'] = self.request.GET.get('search', '')


        if id:
            context['detail'] = get_object_or_404(DispatchRegularly, id=id)
            
        context['group_list'] = RegularlyGroup.objects.all().order_by('number', 'name')
        group_id = self.request.GET.get('group', '')
        if group_id:
            context['group'] = get_object_or_404(RegularlyGroup, id=group_id)
        
        return context

def regularly_order_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = RegularlyForm(request.POST)
        print("RRRR", request.POST)

        if order_form.is_valid():
            print("VALID")
            # if datetime.strptime(request.POST.get('contract_start_date'), FORMAT) > datetime.strptime(request.POST.get('contract_end_date'), FORMAT):
            #     context = {}
            #     # context['order_list'] = DispatchOrder.objects.exclude(regularly=None).order_by('-pk')
            #     context['group_list'] = RegularlyGroup.objects.all()
            #     # context['error'] = "출발일이 도착일보다 늦습니다"
            #     #raise BadRequest('출발일이 도착일보다 늦습니다.')
            #     #return render(request, 'dispatch/regularly_order_create.html', context)
            #     raise Http404
            post_group = request.POST.get('group', None)
            try:
                regularly_group = RegularlyGroup.objects.get(pk=post_group)
            except Exception as e:
                regularly_group = None

            week = ' '.join(request.POST.getlist('week', None))
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_driver_allowance = request.POST.get('driver_allowance')
            if post_driver_allowance:
                driver_allowance = int(post_driver_allowance.replace(',',''))
            else:
                driver_allowance = 0

            order = order_form.save(commit=False)
            
            order.price = price
            order.driver_allowance = driver_allowance
            order.departure_time = f'{departure_time1}:{departure_time2}'
            order.arrival_time = f'{arrival_time1}:{arrival_time2}'
            order.week = week
            order.creator = creator
            order.group = regularly_group
            order.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_order_edit(request):
    id = request.POST.get('id', None)
    order = get_object_or_404(DispatchRegularly, pk=id)
    
    if request.method == 'POST':
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = RegularlyForm(request.POST)
        if order_form.is_valid():
            # overlap = ''
            # overlap_list = DispatchRegularly.objects.exclude(departure_time__gt=order.arrival_time).exclude(arrival_time__lt=order.departure_time)
            # for dispatch in overlap_list:
            #     for i in order.week.split(" "):
            #         try:
            #             temp = dispatch.info_regularly_fixed.get(week=i)
            #             bus = temp.bus_id
            #             driver = temp.driver_id
            #             cur = order.info_regularly_fixed.get(week=i)
            #         except DispatchRegularlyFixed.DoesNotExist:
            #             continue

                    
            #         if bus == cur.bus_id or driver == cur.driver_id:
            #             overlap = dispatch
            # print("OVERLAP", overlap)

            group = get_object_or_404(RegularlyGroup, pk=request.POST.get('group'))
            week = ' '.join(request.POST.getlist('week', None))
        
            # if datetime.strptime(request.POST.get('contract_start_date'), FORMAT) > datetime.strptime(request.POST.get('contract_end_date'), FORMAT):
            #     #raise BadRequest('출발일이 도착일보다 늦습니다.')
            #     raise Http404
            
            # route_name = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'

            post_price = request.POST.get('price')
            if post_price:
                price = int(post_price.replace(',',''))
            else:
                price = 0
            
            post_driver_allowance = request.POST.get('driver_allowance')
            if post_driver_allowance:
                driver_allowance = int(post_driver_allowance.replace(',',''))
            else:
                driver_allowance = 0

            order.references = order_form.cleaned_data['references']
            order.departure = order_form.cleaned_data['departure']
            order.arrival = order_form.cleaned_data['arrival']
            order.departure_time = f'{departure_time1}:{departure_time2}'
            order.arrival_time = f'{arrival_time1}:{arrival_time2}'
            # order.bus_type = order_form.cleaned_data['bus_type']
            # order.bus_cnt = order_form.cleaned_data['bus_cnt']
            order.price = price
            order.driver_allowance = driver_allowance
            order.number1 = order_form.cleaned_data['number1']
            order.number2 = order_form.cleaned_data['number2']
            # order.customer = order_form.cleaned_data['customer']
            # order.customer_phone = order_form.cleaned_data['customer_phone']
            # order.contract_start_date = order_form.cleaned_data['contract_start_date']
            # order.contract_end_date = order_form.cleaned_data['contract_end_date']
            order.work_type = order_form.cleaned_data['work_type']
            order.route = order_form.cleaned_data['route']
            order.location = order_form.cleaned_data['location']
            order.detailed_route = order_form.cleaned_data['detailed_route']

            order.week = week
            order.group = group
            order.creator = creator
            order.save()
            
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else: 
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_order_upload(request):
    # post_data = json.loads(request.body.decode("utf-8"))
    # post_data.get('excel')
    # count = 0
    # for data in post_data:
    #     count = count + 1
    post_data = json.loads(request.body)
    
    group_list = RegularlyGroup.objects.values('name')
    print(post_data)

    count = 1
    for data in post_data:
        overlap = False
        for group in group_list:
            if group['name'] == data['group']:
                overlap = True
            
        if overlap == False:
            return JsonResponse({'group_error': data['group'], 'line': count})
        count += 1

    count = 0
    try:
        for data in post_data:
            group = get_object_or_404(RegularlyGroup, name=data['group'])
            regularly = DispatchRegularly(
                group = group,
                references = data['references'],
                departure = data['departure'],
                arrival = data['arrival'],
                departure_time = data['departure_time'],
                arrival_time = data['arrival_time'],
                price = data['price'],
                driver_allowance = data['driver_allowance'],
                number1 = data['number1'],
                number2 = data['number2'],
                week = data['week'],
                work_type = data['work_type'],
                route = data['route'],
                location = data['location'],
                detailed_route = data['detailed_route'],
                creator = get_object_or_404(Member, pk=request.session['user']),
            )
            regularly.save()
            count += 1
        return JsonResponse({'status': 'success', 'count': count})
    except Exception as e:
        print("ERROR", e)

        return JsonResponse({'status': 'fail', 'count': count})

def regularly_order_delete(request):
    if request.method == "POST":
        id_list = request.POST.getlist("check")
        group = request.POST.get('group', '')
        
        for pk in id_list:
            order = get_object_or_404(DispatchRegularly, pk=pk)
            order.delete()
        return redirect(reverse('dispatch:regularly_route') + f'?group={group}')
    else:
        return HttpResponseNotAllowed(['post'])

def regularly_group_create(request):
    if request.method == "POST":
        group = RegularlyGroup(
            name = request.POST.get('name'),
            number = '999',
            creator = get_object_or_404(Member, pk=request.session['user'])
        )
        group.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_edit(request):

    if request.method == "POST":
        id = request.POST.get('id', None)
        name = request.POST.get('name', None)
        group = get_object_or_404(RegularlyGroup, id=id)
        
        group.name = name
        group.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_delete(request):
    if request.method == "POST":
        group = get_object_or_404(RegularlyGroup, id=request.POST.get('id', None))
        group.delete()
        return redirect('dispatch:regularly_route')
    else:
        return HttpResponseNotAllowed(['POST'])

def regularly_group_fix(request):
    if request.method == "POST":
        
        post_data = json.loads(request.body.decode("utf-8"))

        group_list = post_data['order']
        fix = post_data['fix']
        
        try:
            for i in range(len(group_list)):
                id = group_list[i]
                group = get_object_or_404(RegularlyGroup, id=id)
                group.number = i
                if i+1 > int(fix):
                    group.fix = 'n'
                else:
                    group.fix = 'y'
                
                group.save()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'fail'})
    else:
        return HttpResponseNotAllowed(['POST'])

class OrderList(generic.ListView):
    template_name = 'dispatch/order.html'
    context_object_name = 'order_list'
    model = DispatchOrder

    def get_queryset(self):
        start_date = self.request.GET.get('date1')
        end_date = self.request.GET.get('date2')
        route = self.request.GET.get('route')
        # customer = self.request.GET.get('customer')
        # self.next_week = (datetime.strptime(TODAY, FORMAT) + timedelta(days=7)).strftime(FORMAT)

        if start_date or end_date or route:
            dispatch_list = []
            if start_date and end_date:
                dispatch_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{start_date} 00:00').exclude(departure_date__gt=f'{end_date} 24:00').order_by('departure_date')
                # dispatch_list = DispatchOrder.objects.filter(departure_date__range=[start_date + "T00:00", end_date + "T24:00"]).order_by('departure_date')
            if route:
                if dispatch_list:
                    dispatch_list = dispatch_list.filter(route__contains=route).order_by('departure_date')
                else:
                    dispatch_list = DispatchOrder.objects.prefetch_related('info_order').filter(route__contains=route).order_by('departure_date')
        else:
            
            dispatch_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{TODAY} 00:00').exclude(departure_date__gt=f'{TODAY} 24:00').order_by('departure_date')
        
        return dispatch_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        date = self.request.GET.get('date1', TODAY)
        
        # date2 = self.request.GET.get('date2', TODAY)
        # weekday = WEEK2[datetime.strptime(date, FORMAT).weekday()]
        detail_id = self.request.GET.get('id')
        if detail_id:
            context['detail'] = get_object_or_404(DispatchOrder, id=detail_id)
            date = context['detail'].departure_date[:10]
            date2 = context['detail'].arrival_date[:10]
            context['detail_connect_list'] = context['detail'].info_order.all()
            context['detail_connect_cnt'] = int(context['detail'].bus_cnt) - int(context['detail_connect_list'].count())

        driver_list = Member.objects.filter(role='운전원').values_list('id', 'name')
        context['driver_dict'] = {}
        for driver in driver_list:
            context['driver_dict'][driver[0]] = driver[1]

        outsourcing_list = Member.objects.filter(role='용역').values_list('id', 'name')
        context['outsourcing_dict'] = {}
        for outsourcing in outsourcing_list:
            context['outsourcing_dict'][outsourcing[0]] = outsourcing[1]
        #
        #출발일 ~ 도착일 범위로 한번만 돌면서 for문 안에서 현재 connect date 따라서 list에 appned
        if detail_id:
            r_connect_list = DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date2} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        else:
            r_connect_list = DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')
        dispatch_list = []
        dispatch_list2 = []
        dispatch_data_list = []
        for rc in r_connect_list:
            dispatch = rc.regularly_id
            data = {
                'work_type': dispatch.work_type,
                'departure_date': rc.departure_date,
                'arrival_date': rc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': rc.week,
                'bus_id': rc.bus_id.id,
                'bus_num': rc.bus_id.vehicle_num,
                'driver_id': rc.driver_id.id,
                'driver_name': rc.driver_id.name,
                'outsourcing': rc.outsourcing,
            }
            if detail_id:
                if context['detail'].departure_date[:10] in rc.arrival_date[:10]:
                    dispatch_list.append(data)
                elif context['detail'].arrival_date[:10] in rc.departure_date[:10]:
                    dispatch_list2.append(data)
                
            dispatch_data_list.append(data)
                
                
        if detail_id:
            connect_list = DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date2} 24:00').exclude(arrival_date__lt=f'{date} 00:00')    
        else:
            connect_list = DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00')

        for cc in connect_list:
            dispatch = cc.order_id
            data = {
                'work_type': '일반',
                'departure_date': cc.departure_date,
                'arrival_date': cc.arrival_date,
                'departure': dispatch.departure,
                'arrival': dispatch.arrival,
                # 'week': cc.week,
                'bus_id': cc.bus_id.id,
                'bus_num': cc.bus_id.vehicle_num,
                'driver_id': cc.driver_id.id,
                'driver_name': cc.driver_id.name,
                'outsourcing': cc.outsourcing,
            }
            if detail_id:
                if context['detail'].departure_date[:10] in dispatch.arrival_date[:10]:
                    dispatch_list.append(data)
                elif context['detail'].arrival_date[:10] in dispatch.departure_date[:10]:
                    dispatch_list2.append(data)
            
            dispatch_data_list.append(data)

        context['dispatch_list'] = dispatch_list
        context['dispatch_list2'] = dispatch_list2
        context['dispatch_data_list'] = dispatch_data_list
        #
        
        total = {}
        total['c_bus_cnt'] = 0
        total['bus_cnt'] = 0
        total['driver_allowance'] = 0
        total['price'] = 0
        total['collection_amount'] = 0
        
        for order in context['order_list']:
            total['c_bus_cnt'] += int(order.info_order.count())
            total['bus_cnt'] += int(order.bus_cnt)
            total['driver_allowance'] += int(order.driver_allowance)
            total['price'] += int(order.price)
            total['collection_amount'] += int(order.collection_amount)
            
        total['outstanding_amount'] = total['price'] - total['collection_amount']
        context['total'] = total
        
        context['vehicles'] = Vehicle.objects.filter(use='y').order_by('vehicle_num', 'driver_name')
        context['selected_date1'] = self.request.GET.get('date1')
        context['selected_date2'] = self.request.GET.get('date2')

        return context

def order_connect_create(request):
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))
        order = get_object_or_404(DispatchOrder, id=request.POST.get('id', None))
        outsourcing_list = []
        payment_method_list = []
        for i in range(int(order.bus_cnt)):
            outsourcing_id = request.POST.get(f'outsourcing{i}', '')
            outsourcing_list.append(outsourcing_id)

            post_payment_method = request.POST.get(f'payment_method{i}', '')
            payment_method_list.append(post_payment_method)
        

        bus_list = request.POST.getlist('bus')
        driver_list = request.POST.getlist('driver')
        price_list = request.POST.getlist('price')
        driver_allowance_list = request.POST.getlist('driver_allowance')

        connect = order.info_order.all()
        connect.delete()
        count = 0
        for bus, driver_id in zip(bus_list, driver_list):
            if not bus:
                continue
            vehicle = Vehicle.objects.get(id=bus)
            if outsourcing_list[count]:
                driver = Member.objects.get(id=outsourcing_list[count])
                outsourcing = 'y'
            else:
                driver = Member.objects.get(id=driver_id)
                outsourcing = 'n'

            price = price_list[count].replace(",","")
            allowance = driver_allowance_list[count].replace(",","")
            
            connect = DispatchOrderConnect(
                order_id = order,
                bus_id = vehicle,
                driver_id = driver,
                payment_method = payment_method_list[count],
                outsourcing = outsourcing,
                departure_date = order.departure_date,
                arrival_date = order.arrival_date,
                driver_allowance = allowance,
                price = price,
                creator = creator,
            )
            connect.save()
            count = count + 1
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponseNotAllowed(['post'])


def order_create(request):
    if request.method == "POST":
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)
        waypoint_list = request.POST.getlist('waypoint')
        waypoint_time_list = request.POST.getlist('waypoint_time')
        delegate_list = request.POST.getlist('delegate')
        delegate_phone_list = request.POST.getlist('delegate_phone')


        print("POST", request.POST)
        if order_form.is_valid() and len(waypoint_list) == len(waypoint_time_list):
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'
            
            if request.POST.get('price'):
                price = int(request.POST.get('price').replace(',',''))
            else:
                price = 0
            if request.POST.get('driver_allowance'):
                driver_allowance = int(request.POST.get('driver_allowance').replace(',',''))
            else:
                driver_allowance = 0

            order = order_form.save(commit=False)
            order.price = price
            order.driver_allowance = driver_allowance
            order.VAT = request.POST.get('VAT', 'n')
            order.creator = creator
            order.cost_type = ' '.join(request.POST.getlist('cost_type'))
            order.option = ' '.join(request.POST.getlist('option'))
            order.departure_date = f"{request.POST.get('departure_date')} {departure_time1}:{departure_time2}"
            order.arrival_date = f"{request.POST.get('arrival_date')} {arrival_time1}:{arrival_time2}"
            order.route = request.POST.get('departure') + " ▶ " + request.POST.get('arrival')
            order.save()

            for i in range(len(waypoint_list)):
                waypoint = DispatchOrderWaypoint(
                    order_id=order,
                    waypoint=waypoint_list[i],
                    time=waypoint_time_list[i],
                    delegate=delegate_list[i] if delegate_list[i] != " " else '',
                    delegate_phone=delegate_phone_list[i] if delegate_phone_list[i] != " " else '',
                    creator=creator,
                )
                waypoint.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def order_edit_check(request):
    pk = request.POST.get('id')
    order = get_object_or_404(DispatchOrder, pk=pk)
    #
    connects = order.info_order.all()
    # r_connects = order.info_regularly.all()
    post_departure_date = request.POST.get('departure_date', None)
    post_arrival_date = request.POST.get('arrival_date', None)

    for connect in connects:
        bus = connect.bus_id
        # r_connects = bus.info_regularly_bus_id.all()

        

        format = '%Y-%m-%d %H:%M'
        if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
            print("term begin > term end")
            raise Http404
        o_connect = bus.info_bus_id.exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date).exclude(id__in=connects)
        if o_connect:
            return JsonResponse({
                "status": "fail",
                'route': o_connect[0].order_id.route,
                'driver': o_connect[0].driver_id.name,
                'bus': o_connect[0].bus_id.vehicle_num,
                'arrival_date': o_connect[0].arrival_date,
                'departure_date': o_connect[0].departure_date,
            })
        r_connect = bus.info_regularly_bus_id.exclude(arrival_date__lt=post_departure_date).exclude(departure_date__gt=post_arrival_date)
        if r_connect:
            return JsonResponse({"status": "fail", 'connect': r_connect})
    
    return JsonResponse({'status': 'success', 'departure_date': post_departure_date, 'arrival_date': post_arrival_date})

def order_edit(request):
    pk = request.POST.get('id')
    order = get_object_or_404(DispatchOrder, pk=pk)
    
    if request.method == 'POST':
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        order_form = OrderForm(request.POST)

        waypoint_list = request.POST.getlist('waypoint')
        waypoint_time_list = request.POST.getlist('waypoint_time')
        delegate_list = request.POST.getlist('delegate')
        delegate_phone_list = request.POST.getlist('delegate_phone')


        if order_form.is_valid():
            post_departure_date = request.POST.get('departure_date', None)
            post_arrival_date = request.POST.get('arrival_date', None)
            
            departure_time1 = request.POST.get('departure_time1')
            departure_time2 = request.POST.get('departure_time2')
            arrival_time1 = request.POST.get('arrival_time1')
            arrival_time2 = request.POST.get('arrival_time2')

            if len(departure_time1) < 2:
                departure_time1 = f'0{departure_time1}'
            if len(departure_time2) < 2:
                departure_time2 = f'0{departure_time2}'
            if len(arrival_time1) < 2:
                arrival_time1 = f'0{arrival_time1}'
            if len(arrival_time2) < 2:
                arrival_time2 = f'0{arrival_time2}'

            departure_date = f'{post_departure_date} {departure_time1}:{departure_time2}'
            arrival_date = f'{post_arrival_date} {arrival_time1}:{arrival_time2}'
            format = '%Y-%m-%d'
            if datetime.strptime(post_departure_date, format) > datetime.strptime(post_arrival_date, format):
                print("term begin > term end")
                raise Http404

            #
            connects = order.info_order.all()
            
            for connect in connects:
                connect.departure_date = departure_date
                connect.arrival_date = arrival_date
                connect.save()
            

            if request.POST.get('price'):
                price = int(request.POST.get('price').replace(',',''))
            else:
                price = 0
            if request.POST.get('driver_allowance'):
                driver_allowance = int(request.POST.get('driver_allowance').replace(',',''))
            else:
                driver_allowance = 0

            order.operation_type = order_form.cleaned_data['operation_type']
            order.references = order_form.cleaned_data['references']
            order.departure = order_form.cleaned_data['departure']
            order.arrival = order_form.cleaned_data['arrival']
            order.departure_date = departure_date
            order.arrival_date = arrival_date
            order.bus_type = order_form.cleaned_data['bus_type']
            order.bus_cnt = order_form.cleaned_data['bus_cnt']
            order.price = price
            order.driver_allowance = driver_allowance
            order.contract_status = order_form.cleaned_data['contract_status']
            order.cost_type = ' '.join(request.POST.getlist('cost_type'))
            order.option = ' '.join(request.POST.getlist('option'))
            order.customer = order_form.cleaned_data['customer']
            order.customer_phone = order_form.cleaned_data['customer_phone']
            order.bill_place = order_form.cleaned_data['bill_place']
            order.ticketing_info = order_form.cleaned_data['ticketing_info']
            order.collection_type = order_form.cleaned_data['collection_type']
            
            order.VAT = request.POST.get('VAT', 'n')
            order.route = order_form.cleaned_data['departure'] + " ▶ " + order_form.cleaned_data['arrival']
            order.creator = creator
            print("ORDER", order)
            order.save()

            # 경유지 처리
            order.waypoint.all().delete()

            for i in range(len(waypoint_list)):
                waypoint = DispatchOrderWaypoint(
                    order_id=order,
                    waypoint=waypoint_list[i],
                    time=waypoint_time_list[i],
                    delegate=delegate_list[i] if delegate_list[i] != " " else '',
                    delegate_phone=delegate_phone_list[i] if delegate_phone_list[i] != " " else '',
                    creator=creator,
                )
                waypoint.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['post'])

def order_delete(request):
    if request.method == "POST":
        id_list = request.POST.getlist('id', None)
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')

        for id in id_list:
            order = get_object_or_404(DispatchOrder, id=id)
            order.delete()

        return redirect(reverse('dispatch:order') + f'?date1={date1}&date2={date2}')
    else:
        return HttpResponseNotAllowed(['post'])

def line_print(request):
    context = {}
    date = request.GET.get('date')
    week = WEEK[datetime.strptime(date, FORMAT).weekday()][1]
    
    
    regularly_list = DispatchRegularly.objects.prefetch_related('info_regularly').exclude(info_regularly=None).filter(week__contains=week).order_by('group', 'number1', 'number2', 'departure_time')
    print(regularly_list)
    temp = []
    temp2 = []
    group = ''
    context['regularly_list'] = []
    context['connect_list'] = []
    for r in regularly_list:
        print("GROUP", r.group.name)
        if r.group.name != group:
            group = r.group.name
            if r != regularly_list[0]:
                context['regularly_list'].append(temp)
                context['connect_list'].append(temp2)
                temp = []
                temp2 = []
        temp.append(r)
        temp2.append(r.info_regularly.filter(departure_date__startswith=date))

    if r == regularly_list[len(regularly_list)-1]:
        context['regularly_list'].append(temp)
        context['connect_list'].append(temp2)

        
        
    no_list = DispatchRegularly.objects.filter(info_regularly=None).order_by('group', 'number1', 'number2', 'departure_time')
    
    print('REGULSRY', context['regularly_list'])
    print('connect_list', context['connect_list'])
    context['no_list'] = no_list

    return render(request, 'dispatch/line_print.html', context)

def bus_print(request):
    context = {}
    date = request.GET.get('date')

    vehicle_list = Vehicle.objects.filter(use='y').order_by('vehicle_num')
    context['vehicle_list'] = vehicle_list
    
    connect_object = {}
    e_connect_object = {}
    c_connect_object = {}
    for vehicle in vehicle_list:
        connect_object[vehicle.id] = []
        e_connect_object[vehicle.id] = []
        c_connect_object[vehicle.id] = []

    r_connect_list = DispatchRegularlyConnect.objects.select_related('bus_id', 'regularly_id').filter(departure_date__startswith=date).order_by('departure_date')
    for connect in r_connect_list:
        if connect.work_type == "출근":
            e_connect_object[connect.bus_id.id].append(connect)
        elif connect.work_type == "퇴근":
            c_connect_object[connect.bus_id.id].append(connect)

    connect_list = DispatchOrderConnect.objects.select_related('bus_id', 'order_id').filter(departure_date__lte=f'{date}T24:00').filter(arrival_date__gte=f'{date}T00:00')
    print("CONNECTSLIST", connect_list)
    for connect in connect_list:
        connect_object[connect.bus_id.id].append(connect)


    context['connect_object'] = connect_object
    context['e_connect_object'] = e_connect_object
    context['c_connect_object'] = c_connect_object
    return render(request, 'dispatch/bus_print.html', context)

def daily_driving_list(request):
    context = {}
    date = request.GET.get('date')

    vehicle_list = Vehicle.objects.filter(use='y').order_by('vehicle_num')
    context['vehicle_list'] = vehicle_list
    
    connect_object = {}
    e_connect_object = {}
    c_connect_object = {}
    for vehicle in vehicle_list:
        connect_object[vehicle.id] = []
        e_connect_object[vehicle.id] = []
        c_connect_object[vehicle.id] = []

    r_connect_list = DispatchRegularlyConnect.objects.select_related('bus_id', 'regularly_id').filter(departure_date__startswith=date).order_by('departure_date')
    for connect in r_connect_list:
        if connect.work_type == "출근":
            e_connect_object[connect.bus_id.id].append(connect)
        elif connect.work_type == "퇴근":
            c_connect_object[connect.bus_id.id].append(connect)

    connect_list = DispatchOrderConnect.objects.select_related('bus_id', 'order_id').filter(departure_date__lte=f'{date}T24:00').filter(arrival_date__gte=f'{date}T00:00')
    print("CONNECTSLIST", connect_list)
    for connect in connect_list:
        connect_object[connect.bus_id.id].append(connect)


    context['connect_object'] = connect_object
    context['e_connect_object'] = e_connect_object
    context['c_connect_object'] = c_connect_object
    return render(request, 'dispatch/daily_driving_list.html', context)

def daily_driving_print(request):
    id_list = request.GET.get('id').split(',')
    date = request.GET.get('date')
    context = {}
    context['vehicle_list'] = []
    context['order_list'] = []
    context['e_order_list'] = []
    context['c_order_list'] = []
    context['cnt'] = len(id_list)
    context['date'] = date

    for id in id_list:
        if id and date:
            vehicle = get_object_or_404(Vehicle, id=id)
            context['vehicle_list'].append(vehicle)
            context['order_list'].append(DispatchOrderConnect.objects.select_related('order_id').filter(departure_date__lte=f'{date}T24:00').filter(arrival_date__gte=f'{date}T00:00').filter(bus_id=vehicle).order_by('departure_date'))
            context['e_order_list'].append(DispatchRegularlyConnect.objects.select_related('regularly_id').filter(departure_date__startswith=date).filter(work_type="출근").filter(bus_id=vehicle).order_by('departure_date'))
            context['c_order_list'].append(DispatchRegularlyConnect.objects.select_related('regularly_id').filter(departure_date__startswith=date).filter(work_type="퇴근").filter(bus_id=vehicle).order_by('departure_date'))
            print("ENETET", context['e_order_list'])

        else:
            raise Http404



    return render(request, 'dispatch/daily_driving_print.html', context)
    

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@