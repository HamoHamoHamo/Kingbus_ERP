from django.contrib import admin
from .models import Outlay, Income, MonthlySalary, DailySalary, Collect



admin.site.register(Outlay)
admin.site.register(MonthlySalary)
admin.site.register(DailySalary)
admin.site.register(Income)
admin.site.register(Collect)