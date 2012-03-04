from django.contrib.auth.decorators import permission_required
from grandcentral.core.models import ApplicationPermissions, Application
from django.http import HttpResponseForbidden

import re

class PermissionRequiredMiddleware(object):
    
    def __init__(self):
        pass
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        #o = ApplicationPermissions.objects.get(application=application, user=request.user)
        r = re.compile("^/([^\/]+)\/")
        g = r.match(request.META['PATH_INFO'])
        if g is not None:
            application = g.groups()[0]
            app_obj = None
            try:
                app_obj = Application.objects.get(package="app_%s" % application)
            except:
                return None     # default = ALLOW, if application isn't found
            
            if app_obj is not None:
                per_obj = None
                try:
                    per_obj = ApplicationPermissions.objects.get(application=app_obj)
                except:
                    return None # default = ALLOW, if no permissions exist at all
                
                try:
                    per_obj = ApplicationPermissions.objects.get(application=app_obj, user=request.user)
                except:
                    try:
                        per_obj = ApplicationPermissions.objects.get(application=app_obj, user=None)
                        # This would be the default permission, for user=NULL.
                    except:
                        return HttpResponseForbidden()  # If any permissions exist for app, but not for user, DENY.
                
                if per_obj is not None:
                    if per_obj.permission == 'D':
                        return HttpResponseForbidden()

        return None
    