from django.contrib import admin
from .models import Group, Assignment, AssignmentConnect, AssignmentData
    

admin.site.register(Group)
admin.site.register(Assignment)
admin.site.register(AssignmentConnect)
admin.site.register(AssignmentData)