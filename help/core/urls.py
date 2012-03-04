from django.conf.urls.defaults import patterns, include, handler404, handler500, url
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'help.core.views.HomeAction'),
)
