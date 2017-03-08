from django.conf import settings
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from .models import *

def getContext():
    primary_navbar = PrimaryNavigationMenu.objects.all().order_by('order')
    secondary_navbar = SecondaryNavigationMenu.objects.all().order_by('order')
    primary_menu = PrimaryMenu.objects.all().order_by('order')
    latest_news = LatestNews.objects.filter(visible=True)
    notices = Notice.objects.filter(visible=True)
    secondary_menu = []
    for menu in primary_menu:
        secondary_menu = SecondaryMenu.objects.all()
    marquee = Marquee.objects.all()
    context = {
        'primary_navbar': primary_navbar,
        'secondary_navbar': secondary_navbar,
        'primary_menu': primary_menu,
        'secondary_menu': secondary_menu,
        'latest_news': latest_news,
        'notices': notices,
        'marquee': marquee
    }
    return context


def home(request):
    context = getContext()
    return render(request, 'home.html', context=context)

def timetable(request):
    try:
        morning = TimeTable.objects.filter(shift='M')
    except:
        morning=[]
    try:
        evening = TimeTable.objects.filter(shift='E')
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
        evening = Attendance.objects.filter(shift='E')
    except:
        evening=[]
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
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

def achievements(request):
    try:
        achievements = Achievement.objects.all()
    except:
        achievements = []
    context = getContext()
    context['achievements'] = achievements
    return render(request, 'achievements.html', context=context)

def events(request):
    try:
        event = Event.objects.all().oreder_by('-date')
    except:
        event = Event.objects.all()
    context = getContext()
    context['events'] = event
    return render(request, 'events.html', context=context)

#
# Available Department Choices are ::
# CSE, IT, ECE, EEE, APPLIED SCIENCES

def get_modifier(department):
    '''
        Sorting Modes are ::
        ('1', 'Name wise')
        ('2', 'Designation wise')
        ('3', 'Date-of-joining wise')
    '''
    modifier = ''
    a = int(department.sorting_order)
    b = int(department.sorting_order)
    if a == 1:
        modifier = 'full_name'
    elif a == 2:
        modifier = 'designation'
    elif a == 3:
        modifier = 'date_of_joining'
    if b == 2:
        modifier = '-'+modifier
    return modifier

def get_faculties(department, modifier):
    print modifier
    context = {}
    if department.display_1st_faculty:
        try:
            morning = Faculty.objects.filter(category__icontains='teaching', department=department , shift='M').order_by(modifier)
        except:
            morning = []
        context['morning'] = morning
    if department.display_2nd_faculty:
        try:
            evening = Faculty.objects.filter(category__icontains='teaching', department=department , shift='E').order_by(modifier)
        except:
            evening = []
        context['evening'] = evening
    if department.display_1st_assistant:
        try:
            mlab = Faculty.objects.filter(category__icontains='assistant', department=department , shift='M').order_by(modifier)
        except:
            mlab = []
        context['mlab'] = mlab
    if department.display_2nd_assistant:
        try:
            elab = Faculty.objects.filter(category__icontains='assistant', department=department , shift='E').order_by(modifier)
        except:
            elab = []
        context['elab'] = elab
    return context

def cse(request):
    department = Department.objects.get(department='CSE')
    tabs = department.departmentpage_set.all()
    modifier = get_modifier(department)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    print context
    return render(request, 'faculty.html', context=context)

def it(request):
    department = Department.objects.get(department='IT')
    tabs = department.departmentpage_set.all()
    modifier = get_modifier(department)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    return render(request, 'faculty.html', context=context)

def ece(request):
    department = Department.objects.get(department='ECE')
    tabs = department.departmentpage_set.all()
    modifier = get_modifier(department)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    return render(request, 'faculty.html', context=context)

def eee(request):
    department = Department.objects.get(department='EEE')
    tabs = department.departmentpage_set.all()
    modifier = get_modifier(department)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    return render(request, 'faculty.html', context=context)

def ap(request):
    department = Department.objects.get(department='APPLIED SCIENCES')
    tabs = department.departmentpage_set.all()
    modifier = get_modifier(department)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    return render(request, 'faculty.html', context=context)

def latestNews(request):
    news = LatestNews.objects.all().order_by('-created_at')
    context = getContext()
    context['news'] = news
    return render(request, 'latest.html', context=context)

def notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    context = getContext()
    context['notices'] = notices
    return render(request, 'notices.html', context=context)

def custom(request, key):
    filters = [' ', '@', '#', '^', '!', '&', '~', '/', '`']
    Flag = True
    for c in filters:
        if c in key:
            Flag = False
            break
    if not Flag:
        raise Http404
    key = '/'+key
    page = get_object_or_404(Page, link=key)
    tabs = page.tab_set.all()
    context = getContext()
    context['tabs'] = tabs
    print context
    return render(request, 'general.html', context=context)
