from django.contrib import admin
from .models import Vehicle, VehicleDocument, DailyChecklist, WeeklyChecklist, EquipmentChecklist, Maintenance, VehiclePhoto

# Register your models here.

class Vehicle_documentsInline(admin.TabularInline):
    model = VehicleDocument



class VehicleAdmin(admin.ModelAdmin):
    inlines = (Vehicle_documentsInline, )

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleDocument)
admin.site.register(DailyChecklist)
admin.site.register(WeeklyChecklist)
admin.site.register(EquipmentChecklist)
admin.site.register(Maintenance)
admin.site.register(VehiclePhoto)


