from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter
def inCheck(value, i):
    if i in value:
        return "checked"
    else:
        return None

@register.filter
def index(indexable, i):
    #print("TEMPLATEINDEX", "LIST : ", indexable, "I : ", i)
    return indexable[int(i)]

@register.simple_tag
def to_int(to):
    to = int(to)
    return to


@register.filter
def sub(value, i):
    return int(value)-int(i)