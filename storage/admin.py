# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from xlsxwriter.workbook import Workbook

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import url
from django.http import HttpResponse

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from storage.models import BookRecord, ResearchRecord, NATION, PAPER_TYPE
from web.models import Faculty


@staff_member_required
def exportBook(request, queryset=None):
  output = StringIO.StringIO()

  book = Workbook(output)
  sheet = book.add_worksheet()

  # File Construction Starts Here
  headers = [
    'Sr.no', 'Faculty Name', 'Designation', 'Total Count', 'Title/Topic', 'International/National', 'Publisher', 'ISBN', 'Page.no', 'Year'
  ]

  records = queryset
  if queryset is None:
    records = BookRecord.objects.all().order_by('-year')
  total = records.count()

  sheet.set_column(0, 0, 10)
  sheet.set_column(1, 15, 25)
  sheet.set_row(0, 50)
  global_format = {
    'font_name': 'Times New Roman',
    'align': 'left',
    'valign': 'vcenter',
    'font_size': '12'
  }
  for i in range(1, total+2):
    sheet.set_row(i, 15)

  form = {}
  form.update(global_format)
  form.update({'font_size': '20', 'underline': True, 'align': 'center'})
  sheet.merge_range('A1:J1', 'Book Published Record', book.add_format(form))

  form = {}
  form.update(global_format)
  form.update({'bold': True, 'border': 2, 'align': 'center'})
  for i in range(0, 10):
      sheet.write(1, i, headers[i], book.add_format(form))

  data = []
  counter = 1
  for a in records:
    data.append([str(counter), str(a.faculty), a.faculty.designation[1:] +', '+ a.faculty.department, a.count, a.title, a.type, a.publisher, a.isbn, a.pages, a.year])
    counter += 1

  form = {}
  form.update(global_format)
  form.update({'border': 1})
  r = 2
  c = 0
  for a in data:
      for b in a:
          sheet.write(r, c, b, book.add_format(form))
          c += 1
      r += 1
      c = 0

  # End

  book.close()

  # construct response
  output.seek(0)
  response = HttpResponse(output.read(
  ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
  response['Content-Disposition'] = "attachment; filename=BooksRecord.xlsx"

  return response


class BookRecordAdmin(admin.ModelAdmin):
  change_list_template = 'admin/app/Books/change_list_book.html'

  list_display = ['title', 'faculty', 'type', 'publisher', 'isbn', 'year', 'updated_at', 'created_at']
  list_filter = ('type', ('year', DropdownFilter), ('faculty', RelatedDropdownFilter),
                 ('faculty__department', DropdownFilter), 'faculty__shift',)
  ordering = ('-created_at', '-updated_at', 'title', 'faculty', )
  search_fields = ['title', 'faculty', 'publisher', 'isbn']

  actions = ['export_selected']

  def export_selected(self, request, queryset):
    return exportBook(request, queryset)

  export_selected.short_descriptioon = 'Export the selected Records'

  def get_urls(self):
        urls = super(BookRecordAdmin, self).get_urls()
        my_urls = [
            url(r"^export_book_records_list/$", exportBook)
        ]
        return my_urls + urls


def exportResearch(request, queryset=None):
  output = StringIO.StringIO()

  book = Workbook(output)
  sheet = book.add_worksheet()

  # File Construction Starts Here
  headers = [
    'Sr.no',
    'Faculty Name',
    'Designation',
    'Total Count (Conference)',
    'Total Count (Journal)',
    'Title/Topic',
    'Journal/Conference',
    'H Index',
    'International/National',
    'ISBN',
    'Publisher',
    'Page.no',
    'Year'
  ]

  if queryset is None:
    records = list(set( e[0] for e in ResearchRecord.objects.values_list('faculty')))
    queryset = ResearchRecord.objects.all()
  else:
    records = list(set( e[0] for e in queryset.values_list('faculty')))

  total = len(records)

  sheet.set_column(0, 0, 10)
  sheet.set_column(1, 15, 25)
  sheet.set_row(0, 50)
  global_format = {
      'font_name': 'Times New Roman',
      'align': 'left',
      'valign': 'vcenter',
      'font_size': '12'
  }
  for i in range(1, total+1):
      sheet.set_row(i, 15)

  form = {}
  form.update(global_format)
  form.update({'font_size': '20', 'underline': True, 'align': 'center'})
  sheet.merge_range(
      'A1:M1', 'Research Paper & Conferences Record', book.add_format(form))

  form = {}
  form.update(global_format)
  form.update({'bold': True, 'border': 2, 'align': 'center'})
  for i in range(0, len(headers)):
      sheet.write(1, i, headers[i], book.add_format(form))

  data = []
  counter = 1
  rowspan_count = 2
  form = {}
  form.update(global_format)
  form.update({'border': 1})
  for i in records:
    f = Faculty.objects.get(id=i)
    l = queryset.filter(faculty=f)
    con_count = l.filter(type=PAPER_TYPE[0][0]).count()
    jou_count = l.filter(type=PAPER_TYPE[1][0]).count()
    total = con_count + jou_count
    if total > 1:
      sheet.merge_range('A{s}:A{d}'.format(s=rowspan_count+1, d=rowspan_count+total), counter, book.add_format(form))
      sheet.merge_range('B{s}:B{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + total), str(f), book.add_format(form))
      sheet.merge_range('C{s}:C{d}'.format(s=rowspan_count + 1, d=rowspan_count + total),
                        f.designation[1:] + ', ' + f.department, book.add_format(form))
      sheet.merge_range('D{s}:D{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + total), str(con_count), book.add_format(form))
      sheet.merge_range('E{s}:E{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + total), str(jou_count), book.add_format(form))
    else:
      sheet.write(rowspan_count, 0, counter, book.add_format(form))
      sheet.write(rowspan_count, 1, str(f), book.add_format(form))
      sheet.write(rowspan_count, 2, f.designation[1:] + ', ' + f.department, book.add_format(form))
      sheet.write(rowspan_count, 3, str(con_count), book.add_format(form))
      sheet.write(rowspan_count, 4, str(jou_count), book.add_format(form))

    papers = queryset.filter(faculty=f).order_by('-year')
    for i in papers:
      sheet.write(rowspan_count, 5, i.title, book.add_format(form))
      sheet.write(rowspan_count, 6, i.type, book.add_format(form))
      sheet.write(rowspan_count, 7, i.h_index, book.add_format(form))
      sheet.write(rowspan_count, 8, i.nation, book.add_format(form))
      sheet.write(rowspan_count, 9, i.isbn, book.add_format(form))
      sheet.write(rowspan_count, 10, i.publisher, book.add_format(form))
      sheet.write(rowspan_count, 11, i.pages, book.add_format(form))
      sheet.write(rowspan_count, 12, i.year, book.add_format(form))
      rowspan_count += 1

    # rowspan_count += total
    counter += 1
  # End

  book.close()

  # construct response
  output.seek(0)
  response = HttpResponse(output.read(
  ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
  response['Content-Disposition'] = "attachment; filename=Research Papers & Conferences.xlsx"

  return response


class ResearchRecordAdmin(admin.ModelAdmin):
  change_list_template = 'admin/app/Books/change_list_research.html'

  list_display = ['title', 'faculty', 'type', 'nation', 'publisher',
                  'isbn', 'year', 'updated_at', 'created_at']
  list_filter = ('type', 'nation', ('year', DropdownFilter), ('faculty', RelatedDropdownFilter),
                 ('faculty__department', DropdownFilter), 'faculty__shift',)
  ordering = ('-created_at', '-updated_at', 'title', 'faculty', )
  search_fields = ['title', 'faculty', 'publisher', 'isbn']

  actions = ['export_selected']

  def export_selected(self, request, queryset):
    return exportResearch(request, queryset)

  export_selected.short_descriptioon = 'Export the selected Records'

  def get_urls(self):
        urls = super(ResearchRecordAdmin, self).get_urls()
        my_urls = [
            url(r"^export_research_records_list/$", exportResearch)
        ]
        return my_urls + urls

admin.site.register(BookRecord, BookRecordAdmin)
admin.site.register(ResearchRecord, ResearchRecordAdmin)
