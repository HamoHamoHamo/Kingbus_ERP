from django.contrib import admin
from .models import User, UserFiles

class UserFilesInline(admin.TabularInline):
    model = UserFiles

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','userid','registered_dttm')
    inlines = (UserFilesInline,)


admin.site.register(User, UserAdmin)
admin.site.register(UserFiles)