from __future__ import unicode_literals

import os
from functools import partial

from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import now

from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.hashers import make_password
from web.get_username import current_request
# import .get_username
# from .get_username import *
from multiselectfield import MultiSelectField

from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from fontawesome.fields import IconField


# Option fields
TITLES = (
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'),
    ('Sh.', 'Sh.'),
    ('Ms.', 'Ms.'),
    ('Miss', 'Miss'),
    ('Master', 'Master'),
    ('Dr.', 'Dr.'),
    ('Prof.', 'Prof.'),
)

DESIGNATIONS = (
    ('1HOD', 'HOD'),
    ('2Professor', 'Professor'),
    ('3Associate Professor', 'Associate Professor'),
    ('4Reader', 'Reader'),
    ('5Assistant Professor', 'Assistant Professor'),
    ('6Lab. Assistant', 'Lab. Assistant'),
    ('7Tech. Assistant', 'Tech. Assistant'),
    ('8Programmer', 'Programmer'),
    ('9Instructor', 'Instructor'),
)

DEPARTMENT = (
    ('CSE', 'CSE'),
    ('IT', 'IT'),
    ('ECE', 'ECE'),
    ('EEE', 'EEE'),
    ('APPLIED SCIENCES', 'Applied Sciences'),
)

Extended_DEPARTMENT = (('All', 'All'),) + DEPARTMENT

SHIFTS = (
         ('M', 'Morning'),
         ('E', 'Evening'),
)

SEMESTERS = (
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV'),
    ('5', 'V'),
    ('6', 'VI'),
    ('7', 'VII'),
    ('8', 'VIII'),
)

CATEGORY = (
    ('teaching', "Teaching Faculty"),
    ('assistant', "Lab Assistant"),
)

SORTING = (
    ('1', 'Name wise'),
    ('2', 'Designation wise'),
    ('3', 'Date-of-joining wise'),
    ('4', 'Custom Order Specified'),
)

ORDER = (
    ('1', 'Ascending'),
    ('2', 'Descending'),
)

PERMISSIONS = (
    ('faculty', 'Faculty'),
    ('department', 'Department'),
    ('latest news', 'Latest News'),
    ('notice', 'Notice & Circular'),
    ('achievement', 'Achievement'),
    ('Attendaccnce', 'Attendance'),
    ('Event', 'Event'),
    ('Sliding Text', 'Sliding Text'),
    ('All Other', 'Pages'),
    ('Menu - Left', 'Menu - Left'),
    ('Menu - Top', 'Menu - Top'),
    ('Menu - Secondary', 'Menu - Secondary'),
    ('Society', 'Society'),
    ('AICTE', 'AICTE'),
    ('Syllabus', 'Syllabus'),
    ('Time Table', 'Time Table'),
)


def wrapper(instance, filename, field, folder):
    extension = filename.split('.')[-1]
    slug = os.path.join(folder, slugify(getattr(instance, field)))
    return '%s.%s' % (slug, extension)


def image_name(field='title', folder='general'):
    return partial(wrapper, field=field, folder=folder)


class PrimaryNavigationMenu(models.Model):
    title = models.CharField(verbose_name="Link Title",
                             max_length=50, help_text='Text to show in the Navigation')
    link = models.CharField(
        max_length=1000, help_text='Link to redirect to', blank=True, null=True)
    files = models.FileField(upload_to=image_name(
        'title', 'navigations'), blank=True, null=True)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.title

    def clean(self):
        super(PrimaryNavigationMenu, self).clean()
        # Treat both empty string and None as "no value" for validation purposes
        has_link = bool(self.link)
        has_file = bool(self.files)
        if not has_link and not has_file:
            raise ValidationError(
                "Navigation menu must have either a link to redirect or a file attached to it")
        if has_link and has_file:
            raise ValidationError(
                "Please enter either a link to redirect or a file to attach with the Menu item.")
        return self

    def save(self, *args, **kwargs):
        self.full_clean()
        super(PrimaryNavigationMenu, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Menu - Top'
        verbose_name_plural = 'Menu - Top'


class SecondaryNavigationMenu(models.Model):
    title = models.CharField(verbose_name="Link Title",
                             max_length=50, help_text='Text to show in the Navigation')
    link = models.CharField(
        max_length=1000, help_text='Link to redirect to', blank=True, null=True)
    files = models.FileField(upload_to=image_name(
        'title', 'navigations'), blank=True, null=True)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.title

    def clean(self):
        super(SecondaryNavigationMenu, self).clean()
        # Treat both empty string and None as "no value" for validation purposes
        has_link = bool(self.link)
        has_file = bool(self.files)
        if not has_link and not has_file:
            raise ValidationError(
                "Navigation menu must have either a link to redirect or a file attached to it")
        if has_link and has_file:
            raise ValidationError(
                "Please enter either a link to redirect or a file to attach with the Menu item.")
        return self

    def save(self, *args, **kwargs):
        self.full_clean()
        super(SecondaryNavigationMenu, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Menu - Secondary'
        verbose_name_plural = 'Menu - Secondary'


class Faculty(models.Model):
    title = models.CharField(
        max_length=10, choices=TITLES, default=1, blank=False)
    full_name = models.CharField(
        max_length=200, verbose_name='Full Name', blank=False)
    qualifications = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=1)
    profile_pic = models.ImageField(upload_to=image_name(
        'full_name', 'faculty'), blank=True, null=True)
    category = models.CharField(
        max_length=30, choices=CATEGORY, default='teaching')
    designation = models.CharField(
        max_length=30, choices=DESIGNATIONS, blank=False)
    phone_number = models.CharField(
        max_length=10, help_text='Phone Number (without Regional Code)', verbose_name='Phone Number', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    shift = models.CharField(max_length=1, choices=SHIFTS, default='M',
                             verbose_name='Shift', help_text='Morning or Evening')
    department = models.CharField(
        max_length=30, choices=DEPARTMENT, blank=True, null=True)
    date_of_joining = models.DateField(
        null=True, blank=True, verbose_name='Date Of Joining')
    experience = models.CharField(
    max_length=200, verbose_name='Experience', blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def clean(self):
        super(Faculty, self).clean()
        req = current_request()
        try:
            logged_user = req.user.userdepartment
            if ((str(self.department) == logged_user.department) and (str(self.shift) == logged_user.shift)) or logged_user.department == 'All':
                return self
            else:
                raise ValidationError(
                "You don't have access to change this Database")

        except:
            raise ValidationError(
            "You don't have access to change this Database")


    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return "%s %s" % (self.title, self.full_name)


class LatestNews(models.Model):
    title = models.CharField(max_length=250, help_text='Text to display')
    link = models.CharField(
        max_length=1000, help_text='Link for the News', blank=True, null=True)
    files = models.FileField(upload_to=image_name(
        'title', 'news'), blank=True, null=True)
    new = models.BooleanField(
        default=True, help_text='This places a New Flag on th link')
    visible = models.BooleanField(
        default=True, help_text='Whether the News is Visible on Main Page')
    additional_title = models.CharField(
        max_length=50, help_text='Additional Link Title (if any)', blank=True, null=True)
    additional_link = models.CharField(
        max_length=1000, help_text='Additional Link (if any)', blank=True, null=True)
    additional_files = models.FileField(
        upload_to=image_name('title', 'news'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Right - Latest News'
        verbose_name_plural = 'Right - Latest News'

    def __str__(self):
        return "%s" % self.title

    def clean(self):
        super(LatestNews, self).clean()
        if not self.link and not self.files:
            raise ValidationError(
                "Latest News must have either a link to redirect or a file attached to it")
        elif self.link and self.files:
            raise ValidationError(
                "Please enter either a link to redirect or a file to attach with the News item.")
        else:
            if not self.additional_title:
                return self
            if not self.additional_link and not self.additional_files:
                raise ValidationError(
                    "Additional Title must have either a link to redirect or a file attached to it")
            elif self.additional_link and self.additional_files:
                raise ValidationError(
                    "Please enter either a link to redirect or a file to attach with the Additional Title.")
            else:
                return self

    def save(self, *args, **kwargs):
        self.full_clean()
        super(LatestNews, self).save(*args, **kwargs)


class Notice(models.Model):
    title = models.CharField(max_length=250, help_text='Text to display')
    link = models.CharField(
        max_length=1000, help_text='Link for the Notice', blank=True, null=True)
    files = models.FileField(upload_to=image_name(
        'title', 'notices'), blank=True, null=True)
    new = models.BooleanField(
        default=True, help_text='This places a New Flag on th link')
    visible = models.BooleanField(
        default=True, help_text='Whether the News is Visible on Main Page')
    additional_title = models.CharField(
        max_length=50, help_text='Additional Link Title (if any)', blank=True, null=True)
    additional_link = models.CharField(
        max_length=1000, help_text='Additional Link (if any)', blank=True, null=True)
    additional_files = models.FileField(upload_to=image_name(
        'title', 'notices'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Right - Notice'
        verbose_name_plural = 'Right - Notices'

    def __str__(self):
        return "%s" % self.title

    def clean(self):
        super(Notice, self).clean()
        if not self.link and not self.files:
            raise ValidationError(
                "A Notice must have either a link to redirect or a file attached to it")
        elif self.link and self.files:
            raise ValidationError(
                "Please enter either a link to redirect or a file to attach with the Notice.")
        else:
            if not self.additional_title:
                return self
            if not self.additional_link and not self.additional_files:
                raise ValidationError(
                    "Additional Title must have either a link to redirect or a file attached to it")
            elif self.additional_link and self.additional_files:
                raise ValidationError(
                    "Please enter either a link to redirect or a file to attach with the Additional Title.")
            else:
                return self

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Notice, self).save(*args, **kwargs)


class PrimaryMenu(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Menu - Left'
        verbose_name_plural = 'Menu - Left'


class SecondaryMenu(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(PrimaryMenu, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    link = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Menu - Secondary'
        verbose_name_plural = 'Menu - Secondary'

    def __str__(self):
        return f"{self.parent} > {self.name}"


class TimeTable(models.Model):
    title = models.CharField(max_length=50, help_text='Batch Name')
    department = models.CharField(
        max_length=30, help_text='Department Name', choices=DEPARTMENT, blank=True, null=True)
    shift = models.CharField(max_length=1, choices=SHIFTS)
    semester = models.CharField(
        max_length=1, choices=SEMESTERS, blank=True, null=True)
    pdf = models.FileField(upload_to=image_name("title", 'timetable'))
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = 'Content - Time Table'
        verbose_name_plural = 'Content - Time Tables'

    def clean(self):
        super(TimeTable, self).clean()
        req = current_request()
        try:
            logged_user = req.user.userdepartment
            if (((str(self.department) == logged_user.department) and (str(self.shift) == logged_user.shift))) or logged_user.department == 'All':
                return self
            else:
                raise ValidationError(
                "You don't have access to change this Database")

        except:
            raise ValidationError(
            "You don't have access to change this Database")


class Attendance(models.Model):
    title = models.CharField(max_length=50, help_text='Batch Name')
    department = models.CharField(
        max_length=30, help_text='Department Name', choices=DEPARTMENT, blank=True, null=True)
    shift = models.CharField(max_length=1, choices=SHIFTS)
    semester = models.CharField(
        max_length=1, choices=SEMESTERS, blank=True, null=True)
    pdf = models.FileField(upload_to=image_name("title", "attendance"))
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = 'Content - Attendance'
        verbose_name_plural = 'Content - Attendance'

    def clean(self):
        super(Attendance, self).clean()
        req = current_request()
        try:
            logged_user = req.user.userdepartment
            if (((str(self.department) == logged_user.department) and (str(self.shift) == logged_user.shift))) or logged_user.department == 'All':
                return self
            else:
                raise ValidationError(
                "You don't have access to change this Database")

        except:
            raise ValidationError(
            "You don't have access to change this Database")


class Syllabus(models.Model):
    title = models.CharField(max_length=100, help_text='text to display')
    department = models.CharField(
        max_length=30, help_text='Department Name', choices=DEPARTMENT, blank=True, null=True)
    semester = models.CharField(
        max_length=1, choices=SEMESTERS, blank=True, null=True)
    syllabus = models.FileField(upload_to=image_name("title", "syllabus"), blank=True, null=True)
    lecture_plan = models.FileField(upload_to=image_name("title", "lecture_plan"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = 'Content - Syllabus'
        verbose_name_plural = 'Content - Syllabus'

    def clean(self):
        super(Syllabus, self).clean()
        req = current_request()
        try:
            if str(self.department) == req.user.userdepartment.department or req.user.userdepartment.department == 'All':
                return self
            else:
                raise ValidationError(
                "You don't have access to change this Database")

        except:
            raise ValidationError(
            "You don't have access to change this Database")


class StudentSociety(models.Model):
    name = models.CharField(max_length=50, help_text='Society Name')
    description = RichTextUploadingField()
    order = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Page - Society'
        verbose_name_plural = 'Page - Societies'


class AICTESociety(models.Model):
    name = models.CharField(max_length=50, help_text='Society Name')
    description = RichTextUploadingField()
    order = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Page - AICTE Society'
        verbose_name_plural = 'Page - AICTE Societies'


class AchievementCategory(models.Model):
    name = models.CharField(max_length=100, help_text='Category Name (e.g. Cultural, Sports)')
    slug = models.SlugField(unique=True, help_text='URL-friendly version of the name', blank=True)
    order = models.PositiveIntegerField(default=1, help_text='Display order of the category')
    display_achievements = models.BooleanField(default=True, help_text='Whether to display this category')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(AchievementCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Right - Achievement Category'
        verbose_name_plural = 'Right - Achievement Categories'
        ordering = ['order']

    def __str__(self):
        return self.name


class AchievementTab(models.Model):
    category = models.ForeignKey(AchievementCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    order = models.PositiveIntegerField(default=1, help_text='Display order of the tab')
    content = RichTextUploadingField(config_name='default')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Achievement Tab'
        verbose_name_plural = 'Achievement Tabs'
        ordering = ['category', 'order']

    def __str__(self):
        return "%s - %s" % (self.category.name, self.title)


class Event(models.Model):
    title = models.CharField(max_length=50, help_text='Tab Name')
    date = models.DateField(default=now)
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = 'Page - Event'
        verbose_name_plural = 'Page - Events'


class Department(models.Model):
    department = models.CharField(max_length=30, help_text='Department Name', choices=DEPARTMENT, default='CSE',
                                  unique=True)
    display_1st_faculty = models.BooleanField(verbose_name='Display 1st shift Faculty',
                                              help_text='Check if the list of faculties is to be displayed on the website', default=True)
    display_assistant = models.BooleanField(verbose_name='Display Lab Assistants',
                                                help_text='Check if the list of Lab Assistants is to be displayed on the website', default=False)
    display_2nd_faculty = models.BooleanField(verbose_name='Display 2nd shift Faculty',
                                              help_text='Check if the list of faculties is to be displayed on the website', default=True)
    # display_2nd_assistant = models.BooleanField(verbose_name='Display 2nd shift Lab Assistants',
    #                                             help_text='Check if the list of Lab Assistants is to be displayed on the website', default=False)
    sort_faculty = models.CharField(verbose_name='Faculty Sorting Criteria', max_length=1,
                                    choices=SORTING, default='1')
    sorting_order = models.CharField(verbose_name='Faculty Sorting Order', max_length=1,
                                     choices=ORDER, default='2')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def clean(self):
        super(Department, self).clean()
        req = current_request()
        try:
            if str(self.department) == req.user.userdepartment.department or req.user.userdepartment.department == 'All':
                return self
            else:
                raise ValidationError(
                "You don't have access to change this Database")

        except:
            raise ValidationError(
            "You don't have access to change this Database")



    def __str__(self):
        return "%s" % self.department


class DepartmentPage(models.Model):
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    order = models.PositiveIntegerField()
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.department_name} - {self.title}"

    def clean(self):
        super(DepartmentPage, self).clean()
        req = current_request()
        try:
            if str(self.department_name) == req.user.userdepartment.department or req.user.userdepartment.department == 'All':
                return self
            else:
                raise ValidationError(
                "You don't have access to change this Database")

        except:
            raise ValidationError(
            "You don't have access to change this Database")


class Page(models.Model):
    title = models.CharField(max_length=70)
    link = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = 'Page - All Other'
        verbose_name_plural = 'Page - All Others'


class Tab(models.Model):
    title = models.CharField(max_length=70)
    parent = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.parent.title} > {self.title}"


class Marquee(models.Model):
    title = models.CharField(verbose_name="Link Title",
                             max_length=200, help_text='Text to show in the Marquee')
    link = models.CharField(
        max_length=1000, help_text='Link to redirect to', blank=True, null=True)
    files = models.FileField(upload_to=image_name(
        'title', 'marquee'), blank=True, null=True)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Sliding Text'
        verbose_name_plural = 'Sliding Text'

    def __str__(self):
        return "%s" % self.title

    def clean(self):
        super(Marquee, self).clean()
        if str(self.link) == "" and str(self.files) == "":
            raise ValidationError(
                "Navigation menu must have either a link to redirect or a file attached to it")
        elif str(self.link) != "" and str(self.files) != "":
            raise ValidationError(
                "Please enter either a link to redirect or a file to attach with the Menu item.")
        else:
            return self


class UserDepartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User Department')
    department = models.CharField(verbose_name='Department', choices=Extended_DEPARTMENT, max_length=20)
    shift = models.CharField(verbose_name='Shift', choices=SHIFTS, max_length=10, default='M')

    class Meta:
        verbose_name = 'User Department'
        verbose_name_plural = 'User Departments'

    def __str__(self):
        return f"{self.user.username} - {self.department}"


class SocialAccount(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField()
    visible = models.BooleanField(default=True)
    icon = IconField()
    link = models.URLField(blank=True)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = 'Social Account Links'
        verbose_name_plural = 'Social Account Links'
