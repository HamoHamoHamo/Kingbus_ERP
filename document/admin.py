from django.contrib import admin
from .models import Document, DocumentFile

class DocumentFileInline(admin.TabularInline):
    model = DocumentFile


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title','creator','pub_date')
    inlines = (DocumentFileInline, )


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentFile)