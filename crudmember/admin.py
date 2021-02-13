from django.contrib import admin
from .models import User, UserFile, UserIP

class UserFilesInline(admin.TabularInline):
    model = UserFile

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','userid','registered_dttm')
    inlines = (UserFilesInline,)

class UserIPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'pub_date')
    


admin.site.register(User, UserAdmin)
admin.site.register(UserFile)
admin.site.register(UserIP, UserIPAdmin)