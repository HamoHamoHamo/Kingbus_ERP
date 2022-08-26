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
    #print("TEMPLATEINDEX", "LIST : ", indexable, "I : ", i)
    return indexable[i]

# @register.filter
# def regularly_cnt(order, date):
#     return order.objects.filter(departure_date__startswith=date).count()