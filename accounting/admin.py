from django.contrib import admin
from .models import Income, Salary
class OutlayAdmin(admin.ModelAdmin):
    list_display = ['id', 'outlay_date', 'pub_date' ]

admin.site.register(Salary)
admin.site.register(Income)
