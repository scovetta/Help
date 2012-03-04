from django.template.defaultfilters import stringfilter
from django import template
import logging
import re
import base64

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
@stringfilter
def base64encode(s):
    if s is None or s == '':
        return ''
    return base64.b64encode(s)

