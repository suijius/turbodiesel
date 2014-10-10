# coding=cp1251
from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
# import administration
#import application.urls

#import django

admin.autodiscover()

urlpatterns = patterns('',
                       #    (r'^admin_tools/', include('admin_tools.urls')),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^root/doc/', include('django.contrib.admindocs.urls')),
                       (r'^root/', include(admin.site.urls)),
                       (r'^admin/', include('turbodiesel.administration.urls')),
                       (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       (r'^logout/$', 'turbodiesel.administration.metadata_view.logout'),
                       (r'^error/$', 'turbodiesel.administration.metadata_view.error'),
                       (r'^couchdb/$', 'turbodiesel.document.view.default'),
                       (r'^couchdb/migrate$', 'turbodiesel.document.view.mysql2couchdb'),
                       (r'^couchdb/migrate/$', 'turbodiesel.document.view.mysql2couchdb'),
                       (r'^(.*)/$', 'turbodiesel.application.view.home'),
                       (r'^$', 'turbodiesel.application.view.main_url'),
)




