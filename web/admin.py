from django.contrib import admin
from django.utils.html import format_html

from .models import Faculty


class FacultyAdmin(admin.ModelAdmin):
    verbose_name = 'Faculty'
    verbose_name_plural = 'Faculties'

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.profile_pic.url))

    image_tag.short_description = 'Image'

    list_display = ['full_name', 'image_tag', 'designation', 'shift', 'department', 'date_of_joining']
    fields = ('full_name', 'image_tag', 'profile_pic', 'designation', 'phone_number', 'email', 'shift', 'department', 'date_of_joining', 'description',)
    readonly_fields = ('image_tag',)

admin.site.register(Faculty, FacultyAdmin)
