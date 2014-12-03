# coding=cp1251
import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import models

from turbodiesel.models import Entity, Property, Application, Page, get_application_instance, get_entity_instance, get_model#, ExtWorkflow

# import reversion

def get_params(request, application_alias, extension_alias):
    fields = []
    preext = False
    key_field = 'id'
    # classname = ''
    # classname_list = [ext['ClassName'] for ext in settings.EXTENSIONS if ext['TableName'] == extension_alias]
    # if len(classname_list):
    #     classname = classname_list[0]
    #
    # if globals().__contains__(classname):
    #     model = globals()[classname]
    #     preext = True
    # else:
    #     instance = get_entity_instance(request, extension_alias, application_alias)
    #     fields = Property.objects.filter(parent_entity=instance)
    #     model = create_model(instance, {})

    model = get_model(request, extension_alias, application_alias)

    if model is not None and len(fields) == 0:
        # if classname == 'dbTemplates':
        #     model = model.Template
        fields = [{'name': field.name, 'visible': True, 'label': field.verbose_name} for field in model._meta.fields if field.name != 'site']
        key_field = fields[0]['name']

    return {'fields': fields, 'model': model, 'preext': preext, 'key_field': key_field}


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
    data = [{'Name': application.name, 'Title': application.title, 'TableName': application.alias,
             'Image': application.logotype.name} for application in Application.objects.all()]
    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


@login_required
def page(request, application_alias):
    callback = request.GET['callback']

    application = get_application_instance(application_alias, request)
    pages = Page.objects.filter(site=application.site)
    data = []
    for field in pages:
        value = {}
        for meta in field._meta.fields:
            value[meta.name] = truncate(field.__dict__[str(meta.name if meta.attname is None else meta.attname)],
                                        meta.name)
        data.append(value)

    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


@login_required
def picture(request, application_alias):
    callback = request.GET['callback']

    application = get_application_instance(application_alias, request)
    images = Image.objects.filter(site=application.site)
    data = [{'Name': image.name, 'Image': image.image.name} for image in images]

    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


@login_required
def entity(request, application_alias):
    callback = request.GET['callback']
    data = get_custom_entity(application_alias, request)
    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


def get_custom_entity(application_alias, request):
    application = get_application_instance(application_alias, request)
    data = [{'Name': entity.name, 'TableName': entity.alias, 'Image': entity.image.name, 'text': ''} for entity in
            Entity.objects.filter(site=application.site)]
    if len(data):
        data[0]['text'] = u'Пользовательские расширения'
    return data


@login_required
def property(request, application_alias, entity_alias):
    callback = request.GET['callback']
    entity = get_entity_instance(request, entity_alias, application_alias)
    properties = Property.objects.filter(parent_entity=entity)
    data = [{'Name': property.label, 'TableName': property.name} for property in properties]

    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


@login_required
def extension(request, application_alias, extension_alias):
    # callback = request.GET.get('callback')
    model = get_model(request, extension_alias, application_alias)

    if model is not None:
        application = get_application_instance(application_alias, request)
        data = []
        data_array = []
        if request.GET.__contains__('expression'):
            expression = request.GET['expression']
            entity = Entity.objects.filter(entity_id=request.GET.get('entity'), site=application.site)
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
            kwargs = {request.GET['filter[filters][0][field]']: detail_model.objects.get(request=value,
                                                                                         application_alias=None)}
            if len(data_array):
                data_array = data_array.__or__(model.objects.filter(**kwargs))
            else:
                data_array = model.objects.filter(**kwargs)
                #data_array = data_array.extra(**eval("dict(%s)" % request.GET['extra']))

        else:
            if extension_alias == 'template':
                data_array = model.objects.filter(sites=application.site)
            elif extension_alias == 'extimage' or extension_alias == 'extfilter' or extension_alias == 'extcode' or extension_alias == 'extworkflow':
                data_array = model.objects.filter(site=application.site)
            # elif extension_alias == 'extstatus' or extension_alias == 'extedge':
            #     workflow_id = request.GET.get('workflow')
            #     wf_list = ExtWorkflow.objects.filter(workflow_id=workflow_id)
            #     if len(wf_list):
            #         data_array = model.objects.filter(workflow=wf_list[0])
            else:
                data_array = model.objects.all()

        params = get_params(request, application_alias, extension_alias)
        key_field = params['key_field']

        for row in data_array:
            value = {}
            for meta in row._meta.fields:
                name = str(meta.name if meta.attname is None else meta.attname)
                value[name] = row.__dict__[name]
                if type(meta) is not models.ImageField:
                    value[name] = truncate(value[name], name)
                if meta.name != meta.attname:
                    try:
                        value[meta.name] = row.__getattribute__(str(meta.name))
                        value[meta.name] = truncate(value[meta.name], meta.name)
                    except:
                        value[meta.name] = ''
            for meta in data_array.query.extra_select.keys():
                value[meta] = row.__dict__[str(meta)]
                value[meta] = truncate(value[meta], meta)
            value['key_field'] = value[key_field]
            data.append(value)

        # value = str(callback) + '(' + json.dumps(data) + ')'
        # response = HttpResponse(value)
        # response["Content-Type"] = "application/json"
        # return response
        return data
    else:
        # value = str(callback) + '([])'
        # response = HttpResponse(value)
        # response["Content-Type"] = "application/json"
        # return response
        return []


@login_required
def history(request, application_alias, entity_type, entity_alias):
    data = []
    callback = request.GET['callback']
    try:
        instance = None
        if entity_type == 'application':
            instance = get_application_instance(application_alias, request)
        else:
            model = get_model(request, entity_type, application_alias)
            instance_list = model.objects.filter(code_id=entity_alias)
            if len(instance_list):
                instance = instance_list[0]

        # elif entity_type == 'extcode':
        #     model = get_model(request, entity_type, application_alias)
        #     instance_list = model.objects.filter(code_id=entity_alias)
        #     if len(instance_list):
        #         instance = instance_list[0]
        # elif entity_type == 'exttemplate':
        #     instance_list = dbTemplates.Template.objects.filter(id=entity_alias)
        #     if len(instance_list):
        #         instance = instance_list[0]

        version_list = reversion.get_unique_for_object(instance)
        # entity = get_entity_instance(entity_alias, application_alias)
        # properties = Property.objects.filter(parent_entity = entity)
        data = [{'id': version.id, 'revision': version.revision_id, 'data': version.serialized_data,
                 'date': str(version.revision.date_created), 'user': version.revision.user.username} for version in
                version_list]

    except:
        pass

    value = str(callback) + '(' + json.dumps(data) + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response