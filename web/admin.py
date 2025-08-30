from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django_admin_listfilter_dropdown.filters import DropdownFilter

from .models import Faculty, LatestNews, PrimaryMenu, SecondaryMenu,\
    TimeTable, Attendance, Syllabus, StudentSociety, AICTESociety, Event,\
    PrimaryNavigationMenu, SecondaryNavigationMenu, Department, \
    DepartmentPage, Page, SocialAccount, Tab, Notice, Marquee, UserDepartment, AchievementCategory, AchievementTab

# FIELDS = ('first_name', 'last_name', 'email', 'username', 'password',
#             'dept', 'is_active', 'is_staff', 'is_superuser',
#             'permissions', 'groups',)

# All admin class definitions first
class FacultyAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" height="50" width="auto" />'
                               .format(obj.profile_pic.url))
        except:
            return None

    image_tag.short_description = 'Image'

    list_display = ['title', 'full_name', 'image_tag', 'category', 'designation',
                    'shift', 'department', 'order', 'date_of_joining']
    list_display_links = ('full_name',)
    ordering = ('full_name',)
    list_filter = ('category', 'shift', 'department', 'designation',)
    list_editable = ('order', )

    fields = ('title', 'full_name', 'qualifications', 'image_tag', 'profile_pic', 'order', 'category',
              'designation', 'phone_number', 'email', 'shift', 'department',
              'date_of_joining', 'experience', 'description',)
    readonly_fields = ('image_tag',)
    search_fields = ['full_name']

    def get_queryset(self, request):
        qs = super(FacultyAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
            return qs.filter(department=u.department, shift=u.shift)

class LatestNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'new', 'visible', 'created_at', 'updated_at']
    list_filter = ('new', 'visible', )
    list_editable = ('new', 'visible',)
    search_fields = ['title']
    fields = ('title', 'link', 'files', 'new', 'visible', 'additional_title', 'additional_link', 'additional_files')

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'new', 'visible', 'created_at', 'updated_at']
    list_filter = ('new', 'visible', )
    list_editable = ('new', 'visible',)
    search_fields = ['title']
    fields = ('title', 'link', 'files', 'new', 'visible', 'additional_title', 'additional_link', 'additional_files')

class SecondaryMenuInline(admin.TabularInline):
    model = SecondaryMenu

class PrimaryMenuAdmin(admin.ModelAdmin):
    inlines = [SecondaryMenuInline]
    list_display = ['name', 'order']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order',)
    search_fields = ['name']

class PrimaryNavigationMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'link', 'files']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link', 'files',)
    search_fields = ['title']

class SecondaryNavigationMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'link', 'files']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link', 'files',)
    search_fields = ['title']

class MarqueeAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'link', 'files']
    list_filter = ('order',)
    ordering = ('order',)
    list_editable = ('order', 'link', 'files',)
    search_fields = ['title']

class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['title', 'shift', 'department',
                    'semester', 'pdf', 'created_at', 'updated_at']
    list_filter = ('shift', 'department', 'semester',)
    ordering = ('semester', 'department', 'shift')
    list_editable = ('pdf',)
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(TimeTableAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
            return qs.filter(department=u.department, shift=u.shift)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'shift', 'department',
                    'semester', 'pdf', 'created_at', 'updated_at']
    list_filter = ('shift', 'department', 'semester',)
    ordering = ('semester',)
    list_editable = ('pdf',)
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(AttendanceAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
            return qs.filter(department=u.department, shift=u.shift)

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'semester',
                    'syllabus', 'lecture_plan', 'created_at', 'updated_at']
    list_filter = ('department', 'semester',)
    ordering = ('semester', 'department',)
    list_editable = ('syllabus', 'lecture_plan',)
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(SyllabusAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
            return qs.filter(department=u.department)

class SocietyAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at', 'updated_at']
    list_filter = ('order', )
    ordering = ('order', )
    list_editable = ('order', )
    search_fields = ['name']

class AICTEAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at', 'updated_at']
    list_filter = ('order', )
    ordering = ('order', )
    list_editable = ('order', )
    search_fields = ['name']

class AchievementTabInline(admin.TabularInline):
    model = AchievementTab
    extra = 1
    fields = ('title', 'order', 'content')
    ordering = ('order',)

class AchievementCategoryAdmin(admin.ModelAdmin):
    inlines = [AchievementTabInline]
    list_display = ['name', 'display_achievements', 'order', 'created_at', 'updated_at']
    ordering = ('order',)
    list_editable = ('display_achievements', 'order',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    ordering = ('-date',)
    search_fields = ['title']

class DepartmentPageInline(admin.TabularInline):
    model = DepartmentPage

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [DepartmentPageInline]
    list_display = ['department', 'display_1st_faculty', 'display_2nd_faculty', 'display_assistant',
                    'sort_faculty', 'sorting_order']
    ordering = ('department',)
    list_editable = ('display_1st_faculty', 'display_2nd_faculty', 'display_assistant',
                     'sort_faculty', 'sorting_order',)

    def get_queryset(self, request):
        qs = super(DepartmentAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
            return qs.filter(department=u.department)

class TabInline(admin.TabularInline):
    model = Tab

class PageAdmin(admin.ModelAdmin):
    inlines = [TabInline]
    list_display = ['title', 'link', 'updated_at', 'created_at']
    ordering = ('-created_at', '-updated_at')
    search_fields = ['title']

class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'visible', 'icon', 'link']
    ordering = ('order', )
    list_editable = ('order', 'visible', 'link', 'icon', )

class UserDepartmentInline(admin.StackedInline):
    model = UserDepartment
    can_delete = False
    verbose_name_plural = 'User Departments'
    verbose_name = 'User Departments'

class UserAdmin(BaseUserAdmin):
    inlines = (UserDepartmentInline, )

# All model registrations after class definitions
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(LatestNews, LatestNewsAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(PrimaryMenu, PrimaryMenuAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(StudentSociety, SocietyAdmin)
admin.site.register(AICTESociety, AICTEAdmin)
admin.site.register(AchievementCategory, AchievementCategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PrimaryNavigationMenu, PrimaryNavigationMenuAdmin)
admin.site.register(SecondaryNavigationMenu, SecondaryNavigationMenuAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Marquee, MarqueeAdmin)

# User admin customization
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
