from dispatch.views import FORMAT
from django.db.models.signals import post_save, post_delete, pre_delete
from django.shortcuts import get_object_or_404
from .models import Consulting, VehicleInspectionRequest, InspectionRequestFile
from django.dispatch import receiver
import os

@receiver(post_delete, sender=VehicleInspectionRequest)
def delete_inspection_file(sender, instance, **kwargs):
    files = instance.inspection_request_file.all()
    for file in files:
        os.remove(file.file.path)
        file.delete()

@receiver(post_delete, sender=InspectionRequestFile)
def delete_inspection_file(sender, instance, **kwargs):
    os.remove(instance.file.path)
