from django.contrib import admin
from .models import Outlay, Income, MonthlySalary, DailySalary, Collect

class OutlayAdmin(admin.ModelAdmin):
    list_display = ['id', 'outlay_date', 'pub_date' ]

admin.site.register(Outlay, OutlayAdmin)
admin.site.register(MonthlySalary)
admin.site.register(DailySalary)
admin.site.register(Income)
admin.site.register(Collect)