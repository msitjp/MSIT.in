from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


def image_name(instance, filename):
    fname, extension = filename.split('.')
    slug = ''
    try:
        slug = 'faculty/' + slugify(instance.full_name)
    except:
        pass
    try:
        slug = 'general/' + slugify(instance.filename)
    except:
        pass
    try:
        slug = 'time-tables-and-Attendance/' + slugify(instance.title)
    except:
        pass
    if slug == '':
        slug = slugify(filename)
    return '%s.%s' % (slug, extension)

class Faculty(models.Model):

    SHIFTS = (
         ('M', 'Morning'),
         ('E', 'Evening'),
    )

    CATEGORY = (
        ('administration', 'Administration'),
        ('office', 'Office Staff'),
        ('accounts', "Accounts"),
        ('library', "Library Staff"),
        ('placement', "Placement Staff"),
        ('teaching', "Teaching Faculty"),
    )
    DEPARTMENT = (
        ('1', 'CSE'),
        ('2', 'IT'),
        ('3', 'ECE'),
        ('4', 'EEE'),
        ('5', 'Applied Science'),
    )
    full_name = models.CharField(max_length=200, verbose_name='Full Name', blank=False)
    profile_pic = models.ImageField(upload_to=image_name, blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY, default='teaching')
    designation = models.CharField(max_length=150, verbose_name='Designation', blank=False)
    phone_number = models.CharField(max_length=10, help_text='Phone Number (without Regional Code)', verbose_name='Phone Number', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    shift = models.CharField(max_length=1, choices=SHIFTS, default='M', verbose_name='Shift', help_text='Morning or Evening')
    department = models.CharField(max_length=1, choices=DEPARTMENT, blank=True, null=True)
    date_of_joining = models.DateField(null=True, blank=True, verbose_name='Date Of Joining')
    description = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __unicode__(self):
        return "%s" % self.full_name

class LatestNews(models.Model):
    title = models.CharField(max_length=250, help_text='Text to display')
    link = models.CharField(max_length=1000, help_text='Link for the News')
    new = models.BooleanField(default=True, help_text='This places a New Flag on th link')
    visible = models.BooleanField(default=True, help_text='Whether the News is Visible on Main Page')
    additional_title = models.CharField(max_length=50, help_text='Additional Link Title (if any)', blank=True, null=True)
    additional_link = models.CharField(max_length=1000, help_text='Additional Link (if any)', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Latest News'
        verbose_name_plural = 'Latest News'

    def __unicode__(self):
        return "%s" % self.title

class PrimaryMenu(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Primary Menu'
        verbose_name_plural = 'Primary Menus'

    def __unicode__(self):
        return "%s"  % self.name


class SecondaryMenu(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(PrimaryMenu, on_delete=models.CASCADE)
    link = models.CharField(max_length=1000)
    order = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Secondary Menu'
        verbose_name_plural = 'Secondary Menus'

    def __unicode__(self):
        return "%s > %s"  % (self.parent, self.name)

class TimeTable(models.Model):
    SHIFTS = (
         ('M', 'Morning'),
         ('E', 'Evening'),
    )
    BRANCH = (
        ('1', 'CSE'),
        ('2', 'IT'),
        ('3', 'ECE'),
        ('4', 'EEE'),
        ('5', 'Applied Sciences'),
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
    title = models.CharField(max_length=50, help_text='Batch Name')
    branch = models.CharField(max_length=1, help_text='Branch Name', choices=BRANCH, blank=True, null=True)
    shift = models.CharField(max_length=1, choices=SHIFTS)
    semester = models.CharField(max_length=1, choices=SEMESTERS, blank=True, null=True)
    pdf = models.FileField(upload_to=image_name)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.title)

class Attendance(models.Model):
    SHIFTS = (
         ('M', 'Morning'),
         ('E', 'Evening'),
    )
    BRANCH = (
        ('1', 'CSE'),
        ('2', 'IT'),
        ('3', 'ECE'),
        ('4', 'EEE'),
        ('5', 'Applied Sciences'),
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
    title = models.CharField(max_length=50, help_text='Batch Name')
    shift = models.CharField(max_length=1, choices=SHIFTS)
    branch = models.CharField(max_length=1, help_text='Branch Name', choices=BRANCH, blank=True, null=True)
    semester = models.CharField(max_length=1, choices=SEMESTERS, blank=True, null=True)
    pdf = models.FileField(upload_to=image_name)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.title)

class Syllabus(models.Model):
    BRANCH = (
        ('1', 'CSE'),
        ('2', 'IT'),
        ('3', 'ECE'),
        ('4', 'EEE'),
        ('5', 'Applied Sciences'),
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
    title = models.CharField(max_length=100, help_text='text to display')
    branch = models.CharField(max_length=1, help_text='Branch Name', choices=BRANCH)
    semester = models.CharField(max_length=1, choices=SEMESTERS, blank=True, null=True)
    syllabus = models.FileField(upload_to=image_name)
    lecture_plan = models.FileField(upload_to=image_name)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.title)

class StudentSociety(models.Model):
    name = models.CharField(max_length=50, help_text='Society Name')
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.name)

class Achievement(models.Model):
    title = models.CharField(max_length=50, help_text='Tab Name')
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.title)

class Event(models.Model):
    title = models.CharField(max_length=50, help_text='Tab Name')
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.title)

class GeneralUpload(models.Model):
    filename = models.CharField(max_length=100, help_text='Eg: Campus Ground')
    files = models.FileField(upload_to=image_name)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s"  % (self.filename)

class PrimaryNavigationMenu(models.Model):
    title = models.CharField(max_length=50, help_text='Text to show in the Navigation')
    link = models.CharField(max_length=1000, help_text = 'Link to redirect to')
    order = models.PositiveIntegerField(default=1, blank=True)

    def __unicode__(self):
        return "%s" % self.title

class SecondaryNavigationMenu(models.Model):
    title = models.CharField(max_length=50, help_text='Text to show in the Navigation')
    link = models.CharField(max_length=1000, help_text = 'Link to redirect to')
    order = models.PositiveIntegerField(default=1, blank=True)

    def __unicode__(self):
        return "%s" % self.title
