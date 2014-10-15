# coding=cp1251
from django.conf.urls import patterns

'''

'''

urlpatterns = patterns('',
                       (r'^(.*)$', 'turbodiesel.application.view.home'),
)