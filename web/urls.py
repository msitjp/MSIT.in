from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', home, name='home page'),
    url(r'^administration$', administration, name='administration'),
    url(r'^aboutmsit$', aboutmsit, name='aboutmsit'),
    url(r'^visionmission$', visionmission, name="visionmission"),
    url(r'^history$', history, name="history"),
    url(r'^facilities$', facilities, name="facilities"),
    url(r'^govern$', govern, name="govern"),
    url(r'^fromdesk$', fromdesk, name="fromdesk"),
    url(r'^timetable$', timetable, name="timetable"),
    url(r'^attendance$', attendance, name="attendance"),
    url(r'^syllabus$', syllabus, name="syllabus"),
    url(r'^society$', society, name="society"),
    url(r'^antiragging$', antiragging, name="antiragging"),
    url(r'^sexual$', sexual, name="sexual"),
    url(r'^disaster$', disaster, name="disaster"),
    url(r'^achievements$', achievements, name="achievements"),
    url(r'^events$', events, name="events"),
    url(r'^cse$', cse, name="cse"),
    url(r'^it$', it, name="it"),
    url(r'^ece$', ece, name="ece"),
    url(r'^eee$', eee, name="eee"),
    url(r'^ap$', ap, name="ap"),
    url(r'^placements$', placements, name="placements"),
    url(r'^contact$', contact, name="contact")
    url(r'^suggestion$', suggestion, name="suggestions")
]
