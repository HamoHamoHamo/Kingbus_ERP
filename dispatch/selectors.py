from django.db.models import Value, F, Prefetch

from .models import DispatchRegularly, DispatchOrderConnect, DispatchRegularlyConnect, MorningChecklist, EveningChecklist, DispatchRegularlyStation
from assignment.models import AssignmentConnect

class DispatchSelector:

    def get_monthly_driving_time_list(self, month):
        regularly = list(
            DispatchRegularlyConnect.objects.filter(departure_date__startswith=month)
            .order_by('departure_date')
            .values(
                "driver_id", 
                "departure_date", 
                "arrival_date", 
                "work_type", 
                "time"
            )
        )

        order = list(
            DispatchOrderConnect.objects.filter(departure_date__startswith=month)
            .annotate(
                time=F("order_id__time"),
            )
            .order_by('departure_date')
            .values(
                "driver_id", 
                "departure_date", 
                "arrival_date", 
                "work_type",
                'time'
            )
        )
        return regularly + order

    def get_driving_time_list(self, start_date, end_date):
        regularly = list(
            DispatchRegularlyConnect.objects.filter(departure_date__gte=f'{start_date} 00:00', arrival_date__lte=f'{end_date} 23:59')
            .select_related('regularly_id__group')
            .annotate(
                route_time=F("regularly_id__time"),
                group=F("regularly_id__group__name"),
                route=F("regularly_id__route"),
            )
            .order_by('departure_date')
            .values(
                "driver_id",
                "departure_date", 
                "arrival_date", 
                "work_type",
                "route_time",
                "group",
                "regularly_id",
                "route",
            )
        )

        # 정류장 시간 추가
        regularly_ids = [item['regularly_id'] for item in regularly]
    
        # Fetch DispatchRegularly objects with related DispatchRegularlyStation without using values()
        regularly_objects = DispatchRegularly.objects.filter(id__in=regularly_ids).prefetch_related(
            Prefetch(
                'regularly_station',
                queryset=DispatchRegularlyStation.objects.only('time', 'regularly_id').order_by('index'),
                to_attr='stations_list'
            )
        )
        
        # Create a dictionary to map regularly_id to its stations_list times
        regularly_map = {}
        for reg in regularly_objects:
            stations_times = [station.time for station in reg.stations_list]
            regularly_map[reg.id] = stations_times
        
        # Add the stations_list to the regularly items
        for item in regularly:
            item['stations_list'] = regularly_map.get(item['regularly_id'], [])
        
        # 일반운행
        order = list(
            DispatchOrderConnect.objects.filter(departure_date__gte=f'{start_date} 00:00', arrival_date__lte=f'{end_date} 23:59')
            .annotate(
                route_time=F("order_id__time"),
                route=F("order_id__route"),
                night_work_time=F("order_id__night_work_time"),
                stations_list=Value("")
            )
            .order_by('departure_date')
            .values(
                "driver_id",
                "departure_date", 
                "arrival_date", 
                "work_type",
                "route_time",
                'night_work_time',
                'route',
            )
        )

        assignment = list(
            AssignmentConnect.objects.filter(start_date__gte=f'{start_date} 00:00', end_date__lte=f'{end_date} 23:59')
            .annotate(
                night_work_time=Value(""),
                route_time=Value(""),
                work_type=Value("업무"),
                departure_date=F("start_date"),
                arrival_date=F("end_date"),
                driver_id=F("member_id"),
                route=F("assignment_id__assignment")
            )
            .order_by('start_date')
            .values(
                "driver_id",
                "departure_date", 
                "arrival_date", 
                "work_type",
                "route_time",
                'night_work_time',
                'route',
            )
        )

        return regularly + order + assignment


    def get_monthly_morning_checklist(self, month):
        return list(MorningChecklist.objects.filter(submit_check=True).filter(date__startswith=month).values("date", "member", "arrival_time", "updated_at"))

    def get_monthly_evening_checklist(self, month):
        return list(EveningChecklist.objects.filter(submit_check=True).filter(date__startswith=month).values("date", "member", "updated_at"))

    def get_morning_checklist(self, start_date, end_date):
        return list(MorningChecklist.objects.filter(submit_check=True).filter(date__gte=start_date).filter(date__lte=end_date).values("date", "member", "arrival_time", "updated_at"))

    def get_evening_checklist(self, start_date, end_date):
        return list(EveningChecklist.objects.filter(submit_check=True).filter(date__gte=start_date).filter(date__lte=end_date).values("date", "member", "updated_at"))


    def get_daily_connect_list(self, date):
        regularly = list(
            DispatchRegularlyConnect.objects.filter(departure_date__gte=f'{date} 00:00', arrival_date__lte=f'{date} 23:59')
            .annotate(
                driver=F("driver_id__name"),
                driver_vehicle=Value(""),
                driver_phone_num=F("driver_id__phone_num"),
                bus=F("bus_id__vehicle_num"),
                arrival=F("regularly_id__arrival"),
                departure=F("regularly_id__departure"),
                wake_t=F("check_regularly_connect__wake_time"),
                drive_t=F("check_regularly_connect__drive_time"),
                departure_t=F("check_regularly_connect__departure_time"),
                check=Value(""),
                connect_check=F("check_regularly_connect__connect_check"),
                order_time=F("regularly_id__time"),
                time_list=F("regularly_id__time_list"),
            )
            .order_by('departure_date')
            .values(
                "driver",
                "driver_vehicle",
                "driver_phone_num",
                "bus",
                "departure_date",
                "arrival_date",
                "departure",
                "arrival",
                "wake_t",
                "drive_t",
                "departure_t",
                "check",
                "connect_check",
                "work_type",
                "order_time",
                "time_list",
                'time',
            )
        )

        order = list(
            DispatchOrderConnect.objects.filter(departure_date__gte=f'{date} 00:00', arrival_date__lte=f'{date} 23:59')
            .annotate(
                driver=F("driver_id__name"),
                driver_vehicle=Value(""),
                driver_phone_num=F("driver_id__phone_num"),
                bus=F("bus_id__vehicle_num"),
                arrival=F("order_id__arrival"),
                departure=F("order_id__departure"),
                wake_t=F("check_order_connect__wake_time"),
                drive_t=F("check_order_connect__drive_time"),
                departure_t=F("check_order_connect__departure_time"),
                check=Value(""),
                connect_check=F("check_order_connect__connect_check"),
                order_time=F("order_id__time"),
                time_list=F("order_id__time_list"),
                time=Value(""),
            )
            .order_by('departure_date')
            .values(
                "driver",
                "driver_vehicle",
                "driver_phone_num",
                "bus",
                "departure_date",
                "arrival_date",
                "departure",
                "arrival",
                "wake_t",
                "drive_t",
                "departure_t",
                "check",
                "connect_check",
                "work_type",
                "order_time",
                "time_list",
                "time",
            )
        )
        return regularly + order

# type: ignore