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
    url(r'^start/(?P<cloud>.*?)/(?P<server>.*?)$', start_vm),
    url(r'^stop/(?P<cloud>.*?)/(?P<server>.*?)$', stop_vm),
    url(r'^restart/(?P<cloud>.*?)/(?P<server>.*?)$', restart_vm),
    url(r'^rebuild/(?P<cloud>.*?)/(?P<server>.*?)/(?P<name>.*?)/(?P<image>.*?)$', rebuild_vm),
    url(r'^rescue/(?P<cloud>.*?)/(?P<server>.*?)/(?P<image>.*?)$', rescue_vm),
    url(r'^unrescue/(?P<cloud>.*?)/(?P<server>.*?)$', unrescue_vm),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
