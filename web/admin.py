from django.contrib import admin
from django.utils.html import format_html

from .models import Faculty, LatestNews, PrimaryMenu, SecondaryMenu, TimeTable, Attendance, Syllabus, StudentSociety, Achievement, Event, PrimaryNavigationMenu, SecondaryNavigationMenu


class FacultyAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" height="50" width="auto" />'.format(obj.profile_pic.url))

    image_tag.short_description = 'Image'

    list_display = ['full_name', 'image_tag', 'category', 'designation', 'shift', 'department', 'date_of_joining']
    list_filter = ('category', 'shift', 'department', 'designation', )

    fields = ('full_name', 'image_tag', 'profile_pic', 'category', 'designation', 'phone_number', 'email', 'shift', 'department', 'date_of_joining', 'description',)
    readonly_fields = ('image_tag',)

class LatestNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'new', 'visible', 'created_at', 'updated_at']
    list_filter = ('new', 'visible', )
    list_editable = ('new', 'visible',)

class SecondaryMenuInline(admin.TabularInline):
    model = SecondaryMenu

class PrimaryMenuAdmin(admin.ModelAdmin):
    inlines = [
        SecondaryMenuInline,
    ]
    list_display = ['name', 'order']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order',)

class PrimaryNavigationMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'link']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link',)

class SecondaryNavigationMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'link']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'shift', 'branch', 'semester', 'pdf', 'created_at', 'updated_at']
    list_filter = ('shift', 'branch', 'semester',)
    ordering = ('semester',)
    list_editable = ('pdf',)

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['branch', 'semester', 'syllabus', 'lecture_plan', 'created_at', 'updated_at']
    list_filter = ('branch', 'semester',)
    ordering = ('semester', 'branch',)
    list_editable = ('syllabus', 'lecture_plan',)

class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['title', 'shift', 'branch', 'semester', 'pdf' ,'created_at', 'updated_at']
    list_filter = ('shift', 'branch', 'semester',)
    ordering = ('semester', 'branch', 'shift')
    list_editable = ('pdf',)

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(LatestNews, LatestNewsAdmin)
admin.site.register(PrimaryMenu, PrimaryMenuAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(StudentSociety)
admin.site.register(Achievement)
admin.site.register(Event)
from .models import GeneralUpload
admin.site.register(GeneralUpload)
admin.site.register(PrimaryNavigationMenu, PrimaryNavigationMenuAdmin)
admin.site.register(SecondaryNavigationMenu, SecondaryNavigationMenuAdmin)
