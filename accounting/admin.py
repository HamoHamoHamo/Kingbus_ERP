from django.contrib import admin
from .models import Income, Salary, AdditionalSalary, Collect, LastIncome
class OutlayAdmin(admin.ModelAdmin):
    list_display = ['id', 'outlay_date', 'pub_date' ]

admin.site.register(Salary)
admin.site.register(Income)
admin.site.register(AdditionalSalary)
admin.site.register(Collect)
admin.site.register(LastIncome)