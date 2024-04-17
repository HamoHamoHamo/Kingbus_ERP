from .models import DispatchRegularlyConnect, DispatchOrderConnect, DispatchOrder
from assignment.models import AssignmentConnect, Assignment

def get_date_connect_list(date):
    dispatch_list = []
    
    r_connect_list = list(DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00').values('departure_date', 'arrival_date', 'bus_id__id', 'bus_id__vehicle_num', 'driver_id__id', 'driver_id__name', 'outsourcing', 'regularly_id__work_type', 'regularly_id__departure', 'regularly_id__arrival'))
    dispatch_list = []
    for rc in r_connect_list:
        data = {
            'work_type': rc['regularly_id__work_type'],
            'departure_date': rc['departure_date'],
            'arrival_date': rc['arrival_date'],
            'departure': rc['regularly_id__departure'],
            'arrival': rc['regularly_id__arrival'],
            'bus_id': rc['bus_id__id'],
            'bus_num': rc['bus_id__vehicle_num'],
            'driver_id': rc['driver_id__id'],
            'driver_name': rc['driver_id__name'],
            'outsourcing': rc['outsourcing'],
        }
        dispatch_list.append(data)
    connect_list = list(DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date} 24:00').exclude(arrival_date__lt=f'{date} 00:00').values('departure_date', 'arrival_date', 'bus_id__id', 'bus_id__vehicle_num', 'driver_id__id', 'driver_id__name', 'outsourcing', 'order_id__departure', 'order_id__arrival'))
    for cc in connect_list:
        data = {
            'work_type': '일반',
            'departure_date': cc['departure_date'],
            'arrival_date': cc['arrival_date'],
            'departure': cc['order_id__departure'],
            'arrival': cc['order_id__arrival'],
            'bus_id': cc['bus_id__id'],
            'bus_num': cc['bus_id__vehicle_num'],
            'driver_id': cc['driver_id__id'],
            'driver_name': cc['driver_id__name'],
            'outsourcing': cc['outsourcing'],
        }
        dispatch_list.append(data)

    a_connect_list = list(AssignmentConnect.objects.select_related('assignment_id', 'member_id', 'bus_id').exclude(start_date__gt=f'{date} 24:00').exclude(end_date__lt=f'{date} 00:00').values('start_date', 'end_date', 'bus_id__id', 'bus_id__vehicle_num', 'member_id__id', 'member_id__name', 'assignment_id__assignment', 'type'))
    for cc in a_connect_list:
        data = {
            'work_type': cc['type'],
            'departure_date': cc['start_date'],
            'arrival_date': cc['end_date'],
            'bus_id': cc['bus_id__id'] if cc['bus_id__id'] else "",
            'bus_num': cc['bus_id__vehicle_num'] if cc['bus_id__vehicle_num'] else "",
            'driver_id': cc['member_id__id'],
            'driver_name': cc['member_id__name'],
            'outsourcing': 'n',
            'assignment': cc['assignment_id__assignment']
        }
        dispatch_list.append(data)
    return dispatch_list

def get_multi_date_connect_list(date1, date2, detail):
    if detail and type(detail) == Assignment:
        detail_start_date = detail.start_time
        detail_end_date = detail.end_time
    elif detail and type(detail) == DispatchOrder:
        detail_start_date = detail.departure_date
        detail_end_date = detail.arrival_date

    r_connect_list = list(DispatchRegularlyConnect.objects.select_related('regularly_id').exclude(departure_date__gt=f'{date2} 24:00').exclude(arrival_date__lt=f'{date1} 00:00').values('departure_date', 'arrival_date', 'bus_id__id', 'bus_id__vehicle_num', 'driver_id__id', 'driver_id__name', 'outsourcing', 'regularly_id__work_type', 'regularly_id__departure', 'regularly_id__arrival'))
    dispatch_list = []
    dispatch_list2 = []
    dispatch_data_list = []
    for rc in r_connect_list:
        data = {
            'work_type': rc['regularly_id__work_type'],
            'departure_date': rc['departure_date'],
            'arrival_date': rc['arrival_date'],
            'departure': rc['regularly_id__departure'],
            'arrival': rc['regularly_id__arrival'],
            'bus_id': rc['bus_id__id'],
            'bus_num': rc['bus_id__vehicle_num'],
            'driver_id': rc['driver_id__id'],
            'driver_name': rc['driver_id__name'],
            'outsourcing': rc['outsourcing'],
        }
        if detail:
            if detail_start_date[:10] in data['arrival_date'][:10]:
                dispatch_list.append(data)
            elif detail_end_date[:10] in data['departure_date'][:10]:
                dispatch_list2.append(data)
            
        dispatch_data_list.append(data)
            
    
    connect_list = list(DispatchOrderConnect.objects.select_related('order_id').exclude(departure_date__gt=f'{date2} 24:00').exclude(arrival_date__lt=f'{date1} 00:00').values('departure_date', 'arrival_date', 'bus_id__id', 'bus_id__vehicle_num', 'driver_id__id', 'driver_id__name', 'outsourcing', 'order_id__departure', 'order_id__arrival'))
    for cc in connect_list:
        data = {
            'work_type': '일반',
            'departure_date': cc['departure_date'],
            'arrival_date': cc['arrival_date'],
            'departure': cc['order_id__departure'],
            'arrival': cc['order_id__arrival'],
            'bus_id': cc['bus_id__id'],
            'bus_num': cc['bus_id__vehicle_num'],
            'driver_id': cc['driver_id__id'],
            'driver_name': cc['driver_id__name'],
            'outsourcing': cc['outsourcing'],
        }
        if detail:
            if detail_start_date[:10] in data['arrival_date'][:10]:
                dispatch_list.append(data)
            elif detail_end_date[:10] in data['departure_date'][:10]:
                dispatch_list2.append(data)
        
        dispatch_data_list.append(data)

    a_connect_list = list(AssignmentConnect.objects.select_related('assignment_id', 'member_id', 'bus_id').exclude(start_date__gt=f'{date2} 24:00').exclude(end_date__lt=f'{date1} 00:00').values('start_date', 'end_date', 'bus_id__id', 'bus_id__vehicle_num', 'member_id__id', 'member_id__name', 'assignment_id__assignment', 'type'))
    for cc in a_connect_list:
        data = {
            # 왼쪽 표에 배차 스케줄 표시할 때 assignment에 type 추가해야됨
            'work_type': cc['type'],
            'departure_date': cc['start_date'],
            'arrival_date': cc['end_date'],
            'bus_id': cc['bus_id__id'] if cc['bus_id__id'] else "",
            'bus_num': cc['bus_id__vehicle_num'] if cc['bus_id__vehicle_num'] else "",
            'driver_id': cc['member_id__id'],
            'driver_name': cc['member_id__name'],
            'outsourcing': 'n',
            'assignment': cc['assignment_id__assignment']
        }
        if detail:
            if detail_start_date[:10] in data['arrival_date'][:10]:
                dispatch_list.append(data)
            elif detail_end_date[:10] in data['departure_date'][:10]:
                dispatch_list2.append(data)
        
        dispatch_data_list.append(data)

    return {
        'dispatch_list' : dispatch_list,
        'dispatch_list2' : dispatch_list2,
        'dispatch_data_list' : dispatch_data_list,
    }