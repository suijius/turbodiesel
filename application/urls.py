# coding=cp1251
from django.conf.urls.defaults import *
# from view import EntityCreate, EntityEdit, PropertyCreate
'''

'''

urlpatterns = patterns('',
                       (r'^(.*)$', 'application.view.home'),
                       #    (r'^entity/custom/create/', EntityCreate.as_view()),
                       #    (r'^entity/custom/(.*)/edit/$', EntityEdit.as_view()),
                       ##    (r'^entity/([^//]*)/(.*)$', 'administration.view.operation'),
                       ##    (r'^entity/custom/(.*)$', 'administration.view.operation'),
                       ##    (r'^entity/(.*)', 'administration.view.entity'),
                       #    (r'^entity/custom/(.*)/property/create/', PropertyCreate.as_view()),
                       #    (r'^entity/custom/$', 'administration.view.entity'),
                       #    (r'^entity/system/$', 'administration.view.entity'),
                       #    (r'^data/entity/(.*)$', 'administration.data.entity'),
                       #    (r'^data/properties/(.*)$', 'administration.data.property'),
)

