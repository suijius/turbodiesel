# coding=cp1251
from django.conf.urls.defaults import *
from django.contrib import admin
import settings
#import administration
#import application.urls

#import django

admin.autodiscover()

urlpatterns = patterns('',
#    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    (r'^root/doc/', include('django.contrib.admindocs.urls')),
    (r'^root/', include(admin.site.urls)),
    (r'^admin/', include('administration.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/$', 'administration.metadata_view.logout'),
    (r'^error/$', 'administration.metadata_view.error'),
    (r'^(.*)/$', 'application.view.home'),
    (r'^$', 'application.view.main_url'),
)

