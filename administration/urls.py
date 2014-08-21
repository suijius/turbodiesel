# coding=cp1251
from django.conf.urls import patterns, include, url
from metadata_view import EntityCreate, EntityEdit, PropertyCreate, PropertyEdit
from metamodel_view import CustomEntityUnitCreate, CustomEntityUnitEdit

from form_application import ApplicationEdit, ApplicationCreate
from form_application_page import ApplicationPageEdit, ApplicationPageCreate
from form_extimage import ExtImageCreate
from form_extfilter import ExtFilterCreate, ExtFilterEdit
from form_extcode import ExtCodeCreate, ExtCodeEdit
from form_exttemplate import ExtTemplateCreate, ExtTemplateEdit
from form_extworkflow import ExtWorkflowCreate, ExtWorkflowEdit
from form_extstatus import ExtStatusCreate, ExtStatusEdit
from form_extuser import ExtUserEdit, ExtUserCreate

from django.contrib.auth.decorators import login_required, permission_required


'''
admin - общий адрес для административного интерфейса
admin/entity/system - системные сущности 
admin/entity/custom - пользовательские сущности
    ./create - создание сущности
    ./<entity_name> - редактирование сущности
    ./<entity_name>/property/create - создание аттрибута сущности
    ./<entity_name>/property/<property_name> - редактирование аттрибута
'''

urlpatterns = patterns('',
                       (r'^application/(.*)/entity/(.*)/property/create/', login_required(PropertyCreate.as_view())),
                       (r'^application/(.*)/entity/(.*)/property/(.*)/edit/$', login_required(PropertyEdit.as_view())),
                       (r'^application/(.*)/entity/$', 'administration.metamodel_view.entity'),


                       (r'^$', 'administration.metamodel_view.home'),
                       (r'^application/(.*)/entity/create/', login_required(EntityCreate.as_view())),
                       (r'^application/(.*)/entity/(.*)/edit/', login_required(EntityEdit.as_view())),


                       (r'^application/(.*)/page/create/$', login_required(ApplicationPageCreate.as_view())),
                       (r'^application/(.*)/page/(.*)/edit/$', login_required(ApplicationPageEdit.as_view())),
                       (r'^application/(.*)/extension/ext_filter/(.*)/edit/$', login_required(ExtFilterEdit.as_view())),
                       (r'^application/(.*)/extension/ext_code/(.*)/edit/$', login_required(ExtCodeEdit.as_view())),
                       (r'^application/(.*)/extension/ext_user/(.*)/edit/$', login_required(ExtUserEdit.as_view())),
                       (r'^application/(.*)/extension/ext_template/(.*)/edit/$',
                        login_required(ExtTemplateEdit.as_view())),
                       (r'^application/(.*)/extension/ext_workflow/(.*)/edit/$',
                        login_required(ExtWorkflowEdit.as_view())),
                       (r'^application/(.*)/extension/ext_status/(.*)/edit/$', login_required(ExtStatusEdit.as_view())),
                       (
                       r'^application/(.*)/extension/(.*)/(.*)/edit/$', login_required(CustomEntityUnitEdit.as_view())),
                       (r'^application/create/$', login_required(ApplicationCreate.as_view())),
                       (r'^application/(.*)/edit/$', login_required(ApplicationEdit.as_view())),
                       (r'^application/$', 'administration.metamodel_view.home'),
                       # (r'^application/(.*)/picture/insert/$', 'administration.metamodel_view.picture_insert'),
                       #    (r'^application/(.*)/picture/(.*)/delete/$', 'administration.metamodel_view.picture_delete'),
                       (r'^application/(.*)/extension/ext_image/create/$', login_required(ExtImageCreate.as_view())),
                       (r'^application/(.*)/extension/ext_filter/create/$', login_required(ExtFilterCreate.as_view())),
                       (r'^application/(.*)/extension/ext_code/create/$', login_required(ExtCodeCreate.as_view())),
                       (r'^application/(.*)/extension/ext_user/create/$', login_required(ExtUserCreate.as_view())),
                       (r'^application/(.*)/extension/ext_template/create/$', login_required(ExtTemplateCreate.as_view())),
                       (r'^application/(.*)/extension/ext_workflow/create/$', login_required(ExtWorkflowCreate.as_view())),
                       (r'^application/(.*)/extension/ext_status/(.*)/create/$', login_required(ExtStatusCreate.as_view())),
                       (r'^application/(.*)/extension/(.*)/create/(.*)/(.*)/$', login_required(CustomEntityUnitCreate.as_view())),
                       (r'^application/(.*)/extension/(.*)/create/$', login_required(CustomEntityUnitCreate.as_view())),
                       (r'^application/(.*)/extension/(.*)/$', 'administration.metamodel_view.extension'),


                       (r'^data/application/$', 'administration.data.application'),
                       (r'^data/page/(.*)$', 'administration.data.page'),
                       (r'^data/picture/(.*)$', 'administration.data.picture'),
                       (r'^data/entity/(.*)/$', 'administration.data.entity'),
                       (r'^data/property/(.*)/(.*)$', 'administration.data.property'),
                       (r'^data/extension/(.*)/(.*)$', 'administration.data.extension'),
                       (r'^data/history/application/(.*)/(.*)/(.*)$', 'administration.data.history'),
)

