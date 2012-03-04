import logging
import jsonpickle
import re
import StringIO
import simplejson
import tempfile
import hashlib
import httplib2
import cPickle as pickle
import json
import urllib

from django.http import HttpResponse
from django.shortcuts import render as django_render

from grandcentral.lib.jsonserializer import JSONSerializer

logger = logging.getLogger(__name__)

'''
FileIterWrapper is an block-oriented file wrapper for Django.
Instead of doing:
    return HttpResponse(open('/path/to/file'))
Do:
    return HttpResponse(FileIterWrapper(open('/path/to/file')))
'''  
class FileIterWrapper(object):
    def __init__(self, filelike, block_size = 1024**2):
        self.filelike = filelike
        self.block_size = block_size
    
    def _next(self):
        data = self.filelike.read(self.block_size)
        if data:
            return data
        else:
            raise StopIteration
    
    def __iter__(self):
        return self


def load_url(url, method='GET', body=None, headers=None, timeout_ms=8000):
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    if body is not None:
        if headers is not None:
            response, content = h.request(url, method=method, body=urllib.urlencode(body), headers=headers)
        else:
            response, content = h.request(url, method=method, body=urllib.urlencode(body))
    else:
        if headers is not None:
            response, content = h.request(url, method=method, headers=headers)
        else:
            response, content = h.request(url, method=method)

    if response.status == 200:
        return content
    else:
        return None
   

def is_numeric(str, func=float):
    """ Simple function to test whether a string is actually numeric. Second optional parameter is the test function. """
    try:
        i = func(str)
    except:
        return False
    return True

def render_new(request, *args, **kwargs):
    """
    Wraps django.shortcuts.render() to account for different templates based on the user agent as well as leveraging the API.
    """
    httpresponse_kwargs = {
        'content_type': kwargs.pop('content_type', None),
        'status': kwargs.pop('status', None),
    }
    
    if request.REQUEST.get("api", "") == "json":
        pass

    return django_render(request. args, kwargs)


def cache_function(length):
    """
    A variant of the snippet posted by Jeff Wheeler at
    http://www.djangosnippets.org/snippets/109/
    
    Caches a function, using the function and its arguments as the key, and the return
    value as the value saved. It passes all arguments on to the function, as
    it should.
    
    The decorator itself takes a length argument, which is the number of
    seconds the cache will keep the result around.
    
    It will put in a MethodNotFinishedError in the cache while the function is
    processing. This should not matter in most cases, but if the app is using
    threads, you won't be able to get the previous value, and will need to
    wait until the function finishes. If this is not desired behavior, you can
    remove the first two lines after the ``else``.
    """
    def decorator(func):
        def inner_func(*args, **kwargs):
            from django.core.cache import cache
            
            raw = [func.__name__, func.__module__, args, kwargs]
            pickled = pickle.dumps(raw, protocol=pickle.HIGHEST_PROTOCOL)
            key = hashlib.sha256(pickled).hexdigest()
            value = cache.get(key)
            if cache.has_key(key):
                return value
            else:
                # This will set a temporary value while ``func`` is being
                # processed. When using threads, this is vital, as otherwise
                # the function can be called several times before it finishes
                # and is put into the cache.
                class MethodNotFinishedError(Exception): pass
                cache.set(key, MethodNotFinishedError(
                    'The function %s has not finished processing yet. This \
value will be replaced when it finishes.' % (func.__name__)
                ), length)
                result = func(*args, **kwargs)
                cache.set(key, result, length)
                return result
        return inner_func
    return decorator

def to_integer(str, default_value):
    try:
        return int(str)
    except:
        return default_value

def render_json(params):
    jsonSerializer = JSONSerializer()
    try:
        return HttpResponse(jsonSerializer.serialize(params, use_natural_keys=False, ensure_ascii=False), mimetype='application/json')
    except:
        return HttpResponse(json.dumps(params), mimetype='application/json')

def json_success(request):
    result = {'success': 'true'}
    return render_json(result)

def json_failure(request, message):
    result = {'success': 'false', 
              'error': message}
    return render_json(result)

def currentuser(request):
    return {'user': request.user}

def mssql_escape(str):
    try:
        return str.replace("'", "''")
    except:
        return str