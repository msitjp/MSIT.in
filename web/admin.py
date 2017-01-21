from django.contrib import admin
from django.utils.html import format_html

from .models import Faculty, LatestNews, PrimaryMenu, SecondaryMenu


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

class SecondaryMenuInline(admin.TabularInline):
    model = SecondaryMenu

class PrimaryMenuAdmin(admin.ModelAdmin):
    inlines = [
        SecondaryMenuInline,
    ]

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(LatestNews, LatestNewsAdmin)
admin.site.register(PrimaryMenu, PrimaryMenuAdmin)
