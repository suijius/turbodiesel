# coding=cp1251
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'turbodiesel.frontoffice.views.main'), # Dashboard, главная страница инструментария
)