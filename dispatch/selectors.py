from django.db.models import Q, Value, F, Prefetch

from .models import DispatchOrder, DispatchRegularlyData, DispatchRegularly, DispatchOrderConnect, DispatchRegularlyConnect, MorningChecklist, EveningChecklist, DispatchRegularlyStation

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
            .annotate(
                route_time=F("regularly_id__time"),
                time_list=F("regularly_id__time_list"),
                route=F("regularly_id__route"),
                group=F("regularly_id__group__name")
            )
            .order_by('departure_date')
            .values(
                'regularly_id',
                "driver_id", 
                "departure_date", 
                "arrival_date", 
                "work_type",
                "route_time",
                "route",
                "time",
                "time_list",
                "group",
            )
        )

        # 정류장 시간 추가
        regularly_ids = [item['regularly_id'] for item in regularly]
    
        # Fetch DispatchRegularly objects with related DispatchRegularlyStation without using values()
        regularly_objects = DispatchRegularly.objects.filter(id__in=regularly_ids).prefetch_related(
            Prefetch(
                'regularly_station',
                queryset=DispatchRegularlyStation.objects.order_by('index'),
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
                time=Value(""),
                time_list=F("order_id__time_list"),
                route=F("order_id__route")
            )
            .order_by('departure_date')
            .values(
                "order_id__route",
                "driver_id", 
                "departure_date", 
                "arrival_date", 
                "work_type",
                "route_time",
                "route",
                'time',
                'time_list',
            )
        )
        return regularly + order


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