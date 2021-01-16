from django.contrib import admin
from .models import Notice, NoticeFile, NoticeComment

class NoticeFileInline(admin.TabularInline):
    model = NoticeFile

class NoticeCommentInline(admin.TabularInline):
    model = NoticeComment

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','creator','kinds','registered_dttm')
    inlines = (NoticeCommentInline, NoticeFileInline, )


admin.site.register(Notice, NoticeAdmin)
admin.site.register(NoticeFile)
admin.site.register(NoticeComment)