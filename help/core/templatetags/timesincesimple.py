import logging
import re
from datetime import datetime

from django.template.defaultfilters import stringfilter
from django import template
from django.utils.timesince import timesince

register = template.Library()

logger = logging.getLogger(__name__)

string_formats = ('%a, %d %b %Y %H:%M:%S %Z',
                  '%a, %d %b %Y %H:%M:%S +0000')

@register.filter
def timesincesimple(str):
    """ Formats a string date as something like "2 hours [ago]", using
        Django's timesince and some trial-and-error parsing.
    """
    
    # First, check to see if str is parseable by timesince
    result = str
    if not isinstance(str, datetime):
        for format in string_formats:
            result = parse_date(str, format)
            if result is not None:
                break
        if result is None:
            logger.warning("Unable to parse date: [%s]" % str)
            return str  # Can't parse
        
    result = timesince(result)
    final_string = result.split(",")[0]
    
    #special case, change <= 5 minutes to "a few minutes"
    minutes = final_string.split(" ")
    if 'minute' in minutes[1] and int(minutes[0]) <= 5:
        return "a few minutes"
    
    return final_string

def parse_date(string, format):
    try:
        return datetime.strptime(string, format)
    except:
        return None
