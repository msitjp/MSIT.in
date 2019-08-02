# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from datetime import date


from django import forms
from django.core.exceptions import ValidationError
from django.db import models

from web.models import Faculty
from web.get_username import current_request
from django.core.validators import RegexValidator
from .utils.widgets import MonthYearWidget

NATION = (
  ('International', 'International'),
  ('National', 'National'),
)

PAPER_TYPE = (
  ('Conference', 'Conference'),
  ('Journal', 'Journal'),
)

INDEXING_TYPE = (
  ('SCI/SCIE', 'SCI/SCIE'),
  ('Scopus', 'Scopus'),
  ('Google Scholars', 'Google Scholars'),
  ('Not Applicable', 'Not Applicable'),
  ('Others', 'Others'),
)

class BookRecord(models.Model):
  title = models.CharField(verbose_name="Title/Topic", max_length=300, blank=False)
  faculty = models.ForeignKey(Faculty, default=1)
  count = models.CharField(verbose_name="Total Count",
                           max_length=3, blank=True, null=True)
  type = models.CharField(verbose_name="International/National", max_length=15, blank=False, choices=NATION, default=NATION[0][0])
  publisher = models.CharField(
      verbose_name="Publisher", max_length=200, blank=False, null=True, validators=[RegexValidator('^[a-zA-Z ,-]*$')])
  address = models.CharField(verbose_name="Address", max_length=200, null=True)
  isbn = models.CharField(verbose_name="ISBN", max_length=50, blank=False, null=True, validators=[RegexValidator('^[0-9-xX]*$')])
  pages = models.CharField(verbose_name="Total Pages", max_length=10, blank=False, null=True, validators=[RegexValidator('^[0-9]*$')])
  price = models.CharField(verbose_name="Price", max_length=10, null=True)
# year = models.CharField(max_length=4, blank=False, validators=[RegexValidator('^[0-9]*$')])
  year = models.DateField(verbose_name="Date", blank=False, null=True)
  created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

  def clean(self):
        super(BookRecord, self).clean()
        req = current_request()
        try:
            logged_user = req.user.userdepartment
            if ((str(self.faculty.department) == logged_user.department) and (str(self.faculty.shift) == logged_user.shift)) or logged_user.department == 'All':
                return self
            else:
                raise ValidationError(
                    "You don't have rights to change other Department's Data")

        except:
            raise ValidationError(
                "You don't have rights to change other Department's Data")

  class Meta:
    verbose_name = 'Book Record'
    verbose_name_plural = 'Book Records'

  def __unicode__(self):
    return "%s" % (self.title)


class ResearchRecord(models.Model):
  title = models.CharField(verbose_name="Title/Topic", max_length=300, blank=False)
  faculty = models.ForeignKey(Faculty, default=1)
  type = models.CharField(verbose_name="Conference/Journal",
                          max_length=15, blank=False, choices=PAPER_TYPE, default=PAPER_TYPE[0][0])
  nation = models.CharField(verbose_name="International/National",
                          max_length=15, blank=False, choices=NATION, default=NATION[0][0])
  name_of_conference = models.CharField(verbose_name="Name of Conference/Journal", blank=False, max_length=300, null=True, default="")
  address = models.CharField(max_length=200, null=True, blank=True)
  indexing = models.CharField(max_length=20, choices=INDEXING_TYPE, blank=False, default=INDEXING_TYPE[0][0])
  h_index = models.CharField(verbose_name="H Index",
                             max_length=10, blank=True, null=True)
  publisher = models.CharField(
      verbose_name="Publisher", max_length=200, blank=False, null=True)
  volume = models.CharField(
          verbose_name="Volume", max_length=100, blank=False, null=True, default="")
  issue = models.CharField(
          verbose_name="Issue", max_length=100, blank=False, null=True, default="")
  isbn = models.CharField(
      verbose_name="ISBN/ISSN", max_length=15, blank=False, null=True, validators=[RegexValidator('^[0-9-Xx]*$')])
  pages = models.CharField(verbose_name="Page No",
                           max_length=10, blank=False, validators=[RegexValidator('^[0-9-]*$')], null=True)

  year = models.DateField(verbose_name="Month Year", blank=False, null=True)
  created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)




  def clean(self):
        super(ResearchRecord, self).clean()
        req = current_request()

        type = self.type
        address = self.address

        if type=='Conference' and address=='':
            raise ValidationError("Address is required for conference")

        try:
            logged_user = req.user.userdepartment
            if ((str(self.faculty.department) == logged_user.department) and (str(self.faculty.shift) == logged_user.shift)) or logged_user.department == 'All':
                return self
            else:
                raise ValidationError(
                    "You don't have rights to change other Department's Data")

        except:
            raise ValidationError(
                "You don't have rights to change other Department's Data")




  class Meta:
    verbose_name = 'Research Paper & Conference Record'
    verbose_name_plural = 'Research Paper & Conference Records'

  def __unicode__(self):
    return "%s" % (self.title)


class FDPRecord(models.Model):
  title = models.CharField(verbose_name="Title/Topic", max_length=300, blank=False)
  faculty = models.ForeignKey(Faculty, default=1)
  venue = models.CharField(verbose_name="Venue", max_length=500, blank=False, validators=[RegexValidator('^[a-z .]*$')])
  address = models.CharField(verbose_name="Address", max_length=500, blank=False, null=True)
  date = models.DateField(verbose_name="Date (from)", null=True)
  date2 = models.DateField(verbose_name="Date (to)", null=True)

  duration = models.CharField(default="", max_length=10)
  created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

  def clean(self):
        super(FDPRecord, self).clean()
        req = current_request()

        self.duration = str(abs((self.date2 - self.date).days)) + ' days'

        if (self.date2 - date.today()).days>0:
            raise ValidationError("Date (to) cannot be greater than today's date")

        if (self.date - self.date2).days>0:
            raise ValidationError("Date (from) cannot be greater than Date (to)")

        try:
            logged_user = req.user.userdepartment
            if ((str(self.faculty.department) == logged_user.department) and (str(self.faculty.shift) == logged_user.shift)) or logged_user.department == 'All':
                return self
            else:
                raise ValidationError(
                    "You don't have rights to change other Department's Data")

        except:
            raise ValidationError(
                "You don't have rights to change other Department's Data")

  class Meta:
    verbose_name = 'FDP/Workshop Record'
    verbose_name_plural = 'FDP/Workshop Records'

  def __unicode__(self):
    return "%s" % (self.title)
