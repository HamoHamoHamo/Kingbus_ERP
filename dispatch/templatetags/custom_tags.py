from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.simple_tag
def to_int(to):
    to = int(to)
    return to