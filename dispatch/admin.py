from django.contrib import admin
from .models import DispatchOrder, DispatchOrderConnect, RegularlyGroup, DispatchRegularly, DispatchRegularlyConnect, DispatchCheck

class DispatchInfoInline(admin.TabularInline):
    model = DispatchOrderConnect


class DispatchOrderAdmin(admin.ModelAdmin):
    list_display = ('pk','departure','arrival','route_name','pub_date')
    inlines = (DispatchInfoInline,)

class DispatchConnectAdmin(admin.ModelAdmin):
    list_display = ('pk','departure_date','arrival_date')
    list_per_page = 10


admin.site.register(DispatchOrder, DispatchOrderAdmin)
admin.site.register(DispatchOrderConnect, DispatchConnectAdmin)
admin.site.register(RegularlyGroup)
admin.site.register(DispatchRegularly)
admin.site.register(DispatchRegularlyConnect)
admin.site.register(DispatchCheck)