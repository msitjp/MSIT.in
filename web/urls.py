from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^/?$', home, name='home page'),
    url(r'^timetable/?$', timetable, name="timetable"),
    url(r'^attendance/?$', attendance, name="attendance"),
    url(r'^syllabus/?$', syllabus, name="syllabus"),
    url(r'^society/?$', society, name="society"),
    url(r'^achievements/?$', achievements, name="achievements"),
    url(r'^events/?$', events, name="events"),
    url(r'^cse/?$', cse, name="cse"),
    url(r'^it/?$', it, name="it"),
    url(r'^ece/?$', ece, name="ece"),
    url(r'^eee/?$', eee, name="eee"),
    url(r'^ap/?$', ap, name="ap"),
    url(r'^latest_news/?$', latestNews, name='latest_news'),
    url(r'^notices/?$', notices, name='notices'),
    url(r'^(?P<key>[A-Za-z0-9_\-\(\)\[\]]+)/?$', custom)
]
