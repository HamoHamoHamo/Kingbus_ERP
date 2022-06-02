from django.contrib import admin
from .models import Vehicle, VehicleInsurance, VehicleDocument, VehicleCheck

# Register your models here.

class Vehicle_documentsInline(admin.TabularInline):
    model = VehicleDocument

class Vehicle_insurancesInline(admin.TabularInline):
    model = VehicleInsurance

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_num','group','vehicle_type','maker','model_year','driver','use','passenger_num')
    inlines = (Vehicle_documentsInline, Vehicle_insurancesInline)

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleInsurance)
admin.site.register(VehicleDocument)
admin.site.register(VehicleCheck)
