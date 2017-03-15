from django import template
from django.template.defaultfilters import slugify as sl

'''
Made by @htadg motherfuckers
'''

register = template.Library()


@register.filter
def in_category(things, category):
    return things.filter(parent=category).order_by('order')


@register.filter
def slugify(id):
    return sl(id)
