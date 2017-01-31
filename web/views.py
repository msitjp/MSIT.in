from django.conf import settings
from django.shortcuts import render
from .models import *

def getContext():
    primary_navbar = PrimaryNavigationMenu.objects.all().order_by('order')
    secondary_navbar = SecondaryNavigationMenu.objects.all().order_by('order')
    primary_menu = PrimaryMenu.objects.all().order_by('order')
    latest_news = LatestNews.objects.filter(visible=True)
    secondary_menu = []
    for menu in primary_menu:
        secondary_menu = SecondaryMenu.objects.all()
    print primary_menu
    context = {
        'primary_navbar': primary_navbar,
        'secondary_navbar': secondary_navbar,
        'primary_menu': primary_menu,
        'secondary_menu': secondary_menu,
        'latest_news': latest_news
    }
    return context


def home(request):
    context = getContext()
    return render(request, 'home.html', context=context)

def administration(request):
    try:
        director_general = Faculty.objects.get(category='administration', designation__iexact='Director General')
    except:
        director_general = []
    try:
        director = Faculty.objects.get(category='administration', designation__iexact='Director')
    except:
        director = []
    try:
        deputy_director = Faculty.objects.get(category='administration', designation__iexact='Deputy Director')
    except:
        deputy_director = []
    try:
        office = Faculty.objects.filter(category='office').order_by('designation')
    except:
        office = []
    try:
        accounts = Faculty.objects.filter(category='accounts').order_by('designation')
    except:
        accounts = []
    try:
        library = Faculty.objects.filter(category='library').order_by('designation')
    except:
        library = []
    try:
        placement = Faculty.objects.filter(category='placement').order_by('designation')
    except:
        placement = []
    context = getContext()
    context['director_general'] = director_general
    context['director'] = director
    context['deputy_director'] = deputy_director
    context['office'] = office
    context['accounts'] = accounts
    context['library'] = library
    context['placement'] = placement
    return render(request, 'administration.html', context=context)

def aboutmsit(request):
    context = getContext()
    return render(request, 'aboutmsit.html', context=context)

def visionmission(request):
    context = getContext()
    return render(request, 'visionmission.html', context=context)

def history(request):
    context = getContext()
    return render(request, 'history.html', context=context)

def facilities(request):
    context = getContext()
    return render(request, 'facilities.html', context=context)

def govern(request):
    context = getContext()
    return render(request, 'govern.html', context=context)

def fromdesk(request):
    context = getContext()
    return render(request, 'fromdesk.html', context=context)

def timetable(request):
    try:
        morning = TimeTable.objects.filter(shift='M')
    except:
        morning=[]
    try:
        evening = TimeTable.objects.filter(shift='M')
    except:
        evening=[]
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    return render(request, 'timetable.html', context=context)

def attendance(request):
    try:
        morning = Attendance.objects.filter(shift='M')
    except:
        morning=[]
    try:
        evening = Attendance.objects.filter(shift='M')
    except:
        evening=[]
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    context = getContext()
    return render(request, 'attendance.html', context=context)

def syllabus(request):
    try:
        syllabus = Syllabus.objects.all()
    except:
        syllabus = []
    context = getContext()
    context['syllabus'] = syllabus
    return render(request, 'syllabus.html', context=context)

def society(request):
    try:
        societies = StudentSociety.objects.all()
    except:
        societies = []
    context = getContext()
    context['societies'] = societies
    return render(request, 'society.html', context=context)

def antiragging(request):
    try:
        director = Faculty.objects.get(category='administration', designation__iexact='Director')
    except:
        director = []
    context = getContext()
    context['director'] = director
    return render(request, 'antiragging.html', context=context)

def sexual(request):
    context = getContext()
    return render(request, 'sexual.html', context=context)

def disaster(request):
    context = getContext()
    return render(request, 'disaster.html', context=context)

def achievements(request):
    try:
        achievements = Achievements.objects.all()
    except:
        achievements = []
    context = getContext()
    context['achievements'] = achievements
    return render(request, 'achievements.html', context=context)

def events(request):
    event = Event.objects.all()
    context = getContext()
    context['events'] = event
    return render(request, 'events.html', context=context)

def cse(request):
    try:
        morning = Faculty.objects.filter(category__icontains='teaching', department='1' , shift='M')
    except:
        morning = []
    try:
        evening = Faculty.objects.filter(category__icontains='teaching', department='1', shift='E')
    except:
        evening = []
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    if settings.SORT_FACULTY_BY_NAME:
        context['facultySorter'] = True
    return render(request, 'cse.html', context=context)

def it(request):
    try:
        morning = Faculty.objects.filter(category__icontains='teaching', department='2' , shift='M')
    except:
        morning = []
    try:
        evening = Faculty.objects.filter(category__icontains='teaching', department='2', shift='E')
    except:
        evening = []
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    if settings.SORT_FACULTY_BY_NAME:
        context['facultySorter'] = True
    return render(request, 'it.html', context=context)

def ece(request):
    try:
        morning = Faculty.objects.filter(category__icontains='teaching', department='3' , shift='M')
    except:
        morning = []
    try:
        evening = Faculty.objects.filter(category__icontains='teaching', department='3', shift='E')
    except:
        evening = []
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    if settings.SORT_FACULTY_BY_NAME:
        context['facultySorter'] = True
    return render(request, 'ece.html', context=context)

def eee(request):
    try:
        morning = Faculty.objects.filter(category__icontains='teaching', department='4' , shift='M')
    except:
        morning = []
    context = getContext()
    context['morning'] = morning
    if settings.SORT_FACULTY_BY_NAME:
        context['facultySorter'] = True
    return render(request, 'eee.html', context=context)

def ap(request):
    try:
        morning = Faculty.objects.filter(category__icontains='teaching', department='5' , shift='M')
    except:
        morning = []
    try:
        evening = Faculty.objects.filter(category__icontains='teaching', department='5', shift='E')
    except:
        evening = []
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    if settings.SORT_FACULTY_BY_NAME:
        context['facultySorter'] = True
    return render(request, 'ap.html', context=context)

def placements(request):
    context = getContext()
    return render(request, 'placements.html', context=context)

def contact(request):
    context = getContext()
    return render(request, 'contact.html', context=context)

def suggestion(request):
    context = getContext()
    return render(request, 'suggestion.html', context=context)

def latestNews(request):
    news = LatestNews.objects.all().order_by('-created_at')
    context = getContext()
    context['news'] = news
    return render(request, 'latest.html', context=context)
