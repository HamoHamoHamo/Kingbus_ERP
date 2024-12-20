from django.contrib import admin
from .models import Group, OldAssignment, OldAssignmentConnect, OldAssignmentData
    

admin.site.register(Group)
admin.site.register(OldAssignment)
admin.site.register(OldAssignmentConnect)
admin.site.register(OldAssignmentData)