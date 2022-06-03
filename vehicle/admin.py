from django.contrib import admin
from .models import Vehicle, VehicleDocument

# Register your models here.

class Vehicle_documentsInline(admin.TabularInline):
    model = VehicleDocument



class VehicleAdmin(admin.ModelAdmin):
    inlines = (Vehicle_documentsInline, )

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleDocument)

