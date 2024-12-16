from dispatch.models import DispatchRegularlyConnect, DispatchOrderConnect, DispatchOrder, ConnectStatus, DriverCheck
from assignment.models import AssignmentConnect, Assignment
from datetime import datetime, timedelta
from common.constant import DATE_TIME_FORMAT

class DispatchConnectService:
    # 현재 해야하는 배차 정보 불러오기
    @staticmethod
    def get_current_connect(connects):
        """
        운행 완료가 아닌 가장 첫 번째 배차를 찾습니다.
        
        Args:
            connects (list): 배차 정보가 담긴 리스트
            
        Returns:
            dict or None: 조건에 맞는 첫 번째 배차. 없으면 None 반환
        """
        
        for connect in connects:            
            # 상태가 '운행 완료'가 아닌 첫번째 배차정보 리턴
            if connect['status'] != ConnectStatus.COMPLETE:
                return connect
                
        return None 
    
    # 배차 데이터 불러오기
    @staticmethod
    def get_daily_connect_list(date, user):
        regularly_connects = DispatchRegularlyConnect.objects.filter(departure_date__startswith=date, driver_id=user).select_related('regularly_id', 'bus_id')
        order_connects = DispatchOrderConnect.objects.filter(departure_date__startswith=date, driver_id=user).select_related('order_id', 'bus_id')

        return regularly_connects, order_connects
    
    # 1시간, 20분 범위 겹치는 배차 has_issue 발생하지 않도록 처리, 삭제 될 떄는?
    @staticmethod
    def prevent_dispatch_check_issues(date, user):
        regularly_connects, order_connects = DispatchConnectService.get_daily_connect_list(date, user)
        combined_data = list(regularly_connects.values('departure_date', 'arrival_date', 'id', 'work_type')) + list(order_connects.values('departure_date', 'arrival_date', 'id', 'work_type'))
        # departure_date 기준으로 정렬
        combined_data = sorted(combined_data, key=lambda x: x["departure_date"])

        # combined_data 순회하며 조건 확인
        for i in range(len(combined_data) - 1):  # 마지막 요소는 다음 배차가 없으므로 제외
            current_data = combined_data[i]
            next_data = combined_data[i + 1]
            
            current_arrival_date = datetime.strptime(current_data["arrival_date"], DATE_TIME_FORMAT)
            next_departure_date = datetime.strptime(next_data["departure_date"], DATE_TIME_FORMAT)

            # 다음 배차의 departure_date - 1시간 < 현재 배차의 arrival_date 조건
            if next_departure_date - timedelta(hours=1) <= current_arrival_date:
                if next_data['work_type'] == '출근' or next_data['work_type'] == '퇴근':
                    driver_check = DriverCheck.objects.get(regularly_id=next_data['id'])
                elif next_data['work_type'] == '일반':
                    driver_check = DriverCheck.objects.get(order_id=next_data['id'])
                driver_check.wake_time_has_issue = False
                print("")
                driver_check.save()

            # 다음 배차의 departure_date - 20분 < 현재 배차의 arrival_date 조건
            if next_departure_date - timedelta(minutes=20) <= current_arrival_date:
                driver_check.drive_time_has_issue = False
                driver_check.save()


    @staticmethod
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

    @staticmethod
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