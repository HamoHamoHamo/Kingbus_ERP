from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from dispatch.models import DispatchOrder

from datetime import datetime, timedelta, date

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"


class CompanyDocumentList(generic.ListView):
    template_name = 'document/company.html'
    context_object_name = 'order_list'
    model = DispatchOrder


class DocumentList(generic.ListView):
    template_name = 'document/document.html'
    context_object_name = 'order_list'
    model = DispatchOrder

    def get_queryset(self):
        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        order_list = DispatchOrder.objects.prefetch_related('info_order').filter(arrival_date__lte=f'{date2} 24:00').filter(departure_date__gte=f'{date1} 00:00')
        return order_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departure_date = []
        arrival_date = []
        time = []
        num_days = []

        for order in context['order_list']:
            d_y = order.departure_date[0:4]
            d_m = order.departure_date[5:7]
            d_d = order.departure_date[8:10]
            d_t = order.departure_date[11:16]
            d_date = date(int(d_y), int(d_m), int(d_d))
            
            d_y = d_y[2:4]

            a_y = order.arrival_date[0:4]
            a_m = order.arrival_date[5:7]
            a_d = order.arrival_date[8:10]
            a_t = order.arrival_date[11:16]
            a_date = date(int(a_y), int(a_m), int(a_d))
            
            a_y = a_y[2:4]
            
            date_diff = (a_date - d_date) + timedelta(days=1)
            if date_diff.days > 1:
                num_days.append(date_diff.days)
            else:
                num_days.append('')

            departure_date.append(f"{d_y}.{d_m}.{d_d}")
            time.append(f"{d_t}~{a_t}")
            arrival_date.append(f"{a_y}.{a_m}.{a_d}")

        connect_list = []
        for order in context['order_list']:
            connect_list.append(order.info_order.all())
        print("CONNETCTT", connect_list)
        context['connect_list'] = connect_list
        context['departure_date'] = departure_date
        context['arrival_date'] = arrival_date
        context['num_days'] = num_days
        context['time'] = time
        context['date1'] = self.request.GET.get('date1', TODAY)
        context['date2'] = self.request.GET.get('date2', TODAY)
        
        return context

def vehicle_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    file_list = []
    for connect in order.info_order.all():

        file = connect.bus_id.vehicle_file.all()
        if file.exists():
            file_list.append(file.get(type='vehicle_registration'))

    

    return render(request, 'document/vehicle_print.html', {'file_list': file_list})

def commitment_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    connect_list_all = order.info_order.all()
    cut = False
    connect_list = connect_list_all
    connect_list2 = ''
    if len(connect_list_all) > 18:
        cut = True
        connect_list = connect_list_all[:18]
        connect_list2 = connect_list_all[19:]
    
    return render(request, 'document/commitment_print.html', {'connect_list': connect_list, 'connect_list2': connect_list2, 'order': order, 'cut': cut})

def safety_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    connect_list = order.info_order.all()

    return render(request, 'document/safety_print.html', {'connect_list': connect_list, 'order': order})

def school_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)

    return render(request, 'document/school_print.html', {'order': order})

def drinking_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    connect_list = order.info_order.all()

    
    return render(request, 'document/drinking_print.html', {'connect_list': connect_list, 'departure_date': order.departure_date[:10], 'order': order})
