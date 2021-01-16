from django.contrib import admin
from .models import User, UserFile

class UserFilesInline(admin.TabularInline):
    model = UserFile

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','userid','registered_dttm')
    inlines = (UserFilesInline,)


admin.site.register(User, UserAdmin)
admin.site.register(UserFile)