from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_at_index(object_list, index):
    return object_list[index]

@register.simple_tag            # 2
def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M")