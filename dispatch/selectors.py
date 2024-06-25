from django.db.models import Q, Value, F

from .models import DispatchOrder, DispatchRegularlyData, DispatchRegularly, DispatchOrderConnect, DispatchRegularlyConnect, MorningChecklist, EveningChecklist

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
            DispatchOrderConnect.objects.filter(departure_date__gte=f'{start_date} 00:00', arrival_date__lte=f'{end_date} 23:59')
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


    def get_monthly_morning_checklist(self, month):
        return list(MorningChecklist.objects.filter(submit_check=True).filter(date__startswith=month).values("date", "member", "arrival_time", "updated_at"))

    def get_monthly_evening_checklist(self, month):
        return list(EveningChecklist.objects.filter(submit_check=True).filter(date__startswith=month).values("date", "member", "updated_at"))
