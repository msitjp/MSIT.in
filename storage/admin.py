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

from django_admin_listfilter_dropdown.filters import DropdownFilter

from storage.models import BookRecord


@staff_member_required
def exportBook(request, queryset=None):
  print "queryset", queryset
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

  sheet.set_column(0, 0, 20)
  sheet.set_column(1, 15, 15)
  sheet.set_row(0, 50)
  global_format = {
    'font_name': 'Times New Roman',
    'align': 'center',
    'valign': 'vcenter',
    'font_size': '12'
  }
  for i in range(1, total+2):
    sheet.set_row(i, 40)

  form = {'font_size': '15', 'underline': True}
  form.update(global_format)
  sheet.merge_range('A1:J1', 'Book Published Record', book.add_format(form))

  form = {'bold': True, 'border': 2}
  form.update(global_format)
  for i in range(0, 10):
      sheet.write(1, i, headers[i], book.add_format(form))

  data = []
  counter = 1
  for a in records:
    data.append([str(counter), str(a.faculty), a.faculty.designation[1:] +', '+ a.faculty.department, a.count, a.title, a.type, a.publisher, a.isbn, a.pages, a.year])
    counter += 1

  form = {'font_size': '10', 'border': 1}
  form.update(global_format)
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
  change_list_template = 'admin/app/Books/change_list.html'

  list_display = ['title', 'faculty', 'type', 'publisher', 'isbn', 'year', 'updated_at', 'created_at']
  list_filter = ('type', ('year', DropdownFilter),
                 ('faculty__department', DropdownFilter), 'faculty__shift',)
  ordering = ('-created_at', '-updated_at', 'title', 'faculty', )
  search_fields = ['title', 'faculty', 'publisher', 'isbn']

  actions = ['export_selected']

  def export_selected(self, request, queryset):
    print queryset
    return exportBook(request, queryset)

  export_selected.short_descriptioon = 'Export the selected Records'

  def get_urls(self):
        urls = super(BookRecordAdmin, self).get_urls()
        my_urls = [
            url(r"^export_mailing_list/$", exportBook)
        ]
        return my_urls + urls



admin.site.register(BookRecord, BookRecordAdmin)
