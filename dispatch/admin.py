from django.contrib import admin
from .models import Schedule, DispatchOrder, DispatchOrderConnect, RegularlyGroup, DispatchRegularly, DispatchRegularlyConnect, DispatchCheck, DispatchOrderWaypoint

# class DispatchInfoInline(admin.TabularInline):
#     model = DispatchOrderConnect


# class DispatchOrderAdmin(admin.ModelAdmin):
#     list_display = ('pk','departure','arrival','route_name','pub_date')
#     inlines = (DispatchInfoInline,)

# class DispatchConnectAdmin(admin.ModelAdmin):
#     list_display = ('pk','departure_date','arrival_date')
#     list_per_page = 10


admin.site.register(DispatchOrder)
admin.site.register(DispatchOrderConnect)
admin.site.register(RegularlyGroup)
admin.site.register(DispatchRegularly)
admin.site.register(DispatchRegularlyConnect)
admin.site.register(DispatchCheck)
admin.site.register(DispatchOrderWaypoint)
admin.site.register(Schedule)
