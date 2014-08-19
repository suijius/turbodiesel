# coding=cp1251
from metamodel.models import Application, get_application_instance, Page
from django.forms import ModelForm
import data
import settings
import json
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('editor', 'date_change')


class ApplicationEdit(TurboDieselUpdateView):
    template_name = 'administration/application_edit.html'
    caption = 'entity_type_system'
    action = 'application_action_edit'

    def get_context_data(self, **kwargs):
        application_alias = kwargs['application_alias']
        context = super(ApplicationEdit, self).get_context_data(**kwargs)
        request = kwargs['request']
        extension_list = settings.EXTENSIONS + data.get_custom_entity(application_alias, request)

        application, default = get_application_instance(application_alias, request)
        pages = Page.objects.filter(application = application)
#        data = []
#        for field in pages:
#            value = {}
#            for meta in field._meta.fields:
#                value[meta.name] = truncate(field.__dict__[str(meta.name if meta.attname is None else meta.attname)], meta.name)
#            data.append(value)

        context['pages'] = pages
        context['extension'] = extension_list
        return context

    def post(self, request, **kwargs):
        application_alias = kwargs['application_alias']
        application = self.prepost(request, application_alias)
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, request=request, application_alias=application_alias))

    def get(self, request, application_alias):
        # application_alias = kwargs['application_alias']
        application = self.preget(request, application_alias)
        form = ApplicationForm(instance=application)
        return self.render_to_response(
            self.get_context_data(form=form, request=request, application_alias=application_alias))


class ApplicationCreate(TurboDieselCreateView):
    template_name = 'administration/create.html'
    caption = 'entity_type_system'
    action = 'application_action_create'

    def post(self, request, **kwargs):
        self.prepost(request)

        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request))

    def get(self, request, **kwargs):
        self.preget(request)
        form = ApplicationForm()
        return self.render_to_response(self.get_context_data(form=form, request=request))
