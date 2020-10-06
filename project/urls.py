from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from labconsole.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^console/(?P<server>[\S]+)$', console),
    url(r'^start/(?P<server>[\S]+)$', start_vm),
    url(r'^stop/(?P<server>[\S]+)$', stop_vm),
    url(r'^restart/(?P<server>[\S]+)$', restart_vm),
    url(r'^rebuild/(?P<server>[\S]+)/(?P<name>.*?)/(?P<image>[\S]+)$', rebuild_vm),
    url(r'^rescue/(?P<server>[\S]+)/(?P<image>.*)$', rescue_vm),
    url(r'^unrescue/(?P<server>[\S]+)$', unrescue_vm),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
