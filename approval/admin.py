from django.contrib import admin
from .models import Approval, Approver, ApprovalFile

# Register your models here.

admin.site.register(Approval)
admin.site.register(Approver)
admin.site.register(ApprovalFile)

