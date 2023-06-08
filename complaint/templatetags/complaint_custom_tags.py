from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter
def in_check(value, i):
    return i in value
@register.filter
def index(indexable, i):
    try:
        a = indexable[int(i)]
    except:
        a = ''
    return a

@register.simple_tag
def to_int(to):
    to = int(to)
    return to

@register.filter
def obj(indexable, i):
    return indexable[i]

@register.filter
def sub(value, i):
    return int(value)-int(i)
