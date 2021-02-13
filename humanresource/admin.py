from django.contrib import admin
from .models import Member, HR, MemberDocument

class MemberDocumentInline(admin.TabularInline):
    model = MemberDocument

class HRInline(admin.TabularInline):
    model = HR

class MemberAdmin(admin.ModelAdmin):
    inlines = (HRInline, MemberDocumentInline,)


admin.site.register(HR)
admin.site.register(MemberDocument)
admin.site.register(Member, MemberAdmin)