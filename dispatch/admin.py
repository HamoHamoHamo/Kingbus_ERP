from django.contrib import admin
from .models import Schedule, DispatchOrder, DispatchOrderConnect, RegularlyGroup, \
    DispatchRegularly, DispatchRegularlyData, DispatchRegularlyConnect, DispatchCheck, \
    DispatchOrderWaypoint, DriverCheck, ConnectRefusal, DispatchRegularlyWaypoint, DispatchRegularlyRouteKnow, \
    MorningChecklist, EveningChecklist, DrivingHistory

# class DispatchInfoInline(admin.TabularInline):
#     model = DispatchOrderConnect


# class DispatchOrderAdmin(admin.ModelAdmin):
#     list_display = ('pk','departure','arrival','route_name','pub_date')
#     inlines = (DispatchInfoInline,)

# class DispatchConnectAdmin(admin.ModelAdmin):
#     list_display = ('pk','departure_date','arrival_date')
#     list_per_page = 10

@admin.register(DriverCheck)
class DriverCheckAdmin(admin.ModelAdmin):
    list_display = ['regularly_id', 'order_id', 'wake_time','drive_time','departure_time', 'updated_at']

@admin.register(ConnectRefusal)
class ConnectRefusalAdmin(admin.ModelAdmin):
    list_display = ['regularly_id', 'order_id', 'driver_id', 'refusal', 'updated_at']
    

admin.site.register(DispatchOrder)
admin.site.register(DispatchOrderConnect)
admin.site.register(RegularlyGroup)
admin.site.register(DispatchRegularly)
admin.site.register(DispatchRegularlyData)
admin.site.register(DispatchRegularlyWaypoint)
admin.site.register(DispatchRegularlyConnect)
admin.site.register(DispatchCheck)
admin.site.register(DispatchOrderWaypoint)
admin.site.register(DispatchRegularlyRouteKnow)
admin.site.register(Schedule)
admin.site.register(MorningChecklist)
admin.site.register(EveningChecklist)
admin.site.register(DrivingHistory)
