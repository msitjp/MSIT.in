from datetime import date

from django import forms

from .models import ResearchRecord
from .utils.widgets import MonthYearWidget


class ResearchRecordForm(forms.ModelForm):
  year = forms.DateField(required=False, widget=MonthYearWidget(years=xrange(1970, date.today().year)))

  class Meta:
    model = ResearchRecord
    fields = ('__all__')