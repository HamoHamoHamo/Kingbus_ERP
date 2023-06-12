from django.contrib import admin
from .models import Consulting, VehicleInspectionRequest, InspectionRequestFile, ConsultingFile

admin.site.register(Consulting)
admin.site.register(VehicleInspectionRequest)
admin.site.register(InspectionRequestFile)
admin.site.register(ConsultingFile)