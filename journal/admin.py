from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Record, Comments, Department, Notes, Objectives, ObjectivesDone, ObjectivesStatus, ScheduledTasks


"""class ImagesInline(admin.TabularInline):
    model = Images


class EngRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'tags', 'report_date', 'text', 'preview']

    list_filter = ('author', 'tags')

    readonly_fields = ["preview"]

    inlines = [ImagesInline]

    list_display = ("id", "report_date", "tags", "author")
    search_fields = "tags__istartswith", "id__iexact"

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}"height="200">')
    preview.short_description = 'Изображения'


class DirRecAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'tags', 'report_date', 'text']

    list_filter = ('author', 'tags')

    list_display = ("id", "report_date", "tags", "author")
    search_fields = "tags__istartswith", "id__iexact"


class EngNotesAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'message']

    list_display = ("id", 'created_date', "author")
    search_fields = "id__iexact",


class DirNotesAdmin(admin.ModelAdmin):

    fields = ['created_date', 'author', 'message']

    list_display = ("id", 'created_date', "author")
    search_fields = "id__iexact","""


class AdminRecords(admin.ModelAdmin):

    fields = ['created_date', 'author', 'message']

    list_filter = ('author', 'tags')

    search_fields = "id__iexact",


class AdminObjectives(admin.ModelAdmin):

    fields = ['created_date', 'author', 'name']

    list_filter = ('author', 'name')


"""admin.site.register(EngNotes, EngNotesAdmin)
admin.site.register(DirNotes, DirNotesAdmin)
admin.site.register(EngRec, EngRecAdmin)
admin.site.register(DirRec, DirRecAdmin)
admin.site.register(Images)"""
admin.site.register(Comments)
admin.site.register(Record)
admin.site.register(Department)
admin.site.register(Notes)
admin.site.register(Objectives, AdminObjectives)
admin.site.register(ObjectivesDone)
admin.site.register(ObjectivesStatus)
admin.site.register(ScheduledTasks)


