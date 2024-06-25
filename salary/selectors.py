from django.db.models import Q, Value, F

from .models import HourlyWage

class SalarySelector:
    def get_hourly_wage_by_month(self, month):
        try:
            return HourlyWage.objects.get(month=month)
        except HourlyWage.DoesNotExist:
            return None