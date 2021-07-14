from django.contrib import admin
from .models import Record, EngRec, DirRec, EngNotes, DirNotes


class EngRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'tags', 'report_date', 'text']

    list_display = ("id", "report_date", "author")
    search_fields = "tags__startswith", "id__iexact"

class DirRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'tags', 'report_date', 'text']

    list_display = ("id", "report_date", "author", "tags")
    search_fields = "tags__startswith", "id__iexact"


class EngNotesAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'message']

    list_display = ("id", 'created_date', "author")
    search_fields = "id__iexact",


class DirNotesAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'message']

    list_display = ("id", 'created_date', "author")
    search_fields = "id__iexact",


admin.site.register(EngNotes, EngNotesAdmin)
admin.site.register(DirNotes, DirNotesAdmin)
admin.site.register(EngRec, EngRecAdmin)
admin.site.register(DirRec, DirRecAdmin)

