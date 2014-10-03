# coding=cp1251
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from metamodel.models import Entity, Property, Application, Page, ExtImage, create_model, ExtFilter, \
    get_application_instance, get_entity_instance, get_model
from django.contrib import messages
from django.db import models
from django.core import serializers
from django.forms import ModelForm
import datetime


def get_data(data_array):
    data = []
    for row in data_array:
        value = {}
        for meta in row._meta._name_map:
            field = row.__getattribute__(str(meta))
            try:
                value[meta] = eval("dict(%s)" % field.__unicode__())
            except:
                try:
                    value[meta] = str(field)
                except:
                    value[meta] = field
            try:
                value[meta + "_id"] = field.__getattribute__("id")
                link_fields = Property.objects.filter(parent_entity=field.entity)
                value['_color_name'] = ''
                value['_size_name'] = ''
                for link_field in link_fields:
                    field_value = field.__getattribute__(link_field.name)

                    try:
                        if (type(field_value) is str or type(field_value) is unicode) and field_value[
                            0] <> '0' and field_value.isdigit():
                            field_value = int(field_value)
                        else:
                            field_value = str(field_value)
                    except:
                        field_value = field_value.encode('utf8')
                    value['_%s_%s' % (meta, link_field.name)] = field_value
            except:
                pass
        data.append(value)
    return data


def ajax(request, path):
    value = ''
    if len(path) > 2:
        callback = request.GET.get('callback')
        application = get_application_instance(path[0], request)

        filter_list = ExtFilter.objects.filter(site=application.site, alias=path[2])
        if len(filter_list) > 0:
            filter = filter_list[0]
            if len(path) > 3 and filter.expression.__contains__('%s'):
                expression = filter.expression % path[3]
            elif filter.expression.__contains__('session') and filter.expression.__contains__('%s'):
                expression = filter.expression % request.session.session_key
            else:
                expression = filter.expression

            entity = filter.entity
            entity_model = get_model(request, entity.alias, application.alias)
            expression_list = expression.split('|')
            data_array = []
            for item in expression_list:
                if len(data_array):
                    data_array = data_array.__or__(entity_model.objects.filter(**eval("dict(%s)" % item)))
                else:
                    data_array = entity_model.objects.filter(**eval("dict(%s)" % item))
            data_array = data_array.extra(**eval("dict(%s)" % filter.extra))

            data = get_data(data_array)
            value = json.dumps(data)
            if callback != '':
                value = str(callback) + '(' + value + ')'
    response = HttpResponse(value)
    response["Content-Type"] = "application/json"
    return response


def create_form(application_alias, entity):
    inline = {}
    model = create_model(entity, inline)
    properties = {'Meta': type('Meta', (), {'model': model})}
    return type(entity.alias.encode('cp1251'), (ModelForm,), properties)


def bag(request, path):
    application_alias = path[0]
    extension_alias = path[2]
    post = request.POST.copy()
    post["session"] = request.session.session_key
    #TODO suijius переделать вызов get_entity_instance
    entity = get_entity_instance(request, 'bag', application_alias)
    model_order = get_model(request, 'order', application_alias)
    order_list = model_order.objects.filter(status=1, session=request.session.session_key)
    order = []
    if len(order_list):
        order = order_list[0]
    else:
        model_order_status = get_model(request, 'order_status', application_alias)
        order = model_order(status=model_order_status.objects.get(request=1, application_alias=null),
                            session=request.session.session_key)
        order.save()
    post['order'] = order.id

    model = get_model(request, 'catalog_extra', application_alias)
    article = request.POST.get("article")
    if article:
        post["article"] = model.objects.get(request=article, application_alias=null).id

    form = create_form(application_alias, entity)(post, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, u'Товар успешно добавлен в корзину')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def order(request, path):
    application_alias = path[0]
    extension_alias = path[2]
    #TODO suijius переделать вызов get_entity_instance
    entity = get_entity_instance(request, extension_alias, application_alias)
    model_order = get_model(request, 'order', application_alias)
    model_order_status = get_model(request, 'order_status', application_alias)
    order_list = model_order.objects.filter(status=model_order_status.objects.get(request=1, application_alias=null),
                                            session=request.session.session_key)
    order = []
    if len(order_list):
        order = order_list[0]
    else:
        order = model_order(status=model_order_status.objects.get(request=1, application_alias=null),
                            session=request.session.session_key)
        order.save()
    post = request.POST.copy()
    post["session"] = request.session.session_key
    post["date"] = datetime.date.today()

    #TODO suijius переделать вызов get_entity_instance
    cat = get_entity_instance(request, 'catalog_extra', application_alias)
    inline = {}
    model = create_model(cat, inline)
    article = request.POST.get("article")
    if article:
        post["article"] = model.objects.get(request=article, application_alias=null).id

    post['status'] = 2
    form = create_form(application_alias, entity)(post, request.FILES, instance=order)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return render_to_response(self.get_context_data(form=form, request=request))


def form(request, path):
    application_alias = path[0]
    extension_alias = path[2]
    if globals().__contains__(extension_alias):
        return globals()[extension_alias](request, path)

    #TODO suijius переделать вызов get_entity_instance
    entity = get_entity_instance(request, extension_alias, application_alias)
    post = request.POST.copy()
    post["session"] = request.session.session_key

    #TODO suijius переделать вызов get_entity_instance
    cat = get_entity_instance(request, 'catalog_extra', application_alias)
    inline = {}
    model = create_model(cat, inline)
    article = request.POST.get("article")
    if article:
        post["article"] = model.objects.get(request=article, application_alias=null).id

    form = create_form(application_alias, entity)(post, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return render_to_response(self.get_context_data(form=form, request=request))


def robot(request):
    text = """
    Allow: /
    Disallow: /admin
    Disallow: /root
    """

    response = HttpResponse(text)
    response["Content-Type"] = "text/plain"
    return response






