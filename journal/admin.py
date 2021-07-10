from django.contrib import admin
from .models import Record, EngRec, DirRec


class EngRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'title', 'author', 'issue_category', 'text']

    list_display = ("id", "created_date", "title", "author", 'issue_category')
    search_fields = "issue_category__startswith", "id__iexact"

class DirRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'title', 'author', 'issue_category', 'text']

    list_display = ("id", "created_date", "title", "author", 'issue_category')
    search_fields = "issue_category__startswith", "id__iexact"

admin.site.register(EngRec, EngRecAdmin )
admin.site.register(DirRec, DirRecAdmin)

