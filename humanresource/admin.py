from django.contrib import admin
from .models import Member, HR


class HRInline(admin.TabularInline):
    model = HR

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = (HRInline, )

class HRAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id')

admin.site.register(HR, HRAdmin)

admin.site.register(Member, MemberAdmin)