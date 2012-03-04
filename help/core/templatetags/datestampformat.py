import re
import logging
from datetime import datetime

from django.template.defaultfilters import stringfilter, date as filter_time
from django import template
register = template.Library()

logger = logging.getLogger(__name__)
    
@register.filter
def datestampformat(value, arg=None):
    logger.debug("value=%s, arg=%s" % (value,arg))
    t = datetime.fromtimestamp(int(value))
    logger.debug("Timestamp translated to: %s" % str(t))
    f = filter_time(t, arg)
    logger.debug("Timestamp rendered as %s" % f)
    return f
