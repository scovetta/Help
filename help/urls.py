from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from settings.settings import PROJECT_ROOT
import glob
import re

admin.autodiscover()

# Nexus
import nexus
nexus.autodiscover()
urlpatterns = patterns('',
    ('^nexus/', include(nexus.site.urls)),
)

# Automatically import applications
# Rules are that directories within /grandcentral/ that start with 'app_FOO' are included
# and mapped to /FOO. Restrictions are that the patch may only be alphanum plus [\-_.].
for d in glob.glob(PROJECT_ROOT + "/help/app_*"):
    d = d.replace(PROJECT_ROOT + '/help/', '')
    d = d.replace('app_', '')
    r = re.compile("[^a-zA-Z0-9_\-\.]")
    if r.search(d) is None:     
	print "adding help.app_%s.urls" % d
        urlpatterns += patterns('', (r'^%s/' % d, include('help.app_%s.urls' % d)))


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

# Gargoyle
import gargoyle
gargoyle.autodiscover()

# Sentry
urlpatterns += patterns('',
    (r'^sentry/', include('sentry.web.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^media/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.SITE_ROOT + '/project/uploads',
        'show_indexes': True }),)

# Default URL patterns
urlpatterns += patterns('', (r'', include('help.core.urls')))

