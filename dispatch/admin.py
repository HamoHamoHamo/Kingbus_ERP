from django.contrib import admin
from .models import DispatchOrder, DispatchConsumer, DispatchRoute, DispatchInfo

class DispatchRouteInline(admin.TabularInline):
    model = DispatchRoute

class DispatchInfoInline(admin.TabularInline):
    model = DispatchInfo

class DispatchOrderInline(admin.TabularInline):
    model = DispatchOrder

class DispatchConsumerAdmin(admin.ModelAdmin):
    inlines = (DispatchOrderInline,)

class DispatchOrderAdmin(admin.ModelAdmin):
    #list_display = ('title','creator','kinds','pub_date')
    inlines = (DispatchInfoInline, DispatchRouteInline,)


admin.site.register(DispatchOrder, DispatchOrderAdmin)
admin.site.register(DispatchRoute)
admin.site.register(DispatchInfo)
admin.site.register(DispatchConsumer, DispatchConsumerAdmin)