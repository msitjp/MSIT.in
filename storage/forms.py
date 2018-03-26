from datetime import date

from django import forms

from .models import BookRecord, FDPRecord, ResearchRecord
from .utils.widgets import MonthYearWidget

from web.get_username import current_request
from web.models import Faculty


class BookRecordForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(BookRecordForm, self).__init__(*args, **kwargs)
    req = current_request()
    try:
      user = req.user.userdepartment
      if user.department != 'All':
        self.fields['faculty'].queryset = Faculty.objects.filter(department=user.department, shift=user.shift, category='teaching').order_by('full_name')
      else:
        self.fields['faculty'].queryset = Faculty.objects.all().order_by('full_name')
    except:
      pass

  class Meta:
    model = BookRecord
    fields = ('__all__')


class ResearchRecordForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(ResearchRecordForm, self).__init__(*args, **kwargs)
    req = current_request()
    try:
      user = req.user.userdepartment
      if user.department != 'All':
        self.fields['faculty'].queryset = Faculty.objects.filter(
            department=user.department, shift=user.shift, category='teaching').order_by('full_name')
      else:
        self.fields['faculty'].queryset = Faculty.objects.all().order_by('full_name')
    except:
      pass

  class Meta:
    model = ResearchRecord
    fields = ('__all__')


class FDPRecordForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(FDPRecordForm, self).__init__(*args, **kwargs)
    req = current_request()
    try:
      user = req.user.userdepartment
      if user.department != 'All':
        self.fields['faculty'].queryset = Faculty.objects.filter(
            department=user.department, shift=user.shift, category='teaching').order_by('full_name')
      else:
        self.fields['faculty'].queryset = Faculty.objects.all().order_by('full_name')
    except:
      pass

  class Meta:
    model = FDPRecord
    fields = ('__all__')
