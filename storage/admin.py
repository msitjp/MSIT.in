# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    import cStringIO as StringIO
except ImportError:
    import io as StringIO

from xlsxwriter.workbook import Workbook

from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from rangefilter.filter import DateRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from .forms import BookRecordForm, FDPRecordForm, ResearchRecordForm
from .models import BookRecord, ResearchRecord, FDPRecord, NATION, PAPER_TYPE

from web.get_username import current_request
from web.models import Faculty, UserDepartment


@staff_member_required
def exportBook(request, queryset=None):
  output = StringIO.StringIO()

  book = Workbook(output)
  sheet = book.add_worksheet()

#  if not request.user.is_superuser:
#      queryset = BookRecord.objects.filter(faculty__full_name=request.user.username.replace('-',' ').title());

  # File Construction Starts Here
  headers = [
    'Sr.no', 'Faculty Name', 'Designation', 'Total Count', 'Title/Topic', 'Other Authors','International/National', 'Publisher', 'Address', 'ISBN', 'Page.no', 'Year', 'Price'
  ]


  if queryset is None:
    department = request.user.userdepartment.department
    if department == 'All':
      records = list(set(e[0] for e in BookRecord.objects.order_by('-faculty__designation').values_list('faculty')))
    else:
#      records = list(set(e[0] for e in BookRecord.objects.filter(faculty__department=department).order_by('-faculty__designation').values_list('faculty')))
      records = list(set(e[0] for e in BookRecord.objects.filter(faculty__full_name=request.user.username.replace('-',' ').title()).order_by('-faculty__designation').values_list('faculty')))

    queryset = BookRecord.objects.all()
  else:
    records = list(set(e[0] for e in queryset.values_list('faculty')))

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
  for i in range(1, total+2):
    sheet.set_row(i, 15)

  form = {}
  form.update(global_format)
  form.update({'font_size': '20', 'underline': True, 'align': 'center'})
  sheet.merge_range('A1:J1', 'Book Published Record', book.add_format(form))

  form = {}
  form.update(global_format)
  form.update({'bold': True, 'border': 2, 'align': 'center'})
  for i in range(0, len(headers)):
      sheet.write(1, i, headers[i], book.add_format(form))

  counter = 1
  rowspan_count = 2
  form = {}
  form.update(global_format)
  form.update({'border': 1})
  for i in records:
    f = Faculty.objects.get(id=i)
    l = queryset.filter(faculty=f)
    count = l.count()
    if count > 1:
      sheet.merge_range('A{s}:A{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + count), counter, book.add_format(form))
      sheet.merge_range('B{s}:B{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + count), str(f), book.add_format(form))
      sheet.merge_range('C{s}:C{d}'.format(s=rowspan_count + 1, d=rowspan_count + count),
                        f.designation[1:] + ', ' + f.department, book.add_format(form))
      sheet.merge_range('D{s}:D{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + count), str(count), book.add_format(form))
    else:
      sheet.write(rowspan_count, 0, counter, book.add_format(form))
      sheet.write(rowspan_count, 1, str(f), book.add_format(form))
      sheet.write(rowspan_count, 2, f.designation[
                  1:] + ', ' + f.department, book.add_format(form))
      sheet.write(rowspan_count, 3, str(count), book.add_format(form))

    books = queryset.filter(faculty=f).order_by('-year')
    for i in books:
      sheet.write(rowspan_count, 4, i.title, book.add_format(form))
      sheet.write(rowspan_count, 5, i.other, book.add_format(form))
      sheet.write(rowspan_count, 6, i.type, book.add_format(form))
      sheet.write(rowspan_count, 7, i.publisher, book.add_format(form))
      sheet.write(rowspan_count, 8, i.address, book.add_format(form))
      sheet.write(rowspan_count, 9, i.isbn, book.add_format(form))
      sheet.write(rowspan_count, 10, i.pages, book.add_format(form))
      sheet.write(rowspan_count, 11, i.year, book.add_format(form))
      sheet.write(rowspan_count, 12, i.price, book.add_format(form))
      rowspan_count += 1

    # rowspan_count += total
    counter += 1

  # End

  book.close()

  # construct response
  output.seek(0)
  response = HttpResponse(output.read(
  ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
  response['Content-Disposition'] = "attachment; filename=BooksRecord.xlsx"

  return response


@staff_member_required
def exportResearch(request, queryset=None):
  output = StringIO.StringIO()

  book = Workbook(output)
  sheet = book.add_worksheet()

#  if not request.user.is_superuser:
#      queryset = ResearchRecord.objects.filter(faculty__full_name=request.user.username.replace('-',' ').title());

  # File Construction Starts Here
  headers = [
    'Sr.no',
    'Faculty Name',
    'Designation',
    'Total Count (Conference)',
    'Total Count (Journal)',
    'Title/Topic',
    'Journal/Conference',
    'International/National',
    'Name of Conference/Journal',
    'Indexing',
    'H Index',
    'Publisher',
    'Volume',
    'Issue',
    'ISBN',
    'Page.no',
    'Month Year'
  ]

  if queryset is None:
    department = request.user.userdepartment.department
    if department == 'All':
      records = list(set(e[0] for e in ResearchRecord.objects.order_by(
          '-faculty__designation').values_list('faculty')))
    else:
#      records = list(set(e[0] for e in ResearchRecord.objects.filter(faculty__department=department).order_by('-faculty__designation').values_list('faculty')))
      records = list(set(e[0] for e in ResearchRecord.objects.filter(faculty__full_name=request.user.username.replace('-',' ').title()).order_by('-faculty__designation').values_list('faculty')))

    queryset = ResearchRecord.objects.all()
  else:
    records = list(set( e[0] for e in queryset.values_list('faculty')))

  total = len(records)

  sheet.set_column(0, 0, 10)
  sheet.set_column(1, len(headers)-1, 25)
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
      'A1:Q1', 'Research Paper & Conferences Record', book.add_format(form))

  form = {}
  form.update(global_format)
  form.update({'bold': True, 'border': 2, 'align': 'center'})
  for i in range(0, len(headers)):
      sheet.write(1, i, headers[i], book.add_format(form))

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
      temp_time = ''
      if i.year:
        temp_time = i.year.strftime('%B,%Y')
      sheet.write(rowspan_count, 5, i.title, book.add_format(form))
      sheet.write(rowspan_count, 6, i.type, book.add_format(form))
      sheet.write(rowspan_count, 7, i.nation, book.add_format(form))
      sheet.write(rowspan_count, 8, i.name_of_conference, book.add_format(form))
      sheet.write(rowspan_count, 9, i.indexing, book.add_format(form))
      sheet.write(rowspan_count, 10, i.h_index, book.add_format(form))
      sheet.write(rowspan_count, 11, i.publisher, book.add_format(form))
      sheet.write(rowspan_count, 12, i.volume, book.add_format(form))
      sheet.write(rowspan_count, 13, i.issue, book.add_format(form))
      sheet.write(rowspan_count, 14, i.isbn, book.add_format(form))
      sheet.write(rowspan_count, 15, i.pages, book.add_format(form))
      sheet.write(rowspan_count, 16, temp_time, book.add_format(form))
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

@staff_member_required
def exportFDP(request, queryset=None):
  output = StringIO.StringIO()

  book = Workbook(output)
  sheet = book.add_worksheet()

#  if not request.user.is_superuser:
#      queryset = FDPRecord.objects.filter(faculty__full_name=request.user.username.replace('-',' ').title());

  # File Construction Starts Here
  headers = ['Sr.no', 'Faculty Name', 'Designation', 'Total Count', 'Title/Topic', 'Date (from)', 'Date (to)', 'Duration', 'Venue', 'Address']

  if queryset is None:
    department = request.user.userdepartment.department
    if department == 'All':
      records = list(set(e[0] for e in FDPRecord.objects.order_by(
          '-faculty__designation').values_list('faculty')))
    else:
      records = list(set(e[0] for e in FDPRecord.objects.filter(faculty__full_name=request.user.username.replace('-',' ').title()).order_by('-faculty__designation').values_list('faculty')))
#      records = list(set(e[0] for e in FDPRecord.objects.filter(faculty__department=department).order_by('-faculty__designation').values_list('faculty')))

    queryset = FDPRecord.objects.all()
  else:
    records = list(set(e[0] for e in queryset.values_list('faculty')))

  total = len(records)

  sheet.set_column(0, 0, 7)
  sheet.set_column(1, 1, 25)
  sheet.set_column(2, 2, 20)
  sheet.set_column(3, 3, 15)
  sheet.set_column(4, 4, 60)
  sheet.set_column(5, 5, 25)
  sheet.set_column(6, 6, 60)
  sheet.set_row(0, 50)
  global_format = {
      'font_name': 'Times New Roman',
      'align': 'left',
      'valign': 'vcenter',
      'font_size': '12'
  }
  for i in range(1, total + 1):
      sheet.set_row(i, 15)

  form = {}
  form.update(global_format)
  form.update({'font_size': '20', 'underline': True, 'align': 'center'})
  sheet.merge_range(
      'A1:G1', 'FDP/Workshop Record', book.add_format(form))

  form = {}
  form.update(global_format)
  form.update({'bold': True, 'border': 2, 'align': 'center'})
  for i in range(0, len(headers)):
      sheet.write(1, i, headers[i], book.add_format(form))

  counter = 1
  rowspan_count = 2
  form = {}
  form.update(global_format)
  form.update({'border': 1})
  for i in records:
    f = Faculty.objects.get(id=i)
    l = queryset.filter(faculty=f)
    total = l.count()
    if total > 1:
      sheet.merge_range('A{s}:A{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + total), counter, book.add_format(form))
      sheet.merge_range('B{s}:B{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + total), str(f), book.add_format(form))
      sheet.merge_range('C{s}:C{d}'.format(s=rowspan_count + 1, d=rowspan_count + total),
                        f.designation[1:] + ', ' + f.department, book.add_format(form))
      sheet.merge_range('D{s}:D{d}'.format(
          s=rowspan_count + 1, d=rowspan_count + total), str(total), book.add_format(form))
    else:
      sheet.write(rowspan_count, 0, counter, book.add_format(form))
      sheet.write(rowspan_count, 1, str(f), book.add_format(form))
      sheet.write(rowspan_count, 2, f.designation[
                  1:] + ', ' + f.department, book.add_format(form))
      sheet.write(rowspan_count, 3, str(total), book.add_format(form))

    workshops = queryset.filter(faculty=f).order_by('-date')
    for i in workshops:
      sheet.write(rowspan_count, 4, i.title, book.add_format(form))
#      if i.duration is not None:
#        temp = i.date.strftime('%d %B, %Y') + '(' + i.duration + ' )'
#      else:
#        temp = i.date.strftime('%d %B, %Y')
      if i.date:
          temp1 = i.date.strftime('%d %B, %Y')

      if i.date2:
          temp2 = i.date2.strftime('%d %B, %Y')

      sheet.write(rowspan_count, 5, temp1, book.add_format(form))
      sheet.write(rowspan_count, 6, temp2, book.add_format(form))
      sheet.write(rowspan_count, 7, i.duration, book.add_format(form))
      sheet.write(rowspan_count, 8, i.venue, book.add_format(form))
      sheet.write(rowspan_count, 9, i.address, book.add_format(form))
      rowspan_count += 1

    # rowspan_count += total
    counter += 1
  # End

  book.close()

  # construct response
  output.seek(0)
  response = HttpResponse(output.read(
  ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
  response[
      'Content-Disposition'] = "attachment; filename=FDP/Workshops.xlsx"

  return response


class FacultyFilter(RelatedDropdownFilter):
  title = 'Faculty'
  parameter_name = 'faculty'

  def __init__(self, field, request, params, model, model_admin, field_path):
    super(FacultyFilter, self).__init__(field, request, params, model, model_admin, field_path)
    user = request.user.userdepartment
    self.qs = Faculty.objects.all()
    if user.department != 'All':
      self.qs = Faculty.objects.filter(
          department=user.department, shift=user.shift, category='teaching')

  def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and not self.lookup_val_isnull,
            'query_string': changelist.get_query_string(
                {},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            'display': _('All'),
        }
        for i in self.qs:
            yield {
                'selected': self.lookup_val == force_text(i.pk),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: i.pk,
                }, [self.lookup_kwarg_isnull]),
                'display': str(i),
            }
        if self.include_empty_choice:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }


class BookRecordAdmin(admin.ModelAdmin):
  change_list_template = 'admin/app/Books/change_list_book.html'

  form = BookRecordForm

  list_display = ['title', 'faculty', 'other', 'count', 'type', 'publisher', 'address',
                  'isbn', 'pages', 'price', 'year', 'updated_at', 'created_at']
  list_filter = ('type', ('year', DropdownFilter), ('faculty', FacultyFilter),
                      ('faculty__department',DropdownFilter), 'faculty__shift',)
  ordering = ('-created_at', '-updated_at', 'title', 'faculty', )
  search_fields = ['title', 'faculty__full_name', 'publisher', 'isbn']

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

  def get_queryset(self, request):
        qs = super(BookRecordAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
#            return qs.filter(faculty__department=u.department, faculty__shift=u.shift)
             return qs.filter(faculty__full_name=request.user.username.replace('-',' ').title())

  def get_list_filter(self, request):
    if request.user.userdepartment.department == 'All':
      return ('type', ('year', DropdownFilter), ('faculty', FacultyFilter),
                      ('faculty__department',DropdownFilter), 'faculty__shift',)
    else:
      return ('type', ('year', DropdownFilter),)


class ResearchRecordAdmin(admin.ModelAdmin):
  change_list_template = 'admin/app/Books/change_list_research.html'

  def get_year(self, obj):
    try:
      return obj.year.strftime('%B,%Y')
    except:
      return ''
  get_year.admin_order_field = 'Month Year'
  get_year.short_description = 'Month Year'

  form = ResearchRecordForm

  list_display = ['title', 'faculty', 'type', 'nation', 'name_of_conference', 'address', 'indexing', 'h_index', 'publisher',
                  'volume', 'issue', 'isbn', 'pages', 'get_year', 'updated_at', 'created_at']
  list_filter = ('type', 'nation', ('year', DateRangeFilter), ('faculty', FacultyFilter),
                 ('faculty__department', DropdownFilter), 'faculty__shift',)
  ordering = ('-created_at', '-updated_at', 'title', 'faculty', )
  search_fields = ['title', 'faculty__full_name', 'publisher', 'name_of_conference', 'isbn']

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

  def get_queryset(self, request):
        qs = super(ResearchRecordAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
#           return qs.filter(faculty__department=u.department, faculty__shift=u.shift)
            return qs.filter(faculty__full_name=request.user.username.replace('-',' ').title())

  def get_list_filter(self, request):
    if request.user.userdepartment.department == 'All':
      return ('type', 'nation', ('year', DateRangeFilter), ('faculty', FacultyFilter),
              ('faculty__department', DropdownFilter), 'faculty__shift',)
    else:
      return ('type', 'nation', ('year', DateRangeFilter),)


class FDPRecordAdmin(admin.ModelAdmin):
  change_list_template = 'admin/app/Books/change_list_fdp.html'

  form = FDPRecordForm

  list_display = ['title', 'faculty', 'venue', 'address', 'date', 'date2', 'duration', 'updated_at', 'created_at']

  list_filter = (('date', DateRangeFilter), ('faculty', FacultyFilter),
                 ('faculty__department', DropdownFilter), 'faculty__shift',)

  ordering = ('-created_at', '-updated_at', '-date', )
  search_fields = ['title', 'faculty__full_name', 'venue']

  actions = ['export_selected']

  def export_selected(self, request, queryset):
    return exportFDP(request, queryset)

  export_selected.short_descriptioon = 'Export the selected Records'

  def get_urls(self):
        urls = super(FDPRecordAdmin, self).get_urls()
        my_urls = [
            url(r"^export_fdp_records_list/$", exportFDP)
        ]
        return my_urls + urls

  def get_queryset(self, request):
        qs = super(FDPRecordAdmin, self).get_queryset(request)
        ud = User.objects.get(username=request.user.username)
        u = UserDepartment.objects.get(user=ud)
        if request.user.is_superuser or u.department == 'All':
            return qs
        else:
#            return qs.filter(faculty__department=u.department, faculty__shift=u.shift)
             return qs.filter(faculty__full_name=request.user.username.replace('-',' ').title())

  def get_list_filter(self, request):
    if request.user.userdepartment.department == 'All':
      return (('date', DateRangeFilter), ('faculty', FacultyFilter),
              ('faculty__department', DropdownFilter), 'faculty__shift',)
    else:
      return (('date', DateRangeFilter),)

admin.site.register(BookRecord, BookRecordAdmin)
admin.site.register(ResearchRecord, ResearchRecordAdmin)
admin.site.register(FDPRecord, FDPRecordAdmin)
