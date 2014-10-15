# coding=cp1251
#from django.contrib.auth import logout
import django.contrib.auth
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.forms.widgets import TextInput, Select, Textarea, DateTimeInput, CheckboxInput, DateInput
from django.views.generic import CreateView, UpdateView
from django.contrib import messages

from turbodiesel.administration import localization

from turbodiesel.models import Entity, Property, get_application_instance, get_entity_instance


class EntityForm(ModelForm):
    class Meta:
        model = Entity
        exclude = ('editor', 'date_change', 'application')


class EntityCreate(CreateView):
    template_name = 'administration/create.html'
    object = None

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        application = get_application_instance(kwargs['application_alias'], request)

        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', 'entity_type_custom'),
            'href': '/admin/entity/custom',
            'action': localization.get_string(request, 'ru', 'entity_action_create'),
            'messages': messages.get_messages(request),
            'application': application
        }
        return context

    def get(self, request, application_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        form = EntityForm()
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application_alias=application_alias))

    def post(self, request, application_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        if len(request.FILES) > 0:
            request.FILES['image'].name = request.POST.get('alias') + '.png'
        application = get_application_instance(application_alias, request)
        form = EntityForm(request.POST, request.FILES)
        form.instance.application = application
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, request=request, application_alias=application_alias))


class EntityEdit(UpdateView):
    template_name = 'administration/entity_edit.html'
    object = None
    application = None

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        application = get_application_instance(kwargs['application_alias'], request)

        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', 'entity_type_custom'),
            'action': localization.get_string(request, 'ru', 'entity_action_edit'),
            'properties': kwargs.get('properties', []),
            'messages': messages.get_messages(request),
            'application': application
        }
        return context

    def post(self, request, application_alias, entity_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        if len(request.FILES) > 0:
            request.FILES['image'].name = request.POST.get('alias') + '.png'

        entity = get_entity_instance(request, entity_alias, application_alias)

        form = EntityForm(request.POST, request.FILES, instance=entity)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
        else:
            properties = Property.objects.get(parent_entity=entity)
            return self.render_to_response(self.get_context_data(form=form, properties=properties, request=request,
                                                                 application_alias=application_alias))

    def get(self, request, application_alias, entity_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        entity = get_entity_instance(request, entity_alias, application_alias)
        form = EntityForm(instance=entity)
        entity = get_entity_instance(request, entity_alias, application_alias)
        properties = Property.objects.filter(parent_entity=entity)
        data = [{'Name': property.label, 'TableName': property.name} for property in properties]
        return self.render_to_response(self.get_context_data(form=form, request=request, application_alias=application_alias, properties=data))


class PropertyCreate(CreateView):
    template_name = 'administration/create.html'
    object = None

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        entity_alias = kwargs['entity_alias']
        entity = get_entity_instance(request, entity_alias, kwargs['application_alias'])
        application = get_application_instance(kwargs['application_alias'], request)

        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', 'entity_type_custom'),
            'href': '/admin/applicaion/%s/entity/%s/edit/' % (kwargs['application_alias'], entity_alias),
            'action': localization.get_string(request, 'ru', 'property_action_create'),
            'property_entity': entity.name,
            'messages': messages.get_messages(request),
            'application': application
        }
        return context

    def get(self, request, application_alias, entity_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        application = get_application_instance(application_alias, request)
        form = PropertyForm()
        form.fields['link_entity'].queryset = Entity.objects.filter(site=application.site)
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, entity_alias=entity_alias,
                                          application_alias=application_alias))

    def post(self, request, application_alias, entity_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        if len(request.FILES) > 0:
            request.FILES['image'].name = request.POST.get('alias') + '.png'
        form = PropertyForm(request.POST, request.FILES)
        entity = get_entity_instance(request, entity_alias, application_alias)

        form.instance.parent_entity = entity
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/application/%s/entity/%s/edit/' % (application_alias, entity_alias))
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, entity_alias=entity_alias,
                                                                 application_alias=application_alias))


class PropertyEdit(UpdateView):
    template_name = 'administration/create.html'
    object = None

    def get_context_data(self, **kwargs):
        prepare_form(kwargs['form'])
        request = kwargs['request']
        entity_alias = kwargs['entity_alias']
        entity = get_entity_instance(request, entity_alias, kwargs['application_alias'])
        application = get_application_instance(kwargs['application_alias'], request)

        context = {
            'form': kwargs['form'],
            'caption': localization.get_string(request, 'ru', 'entity_type_custom'),
            'href': '/admin/application/%s/entity/%s/edit/' % (kwargs['application_alias'], entity_alias),
            'action': localization.get_string(request, 'ru', 'property_action_edit'),
            'property_entity': entity.name,
            'messages': messages.get_messages(request),
            'application': application
        }
        return context

    def get(self, request, application_alias, entity_alias, property_alias):
        if not request.user.is_superuser:
            raise PermissionDenied

        entity = get_entity_instance(request, entity_alias, application_alias)

        instance = Property.objects.filter(name=property_alias, parent_entity=entity)
        if len(instance) > 0:
            form = PropertyForm(instance=instance[0])
            return self.render_to_response(
                context=self.get_context_data(form=form, request=request, entity_alias=entity_alias,
                                              application_alias=application_alias))
        else:
            messages.error(request, u'Свойства "%s" для сущности "%s" не существует' % (property_alias, entity_alias))
            return HttpResponseRedirect('..')

    def post(self, request, application_alias, entity_alias, property_alias):
        if not request.user.is_superuser:
            raise PermissionDenied
        if len(request.FILES) > 0:
            request.FILES['image'].name = request.POST.get('alias') + '.png'

        entity = get_entity_instance(request, entity_alias, application_alias)
        instance = Property.objects.filter(name=property_alias, parent_entity=entity)
        if len(instance) > 0:
            form = PropertyForm(request.POST, request.FILES, instance=instance[0])
        else:
            messages.error(request, u'Свойства "%s" для сущности "%s" не существует' % (property_alias, entity_alias))
            return HttpResponseRedirect('..')

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/application/%s/entity/%s/edit/' % (application_alias, entity_alias))
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, entity_alias=entity_alias,
                                                                 application_alias=application_alias))


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        exclude = ('editor', 'date_change', 'parent_entity')


def prepare_form(form):
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
        elif type(form[field_name].field.widget) == Textarea:
            form[field_name].field.widget.attrs.__setitem__('class', "textarea span")
        elif type(form[field_name].field.widget) == DateTimeInput:
            form[field_name].field.widget.attrs.__setitem__('class', "datetime span")
        elif type(form[field_name].field.widget) == DateInput:
            form[field_name].field.widget.attrs.__setitem__('class', "date span")


@login_required
def home(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    return render_to_response('administration/home.html', {'request': request})


def error(request):
    return render_to_response('base_error.html', {'request': request, 'messages': messages.get_messages(request)})


def logout(request):
    """

    """
    django.contrib.auth.logout(request)
    return HttpResponseRedirect('/admin')
