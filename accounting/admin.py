from django.contrib import admin
from .models import Outlay, Income, Salary, Collect

class OutlayAdmin(admin.ModelAdmin):
    list_display = ['id', 'outlay_date', 'pub_date' ]

admin.site.register(Outlay, OutlayAdmin)
admin.site.register(Salary)
admin.site.register(Income)
admin.site.register(Collect)