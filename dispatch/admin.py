from django.contrib import admin
from .models import DispatchOrder, DispatchConsumer, DispatchConnect, DispatchRoute

class DispatchInfoInline(admin.TabularInline):
    model = DispatchConnect

class DispatchOrderInline(admin.TabularInline):
    model = DispatchOrder

class DispatchConsumerAdmin(admin.ModelAdmin):
    inlines = (DispatchOrderInline,)

class DispatchRouteAdmin(admin.ModelAdmin):
    inlines = (DispatchOrderInline,)

class DispatchOrderAdmin(admin.ModelAdmin):
    #list_display = ('title','creator','kinds','pub_date')
    inlines = (DispatchInfoInline,)


admin.site.register(DispatchOrder, DispatchOrderAdmin)
admin.site.register(DispatchConnect)
admin.site.register(DispatchRoute, DispatchRouteAdmin)
admin.site.register(DispatchConsumer, DispatchConsumerAdmin)