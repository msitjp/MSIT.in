from django.shortcuts import render
from .models import *

def getContext():
    primary_navbar = PrimaryNavigationMenu.objects.all()
    secondary_navbar = SecondaryNavigationMenu.objects.all()
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
