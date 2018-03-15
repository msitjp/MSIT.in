# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from web.models import Faculty
from web.get_username import current_request


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
  ('Others', 'Others'),
)


class BookRecord(models.Model):
  title = models.CharField(verbose_name="Title/Topic", max_length=300)
  faculty = models.ForeignKey(Faculty)
  count = models.CharField(verbose_name="Total Count",
                           max_length=3, blank=True, null=True)
  type = models.CharField(verbose_name="International/National", max_length=15, choices=NATION, default=NATION[0][0])
  publisher = models.CharField(
      verbose_name="Publisher", max_length=200, blank=True, null=True)
  isbn = models.CharField(
      verbose_name="ISBN", max_length=50, blank=True, null=True)
  pages = models.CharField(verbose_name="Page No",
                           max_length=10, blank=True, null=True)
  year = models.CharField(max_length=4)
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
  title = models.CharField(verbose_name="Title/Topic", max_length=300)
  faculty = models.ForeignKey(Faculty)
  type = models.CharField(verbose_name="Conference/Journal",
                          max_length=15, choices=PAPER_TYPE, default=PAPER_TYPE[0][0])
  nation = models.CharField(verbose_name="International/National",
                          max_length=15, choices=NATION, default=NATION[0][0])
  indexing = models.CharField(max_length=10, choices=INDEXING_TYPE, default=INDEXING_TYPE[0][0])
  h_index = models.CharField(verbose_name="H Index",
                             max_length=10, blank=True, null=True)
  publisher = models.CharField(
      verbose_name="Publisher", max_length=200, blank=True, null=True)
  isbn = models.CharField(
      verbose_name="ISBN/ISSN", max_length=50, blank=True, null=True)
  pages = models.CharField(verbose_name="Page No",
                           max_length=10, blank=True, null=True)
  year = models.CharField(max_length=4)
  created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

  def clean(self):
        super(ResearchRecord, self).clean()
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
    verbose_name = 'Research Paper & Conference Record'
    verbose_name_plural = 'Research Paper & Conference Records'

  def __unicode__(self):
    return "%s" % (self.title)


class FDPRecord(models.Model):
  title = models.CharField(verbose_name="Title/Topic", max_length=300)
  faculty = models.ForeignKey(Faculty)
  venue = models.CharField(verbose_name="Venue", max_length=500)
  date = models.DateField()
  duration = models.CharField(max_length=5, help_text="Number of days", blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

  def clean(self):
        super(FDPRecord, self).clean()
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
    verbose_name = 'FDP/Workshop Record'
    verbose_name_plural = 'FDP/Workshop Records'

  def __unicode__(self):
    return "%s" % (self.title)
