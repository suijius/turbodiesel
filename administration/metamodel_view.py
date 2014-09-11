# coding=cp1251
#from django.contrib.auth import logout
#import django.contrib.auth 
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response  #, render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.forms.widgets import TextInput, Select, Textarea, DateTimeInput, CheckboxInput, DateInput
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.base import ModelBase
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor
#from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import PermissionDenied

import localization
import data
from metamodel.models import Entity, Property, Application, Page, ExtImage, ExtWorkflow, ExtFilter, ExtCode, create_model, get_application_instance, get_entity_instance, UserProfile
from dbtemplates import models as dbTemplates
import settings
import json
#from application.data import get_data
import application.data as app_data


@login_required
def home(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    apps = [{'Name': application.name, 'Title': application.title, 'TableName': application.alias,
             'Image': application.logotype.name} for application in Application.objects.all()]
    return render_to_response('administration/application.html',
                              {'request': request, 'messages': messages.get_messages(request), 'applications': apps})


#@login_required
#def picture_insert(request, application_alias):
#    if not request.user.is_superuser:
#        raise PermissionDenied
#    return render_to_response('administration/application.html', {'request': request, 'messages': messages.get_messages(request)    })
#
#@login_required
#def picture_delete(request, application_alias, picture_name):
#    if not request.user.is_superuser:
#        raise PermissionDenied
#    return render_to_response('administration/application.html', {'request': request, 'messages': messages.get_messages(request)    })


def get_params(request, application_alias, extension_alias):
    fields = []
    preext = False
    model = None
    classname = ''
    classname_list = [ext['ClassName'] for ext in settings.EXTENSIONS if ext['TableName'] == extension_alias]
    if len(classname_list):
        classname = classname_list[0]
    key_field = 'id'
    if globals().__contains__(classname):
        model = globals()[classname]
        preext = True
    else:
        instance = get_entity_instance(request, extension_alias, application_alias)
        fields = Property.objects.filter(parent_entity=instance)
        model = create_model(instance, {})

    if model is not None and len(fields) == 0:
        if classname == 'dbTemplates':
            model = model.Template
        fields = [{'name': field.name, 'visible': True, 'label': field.verbose_name} for field in model._meta.fields if
                  field.name != 'application']
        key_field = fields[0]['name']

    return {'fields': fields, 'model': model, 'preext': preext, 'key_field': key_field}


@login_required
def extension(request, application_alias, extension_alias):
    if not request.user.is_superuser:
        raise PermissionDenied
    application, default = get_application_instance(application_alias, request)
    extension_list = [ext for ext in settings.EXTENSIONS + data.get_custom_entity(application_alias, request) if
                      ext['TableName'] == extension_alias]

    params = get_params(request, application_alias, extension_alias)

    fields = params['fields']
    model = params['model']
    preext = params['preext']
    key_field = params['key_field']

    # detail_list = model._meta.get_all_related_objects()
    # detail = {}
    # if len(detail_list):
    #     detail['extension'] = detail_list[0].model._meta.module_name
    #     detail['field'] = detail_list[0].field.name
    #     detail['model'] = detail_list[0].field.rel.to._meta.module_name
    #     entity = Entity.objects.filter(alias=detail['extension'], application=application)
    #     detail['fields'] = []
    #     if entity is not None:
    #         detail['fields'] = Property.objects.filter(parent_entity=entity)
    #     else:
    #         detail['fields'] = detail_list[0].model._meta.fields

    ext_data = data.extension(request, application_alias, extension_alias)

    return render_to_response('administration/extension.html',
                              {'request': request, 'messages': messages.get_messages(request),
                               'extension': extension_list[0], 'application': application, 'extension_fields': fields,
                               'preext': preext, 'key_field': key_field, 'extension_data': ext_data})


@login_required
def entity(request, application_alias):
    if not request.user.is_superuser:
        raise PermissionDenied
    application, default = get_application_instance(application_alias, request)
    entity_data = data.get_custom_entity(application_alias, request)

    return render_to_response('administration/entity.html',
                              {'request': request, 'messages': messages.get_messages(request),
                               'application': application, 'entity': entity_data})


def prepare_form(form, withEditor=True):
    for field_name in form.fields:
        if type(form[field_name].field.widget) == CheckboxInput:
            continue
        if type(form[field_name].field.widget) == TextInput:
            if field_name == 'tags':
                form[field_name].field.widget.attrs.__setitem__('class', "k-input text span tags_input")
            else:
                form[field_name].field.widget.attrs.__setitem__('class', "k-input text span")
        elif type(form[field_name].field.widget) == Select:
            form[field_name].field.widget.attrs.__setitem__('class', "select span_select")
        elif type(form[field_name].field.widget) == DateTimeInput:
            form[field_name].field.widget.attrs.__setitem__('class', "datetime span")
        elif type(form[field_name].field.widget) == DateInput:
            form[field_name].field.widget.attrs.__setitem__('class', "date span")
        elif type(form[field_name].field.widget) == Textarea and withEditor:
            form[field_name].field.widget.attrs.__setitem__('class', "textarea span")
        else:
            form[field_name].field.widget.attrs.__setitem__('class', "span")


class TurboDieselCreateView(CreateView):
    object = None
    action = 'entity_action_create'
    caption = 'entity_type_system'

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', self.caption),
            'action': localization.get_string(request, 'ru', self.action),
            'messages': messages.get_messages(request),
            'application': kwargs.get('application', []),
            'href': '/admin/entity/custom'
        }
        return context

    def prepost_raw(self, request):
        self.preget_raw(request)
        if len(request.FILES) > 0 and request.FILES.get('image') <> 0:
            request.FILES['image'].name = request.POST.get('alias') + '.png'
        if len(request.FILES) > 0 and request.FILES.get('logotype') <> 0:
            request.FILES['logotype'].name = request.POST.get('alias') + '.png'

    def prepost(self, request, application_alias=None):
        self.prepost_raw(request)
        if application_alias is not None:
            return get_application_instance(application_alias, request)[0]

    def preget_raw(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

    def preget(self, request, application_alias=None):
        self.preget_raw(request)
        if application_alias is not None:
            return get_application_instance(application_alias, request)[0]


class TurboDieselUpdateView(UpdateView):
    object = None
    action = 'entity_action_edit'
    caption = 'entity_type_system'

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', self.caption),
            'action': localization.get_string(request, 'ru', self.action),
            'messages': messages.get_messages(request),
            'application': kwargs.get('application', []),
            'href': '/admin/entity/custom',
            'related_objects': kwargs.get('related_objects', []),
            'params': kwargs.get('params', []),
            'extension_alias': kwargs.get('extension_alias', []),
            'extension_id': kwargs.get('extension_id', [])
        }
        return context

    def prepost(self, request, application_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        if len(request.FILES) > 0 and request.FILES.get('image') <> 0:
            request.FILES['image'].name = request.POST.get('alias') + '.png'
        if len(request.FILES) > 0 and request.FILES.get('logotype') <> 0:
            request.FILES['logotype'].name = request.POST.get('alias') + '.png'
        return get_application_instance(application_alias, request)[0]

    def preget(self, request, application_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        return get_application_instance(application_alias, request)[0]


class CustomEntityUnitCreate(CreateView):
    template_name = 'administration/create.html'
    object = None

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', 'entity_type_custom'),
            'href': '/admin/entity/custom',
            'action': localization.get_string(request, 'ru', 'entity_action_create'),
            'messages': messages.get_messages(request),
            'application': kwargs['application']
        }
        return context

    def get_parent(self, request, parent_alias, parent_id, application_alias, extension_alias):
        inline = {}
        model_instance = get_entity_instance(request, parent_alias, application_alias)
        model = create_model(model_instance, inline)
        parent_instance = model.objects.filter(id=parent_id)[0]
        params_dict = dict(parent_instance._base_manager.model.__dict__)
        parent_field = ''
        for key in params_dict:
            if type(params_dict[key]) is ForeignRelatedObjectsDescriptor:
                related_object = params_dict[key].related
                if extension_alias == related_object.var_name:
                    parent_field = related_object.field.column
        return {'parent_field': parent_field, 'parent_instance': parent_instance}

    def createForm(self, application_alias, entity, exclude=()):
        inline = {}
        model = create_model(entity, inline)
        properties = {'Meta': type('Meta', (), {'model': model, 'exclude': exclude})}
        return type(entity.alias.encode('cp1251'), (ModelForm,), properties)

    def get(self, request, application_alias, extension_alias, parent_alias=None, parent_id=None):
        if not request.user.is_superuser:
            raise PermissionDenied
        instance = get_entity_instance(request, extension_alias, application_alias)
        application, default = get_application_instance(application_alias, request)
        exclude = ()
        parent_field = ''
        if parent_alias is not None:
            parent = self.get_parent(request, parent_alias, parent_id, application_alias, extension_alias)
            exclude = (parent['parent_field'],)
        form = self.createForm(application_alias, instance, exclude)()
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias, extension_alias, parent_alias=None, parent_id=None):
        if not request.user.is_superuser:
            raise PermissionDenied
        instance = get_entity_instance(request, extension_alias, application_alias)
        application, default = get_application_instance(application_alias, request)
        form = self.createForm(application_alias, instance)(request.POST, request.FILES)
        if parent_alias is not None:
            post = request.POST
            parent = self.get_parent(request, parent_alias, parent_id, application_alias, extension_alias)
            post[parent['parent_field']] = parent_id
            form = self.createForm(application_alias, instance)(post, request.FILES)
        #            form.instance[parent['parent_field']] = parent['parent_instance']

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))


class CustomEntityUnitEdit(TurboDieselUpdateView):
    template_name = 'administration/create.html'
    action = 'entity_action_edit'
    caption = 'entity_type_system'


    def createForm(self, application_alias, entity, entity_id):
        inline = {}
        model = entity
        if type(entity) is not ModelBase:
            model = create_model(entity, inline)
        instance = model.objects.filter(id=entity_id)[0]
        properties = {'Meta': type('Meta', (), {'model': model})}
        return [type(entity.alias.encode('cp1251'), (ModelForm,), properties), instance]

    def get(self, request, application_alias, extension_alias, extension_id):
        instance = get_entity_instance(request, extension_alias, application_alias)
        application = self.preget(request, application_alias)
        params = self.createForm(application_alias, instance, extension_id)
        form = params[0](instance=params[1])
        params_dict = dict(params[1]._base_manager.model.__dict__)
        related_objects = {}
        params_ext = {}
        fields = []
        for key in params_dict:
            if type(params_dict[key]) is ForeignRelatedObjectsDescriptor:
                related_object = params_dict[key].related
                entity_list = Entity.objects.filter(alias=related_object.var_name)
                if len(entity_list):
                    if not entity_list[0].service:
                        data_array = related_object.model.objects.filter(**eval("dict(%s=%s)" % (related_object.field.column, params[1].id)))
                        related_objects[related_object.model.entity] = app_data.get_data(data_array)#json.dumps(app_data.get_data(data_array))
                        params_ext[related_object.model.entity] = get_params(request, application_alias,
                                                                             related_object.model.entity.alias)
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application,
                                          related_objects=related_objects, params=params_ext,
                                          extension_alias=extension_alias, extension_id=extension_id))

    def post(self, request, application_alias, extension_alias, enxtension_id):
        instance = get_entity_instance(request, extension_alias, application_alias)
        application = self.prepost(request, application_alias)
        params = self.createForm(application_alias, instance, enxtension_id)
        for item in request.POST:
            while request.POST[item].__contains__('&lt') or request.POST[item].__contains__('&gt') or request.POST[
                item].__contains__('&amp'):
                request.POST[item] = request.POST[item].replace('&lt;', '<').replace('&gt;', '>').replace('&amp;',
                                                                                                          '&').replace(
                    '&nbsp;', ' ')
        form = params[0](request.POST, request.FILES, instance=params[1])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))
