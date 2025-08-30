from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    url(r'^/?$', home, name='home page'),
    url(r'^timetable/?$', timetable, name="timetable"),
    url(r'^attendance/?$', attendance, name="attendance"),
    url(r'^syllabus/?$', syllabus, name="syllabus"),
    url(r'^society/?$', society, name="society"),
    url(r'^aicte/?$', aicte, name="aicte"),
    url(r'^achievements/?$', achievements, name="achievements"),
    url(r'^events/?$', events, name="events"),
    url(r'^calendar/?$', calendar, name="calendar"),
    url(r'^facilities/?$', facilities, name="facilities"),
    url(r'^cse/(?P<sort>[1,2,3]+)/(?P<order>[1,2]+)/?$', cse, name="cse"),
    url(r'^cse/?$', cse, name="cse"),
    url(r'^it/(?P<sort>[1,2,3]+)/(?P<order>[1,2]+)/?$', it, name="it"),
    url(r'^it/?$', it, name="it"),
    url(r'^ece/(?P<sort>[1,2,3]+)/(?P<order>[1,2]+)/?$', ece, name="ece"),
    url(r'^ece/?$', ece, name="ece"),
    url(r'^eee/(?P<sort>[1,2,3]+)/(?P<order>[1,2]+)/?$', eee, name="eee"),
    url(r'^eee/?$', eee, name="eee"),
    url(r'^ap/(?P<sort>[1,2,3]+)/(?P<order>[1,2]+)/?$', ap, name="ap"),
    url(r'^ap/?$', ap, name="ap"),
    url(r'^latest_news/?$', latestNews, name='latest_news'),
    url(r'^notices/?$', notices, name='notices'),
    url(r'^faculties/(?P<department>[A-Za-z0-9\ ]+)/(?P<shift>[A-Za-z0-9\ ]+)/(?P<teaching>[0,1])/(?P<types>[1,2,3]+)/(?P<order>[0,1]+)/?', faculty_api),
    url(r'^(?P<key>[A-Za-z0-9_\-\(\)\[\]]+)/?$', custom),
    url(r'^send_to_notice/(?P<pk>[0-9]+)', send_to_notice),
    url(r'^achievement/(?P<category_id>\d+)/$', views.achievement_category, name='achievement_category'),
]
