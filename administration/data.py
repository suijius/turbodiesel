# coding=cp1251
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from metamodel.models import Entity, Property, Application, Page, ExtImage, create_model, ExtFilter, get_application_instance, get_entity_instance, get_model, ExtWorkflow, ExtStatus, ExtEdge
from django.contrib import messages
from django.db import models
from django.core import serializers
from django.db.models import Avg, Max, Min, Count
import settings
from dbtemplates import models as dbTemplates
from django.db.models.base import ModelBase
#import reversion

def truncate(item, name):
    data = item
    if name != "image":
        if type(data) is not str and type(data) is not unicode:
            try:
                data = item.__unicode__()
            except:
                data = str(item)
    
        #return data
        if len(data) > 40:
            data = data[0:40] + " ..." 
    return data

@login_required
def application(request):
    callback = request.GET['callback']
    data = [{'Name': application.name,'Title': application.title, 'TableName':application.alias, 'Image' : application.logotype.name} for application in Application.objects.all()]
    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response

@login_required
def page(request, application_alias):
    callback = request.GET['callback']

    application, default = get_application_instance(application_alias, request)
    pages = Page.objects.filter(application = application)
    data = []
    for field in pages:
        value = {}
        for meta in field._meta.fields:
            value[meta.name] = truncate(field.__dict__[str(meta.name if meta.attname is None else meta.attname)], meta.name)
        data.append(value)
            
    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response    

@login_required
def picture(request, application_alias):
    callback = request.GET['callback']

    application, default = get_application_instance(application_alias, request)
    images = Image.objects.filter(application = application)
    data = [{'Name': image.name, 'Image':image.image.name} for image in images]

    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response    

@login_required
def entity(request, application_alias):
    callback = request.GET['callback']
    data = []
    data = get_custom_entity(application_alias, request)
    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


def get_system_entity():
    data = [{'Name': u'Сущности', 'TableName':'entity', 'Image':'turbodiesel/images/admin/entity.png'},
            {'Name': u'Аттрибуты', 'TableName':'property', 'Image':'turbodiesel/images/admin/property.png'},
            {'Name': u'Сущности-Аттрибуты', 'TableName':'entityproperty', 'Image':'turbodiesel/images/admin/entityproperty.png'},
            {'Name': u'Типы аттрибутов', 'TableName':'propertytype', 'Image':'turbodiesel/images/admin/propertytype.png'},
            {'Name': u'Типы аттрибутов интерфейса', 'TableName':'propertytypeui', 'Image':'turbodiesel/images/admin/propertytypeui.png'},
            {'Name': u'Приложения', 'TableName':'application', 'Image':'turbodiesel/images/admin/application.png'},
            ]
    return data

def get_custom_entity(application_alias, request):
    application, default = get_application_instance(application_alias, request)
    data = [{'Name': entity.name, 'TableName':entity.alias, 'Image' : entity.image.name, 'text':''} for entity in Entity.objects.filter(application = application)]
    if len(data):
        data[0]['text'] = u'<br/>Пользовательские расширения'
    return data

@login_required
def property(request, application_alias, entity_alias):
    callback = request.GET['callback']
    entity = get_entity_instance(request, entity_alias, application_alias)
    properties = Property.objects.filter(parent_entity = entity)
    data = [{'Name': property.label, 'TableName':property.name} for property in properties]

    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response    
    
@login_required
def extension(request, application_alias, extension_alias):
    callback = request.GET.get('callback', request.GET.get('$callback', '')) 
    model = get_model(request, extension_alias, application_alias)
  
    if model is not None:
        application, default = get_application_instance(application_alias, request)
        data = []
        data_array = []
        if request.GET.__contains__('expression'):
            expression = request.GET['expression']
            entity = Entity.objects.filter(entity_id = request.GET.get('entity', 0), application = application)
            if len(entity):
                entity_model = get_model(request, entity[0].alias, application_alias)
                expression_list = expression.split('|')
                for item in expression_list:
                    if len(data_array):
                        data_array = data_array.__or__(entity_model.objects.filter(**eval("dict(%s)" % item)))
                    else:
                        data_array = entity_model.objects.filter(**eval("dict(%s)" % item))
                data_array = data_array.extra(**eval("dict(%s)" % request.GET['extra']))
        elif request.GET.__contains__('filter[filters][0][value]'):
            value = request.GET['filter[filters][0][value]']
            detail_model = get_model(request, request.GET['filter[filters][0][model]'], application_alias)
            kwargs = {request.GET['filter[filters][0][field]']:detail_model.objects.get(id=value)}
            if len(data_array):
                data_array = data_array.__or__(model.objects.filter(**kwargs))
            else:
                data_array = model.objects.filter(**kwargs)
            #data_array = data_array.extra(**eval("dict(%s)" % request.GET['extra']))

        else:
            if extension_alias == 'ext_template':
                data_array = model.objects.filter(name__contains = application.alias)
            elif extension_alias == 'ext_image' or extension_alias == 'ext_filter' or extension_alias == 'ext_code'  or extension_alias == 'ext_workflow' :
                data_array = model.objects.filter(application = application)
            elif extension_alias == 'ext_status' or extension_alias == 'ext_edge':
                workflow_id = request.GET.get('workflow', 0)
                wf_list = ExtWorkflow.objects.filter(workflow_id = workflow_id)
                if len(wf_list):
                    data_array = model.objects.filter(workflow = wf_list[0])
            else:
                data_array = model.objects.all()
                
        for row in data_array:
            value = {}
            for meta in row._meta.fields:
                name = str(meta.name if meta.attname is None else meta.attname)
                value[name] = row.__dict__[name]
                if type(meta) is not models.ImageField:
                    value[name] = truncate(value[name], name)
                if meta.name <> meta.attname:
                    try:
                        value[meta.name] = row.__getattribute__(str(meta.name))
                        value[meta.name] = truncate(value[meta.name], meta.name)
                    except:
                        value[meta.name] = ''
            for meta in data_array.query.extra_select.keys():
                value[meta] = row.__dict__[str(meta)]
                value[meta] = truncate(value[meta], meta)
            data.append(value)
                       


        
        value = str(callback) + '(' + json.dumps(data) + ')'
        response = HttpResponse(value)
        response["Content-Type"] = "application/json"
        return response    
  
    else:
        value = str(callback) + '([])'
        response = HttpResponse(value)
        response["Content-Type"] = "application/json"
        return response    
    
    
    
@login_required
def history(request, application_alias, entity_type, entity_alias):
    data = []
    callback = request.GET['callback']
    try:
        instance = None
        if entity_type == 'application':
            instance, default = get_application_instance(entity_alias, request)
        elif entity_type == 'ext_code':
            model = get_entity_instance(request, entity_type, application_alias)
            instance_list = model.objects.filter(code_id = entity_alias)
            if len(instance_list):
                instance = instance_list[0]
        elif entity_type == 'ext_template':
            instance_list = dbTemplates.Template.objects.filter(id = entity_alias)
            if len(instance_list):
                instance = instance_list[0]
            
            
        version_list = reversion.get_unique_for_object(instance)
       # entity = get_entity_instance(entity_alias, application_alias)
       # properties = Property.objects.filter(parent_entity = entity)
        data = [{'id':version.id, 'revision': version.revision_id, 'data':version.serialized_data, 'date': str(version.revision.date_created), 'user':version.revision.user.username} for version in version_list]
    
    except:
        pass
    
    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response    
        