import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def convert_to_markdown(values):
    return mark_safe(markdown.markdown(values, extensions=['markdown.extensions.fenced_code']))
