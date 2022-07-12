from django.contrib import admin
from .models import Member, HR, Yearly

admin.site.register(HR)
admin.site.register(Member)
admin.site.register(Yearly)