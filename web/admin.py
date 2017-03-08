from django.contrib import admin
from django.utils.html import format_html

from .models import Faculty, LatestNews, PrimaryMenu, SecondaryMenu,\
    TimeTable, Attendance, Syllabus, StudentSociety, Achievement, Event,\
    PrimaryNavigationMenu, SecondaryNavigationMenu, Department, \
    DepartmentPage, Page, Tab, Notice, Marquee


class FacultyAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" height="50" width="auto" />'
                               .format(obj.profile_pic.url))
        except:
            return None

    image_tag.short_description = 'Image'

    list_display = ['full_name', 'image_tag', 'category', 'designation',
                    'shift', 'department', 'date_of_joining']
    list_filter = ('category', 'shift', 'department', 'designation', )

    fields = ('title', 'full_name', 'qualifications', 'image_tag', 'profile_pic', 'category',
              'designation', 'phone_number', 'email', 'shift', 'department',
              'date_of_joining', 'description',)
    readonly_fields = ('image_tag',)


class LatestNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'new', 'visible', 'created_at', 'updated_at']
    list_filter = ('new', 'visible', )
    list_editable = ('new', 'visible',)


class NoticeAdmin(admin.ModelAdmin):
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
    list_display = ['title', 'order', 'link', 'files']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link', 'files',)


class SecondaryNavigationMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'link', 'files']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link', 'files',)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'shift', 'department',
                    'semester', 'pdf', 'created_at', 'updated_at']
    list_filter = ('shift', 'department', 'semester',)
    ordering = ('semester',)
    list_editable = ('pdf',)


class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'semester',
                    'syllabus', 'lecture_plan', 'created_at', 'updated_at']
    list_filter = ('department', 'semester',)
    ordering = ('semester', 'department',)
    list_editable = ('syllabus', 'lecture_plan',)


class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['title', 'shift', 'department',
                    'semester', 'pdf', 'created_at', 'updated_at']
    list_filter = ('shift', 'department', 'semester',)
    ordering = ('semester', 'department', 'shift')
    list_editable = ('pdf',)


class DepartmentPageInline(admin.TabularInline):
    model = DepartmentPage


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [
        DepartmentPageInline
    ]
    list_display = ['department', 'display_1st_faculty', 'display_2nd_faculty', 'display_1st_assistant',
                    'display_2nd_assistant', 'sort_faculty', 'sorting_order']
    ordering = ('department',)
    list_editable = ('display_1st_faculty', 'display_2nd_faculty', 'display_1st_assistant',
                     'display_2nd_assistant', 'sort_faculty', 'sorting_order',)


class TabInline(admin.TabularInline):
    model = Tab


class PageAdmin(admin.ModelAdmin):
    inlines = [
        TabInline
    ]
    list_display = ['title', 'link', 'updated_at', 'created_at']
    ordering = ('-created_at', '-updated_at')


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(LatestNews, LatestNewsAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(PrimaryMenu, PrimaryMenuAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(StudentSociety)
admin.site.register(Achievement)
admin.site.register(Event)
admin.site.register(PrimaryNavigationMenu, PrimaryNavigationMenuAdmin)
admin.site.register(SecondaryNavigationMenu, SecondaryNavigationMenuAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Marquee)
