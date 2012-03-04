from django.template.defaultfilters import stringfilter
from django import template
import logging
import re

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
@stringfilter
def fix_entities(str):
    if str is None or str == '':
        return ''
    try:
        newstr = str
        newstr = newstr.replace("&quot;", "\"")
        newstr = newstr.replace("&amp;", "&")
        return newstr
    except:
        return str
