# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from web.models import Faculty


NATION = (
  ('International', 'International'),
  ('National', 'National'),
)

PAPER_TYPE = (
  ('Conference', 'Conference'),
  ('Journal', 'Journal'),
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

  class Meta:
    verbose_name = 'Research Paper & Conference Record'
    verbose_name_plural = 'Research Paper & Conference Records'

  def __unicode__(self):
    return "%s" % (self.title)
