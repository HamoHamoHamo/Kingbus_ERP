from django.contrib import admin
from .models import Notice, NoticeFile, NoticeComment, NoticeViewCnt

class NoticeFileInline(admin.TabularInline):
    model = NoticeFile

class NoticeCommentInline(admin.TabularInline):
    model = NoticeComment

class NoticeViewCntInline(admin.TabularInline):
    model = NoticeViewCnt

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','creator','kinds','pub_date')
    inlines = (NoticeCommentInline, NoticeFileInline, NoticeViewCntInline, )


admin.site.register(Notice, NoticeAdmin)
admin.site.register(NoticeFile)
admin.site.register(NoticeComment)
admin.site.register(NoticeViewCnt)