from django.contrib import admin
from .models import Record, EngRec, DirRec


class EngRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'tags', 'report_date', 'text']

    list_display = ("id", "report_date", "author", "tags")
    search_fields = "tags__startswith", "id__iexact"

class DirRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'tags', 'report_date', 'text']

    list_display = ("id", "report_date", "author", "tags")
    search_fields = "tags__startswith", "id__iexact"


admin.site.register(EngRec, EngRecAdmin )
admin.site.register(DirRec, DirRecAdmin)

