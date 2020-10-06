from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from labconsole.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^console/(?P<server>.*?)$', console),
    url(r'^start/(?P<server>.*?)$', start_vm),
    url(r'^stop/(?P<server>.*?)$', stop_vm),
    url(r'^restart/(?P<server>.*?)$', restart_vm),
    url(r'^rebuild/(?P<server>.*?)/(?P<name>.*?)/(?P<image>.*?)$', rebuild_vm),
    url(r'^rescue/(?P<server>.*?)/(?P<image>.*?)$', rescue_vm),
    url(r'^unrescue/(?P<server>.*?)$', unrescue_vm),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
