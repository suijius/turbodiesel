# coding=cp1251
from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required

from metadata_view import EntityCreate, EntityEdit, PropertyCreate, PropertyEdit
from metamodel_view import CustomEntityUnitCreate, CustomEntityUnitEdit
from form_application import ApplicationEdit, ApplicationCreate, ApplicationDelete
from form_application_page import ApplicationPageEdit, ApplicationPageCreate
from turbodiesel.administration.form_extimage import ExtImageCreate
from form_extfilter import ExtFilterCreate, ExtFilterEdit
from form_extcode import ExtCodeCreate, ExtCodeEdit
from form_exttemplate import ExtTemplateCreate, ExtTemplateEdit
from form_extworkflow import ExtWorkflowCreate, ExtWorkflowEdit
from form_extstatus import ExtStatusCreate, ExtStatusEdit
from form_extuser import ExtUserEdit, ExtUserCreate


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
                       (r'^application/(.*)/entity/$', 'turbodiesel.administration.metamodel_view.entity'),


                       (r'^$', 'turbodiesel.administration.metamodel_view.home'),
                       (r'^application/(.*)/entity/create/', login_required(EntityCreate.as_view())),
                       (r'^application/(.*)/entity/(.*)/edit/', login_required(EntityEdit.as_view())),


                       (r'^application/(.*)/page/create/$', login_required(ApplicationPageCreate.as_view())),
                       (r'^application/(.*)/page/(.*)/edit/$', login_required(ApplicationPageEdit.as_view())),
                       (r'^application/(.*)/extension/extfilter/(.*)/edit/$', login_required(ExtFilterEdit.as_view())),
                       (r'^application/(.*)/extension/extcode/(.*)/edit/$', login_required(ExtCodeEdit.as_view())),
                       (r'^application/(.*)/extension/extuser/(.*)/edit/$', login_required(ExtUserEdit.as_view())),
                       (r'^application/(.*)/extension/template/(.*)/edit/$', login_required(ExtTemplateEdit.as_view())),
                       (r'^application/(.*)/extension/extworkflow/(.*)/edit/$', login_required(ExtWorkflowEdit.as_view())),
                       (r'^application/(.*)/extension/extstatus/(.*)/edit/$', login_required(ExtStatusEdit.as_view())),
                       (
                       r'^application/(.*)/extension/(.*)/(.*)/edit/$', login_required(CustomEntityUnitEdit.as_view())),
                       (r'^application/create/$', login_required(ApplicationCreate.as_view())),
                       (r'^application/(.*)/edit/$', login_required(ApplicationEdit.as_view())),
                       (r'^application/(.*)/delete/$', login_required(ApplicationDelete.as_view())),
                       (r'^application/$', 'turbodiesel.administration.metamodel_view.home'),

                       # (r'^application/(.*)/picture/insert/$', 'administration.metamodel_view.picture_insert'),
                       #    (r'^application/(.*)/picture/(.*)/delete/$', 'administration.metamodel_view.picture_delete'),
                       (r'^application/(.*)/extension/extimage/create/$', login_required(ExtImageCreate.as_view())),
                       (r'^application/(.*)/extension/extfilter/create/$', login_required(ExtFilterCreate.as_view())),
                       (r'^application/(.*)/extension/extcode/create/$', login_required(ExtCodeCreate.as_view())),
                       (r'^application/(.*)/extension/extuser/create/$', login_required(ExtUserCreate.as_view())),
                       (r'^application/(.*)/extension/template/create/$', login_required(ExtTemplateCreate.as_view())),
                       (r'^application/(.*)/extension/extworkflow/create/$', login_required(ExtWorkflowCreate.as_view())),
                       (r'^application/(.*)/extension/extstatus/(.*)/create/$', login_required(ExtStatusCreate.as_view())),
                       (r'^application/(.*)/extension/(.*)/create/(.*)/(.*)/$', login_required(CustomEntityUnitCreate.as_view())),
                       (r'^application/(.*)/extension/(.*)/create/$', login_required(CustomEntityUnitCreate.as_view())),
                       (r'^application/(.*)/extension/(.*)/$', 'turbodiesel.administration.metamodel_view.extension'),


                       (r'^data/application/$', 'turbodiesel.administration.data.application'),
                       (r'^data/page/(.*)$', 'turbodiesel.administration.data.page'),
                       (r'^data/picture/(.*)$', 'turbodiesel.administration.data.picture'),
                       (r'^data/entity/(.*)/$', 'turbodiesel.administration.data.entity'),
                       (r'^data/property/(.*)/(.*)$', 'turbodiesel.administration.data.property'),
                       (r'^data/extension/(.*)/(.*)$', 'turbodiesel.administration.data.extension'),
                       (r'^data/history/application/(.*)/(.*)/(.*)$', 'turbodiesel.administration.data.history'),
)