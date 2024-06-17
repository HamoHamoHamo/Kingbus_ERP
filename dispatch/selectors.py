from django.db.models import Q, Value

from .models import DispatchOrder, DispatchRegularlyData, DispatchRegularly, DispatchOrderConnect, DispatchRegularlyConnect, MorningChecklist, EveningChecklist

class DispatchSelector:

    def get_monthly_driving_time_list(self, month):
        regularly = list(DispatchRegularlyConnect.objects.filter(departure_date__startswith=month).order_by('departure_date').values("driver_id", "departure_date", "arrival_date", "work_type"))
        order = list(DispatchOrderConnect.objects.filter(departure_date__startswith=month).annotate(work_type=Value("일반")).order_by('departure_date').values("driver_id", "departure_date", "arrival_date", "work_type"))
        return regularly + order

    def get_monthly_morning_checklist(self, month):
        return list(MorningChecklist.objects.filter(submit_check=True).filter(date__startswith=month).values("date", "member", "arrival_time", "updated_at"))

    def get_monthly_evening_checklist(self, month):
        return list(EveningChecklist.objects.filter(submit_check=True).filter(date__startswith=month).values("date", "member", "updated_at"))
