from django.conf import settings
from django import template
from django.templatetags.static import StaticNode
register = template.Library()

class CustomStaticNode(StaticNode):
    def url(self, context):
        version = settings.VERSION
        path = f'{super().url(context)}?v={version}'
        return path


@register.tag('static')
def do_static(parser, token):
    node = CustomStaticNode.handle_token(parser, token)
    return node