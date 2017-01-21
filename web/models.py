from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

from ckeditor.fields import RichTextField


def image_name(instance, filename):
    fname, extension = filename.split('.')
    slug = slugify(instance.full_name)
    return 'faculty/'+'%s.%s' % (slug, extension)

class Faculty(models.Model):

    SHIFTS = (
             ('M', 'Morning'),
             ('E', 'Evening'),
    )

    full_name = models.CharField(max_length=200, verbose_name='Full Name', blank=False)
    profile_pic = models.ImageField(upload_to=image_name)
    designation = models.CharField(max_length=150, verbose_name='Designation', blank=False)
    phone_number = models.CharField(max_length=10, help_text='Phone Number (without Regional Code)', verbose_name='Phone Number', blank=True, null=True)
    email = models.EmailField()
    shift = models.CharField(max_length=1, choices=SHIFTS, verbose_name='Shift', help_text='Morning or Evening')
    department = models.CharField(max_length=100, verbose_name='Department', help_text='Eg. CSE / IT / EEE')
    date_of_joining = models.DateField(null=True, blank=True, verbose_name='Date Of Joining')
    description = RichTextField(blank=True, null=True)


    def __unicode__(self):
        return "%s" % self.full_name



# DB_NAME Faculty:
#   - Id (Default)
#   - Full Name
#   - Profile Pic (Optional)
#   - Phone Number (Optional)
#   - Designation
#   - Description (Optional)
#   - Email (Optional)
#   - Subject
#   - Shift
#   - Batch
#   <b>- DateOfJoining (Optional)</b>
