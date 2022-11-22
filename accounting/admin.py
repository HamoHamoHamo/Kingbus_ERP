from django.contrib import admin
from .models import Income, Collect, LastIncome, AdditionalCollect, TotalPrice
class OutlayAdmin(admin.ModelAdmin):
    list_display = ['id', 'outlay_date', 'pub_date' ]

admin.site.register(Income)
admin.site.register(Collect)
admin.site.register(LastIncome)
admin.site.register(AdditionalCollect)
admin.site.register(TotalPrice)
