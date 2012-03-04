from django.template.defaultfilters import stringfilter
from django import template

import re

register = template.Library()

@register.filter
@stringfilter
def strip(string): 
    try:
        return string.strip()
    except:
        return string
