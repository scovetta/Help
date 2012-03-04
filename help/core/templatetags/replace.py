from django.template.defaultfilters import stringfilter
from django import template

import re

register = template.Library()

@register.filter
@stringfilter
def replace(string, args):
    if string is None or args is None:
        return None
    try:
        search  = args.split(args[0])[1]
        replace = args.split(args[0])[2]
        return re.sub( search, replace, string )
    except:
        return string
