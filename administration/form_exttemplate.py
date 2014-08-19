# coding=cp1251

from metamodel.models import Application
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
import data
import settings
import json
from dbtemplates import models as dbTemplates
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect, HttpResponse


class ExtTemplateForm(ModelForm):
    class Meta:
        model = dbTemplates.Template
        exclude = ('application', 'date_change')


class ExtTemplateCreate(TurboDieselCreateView):
    template_name = 'administration/template.html'

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ExtTemplateForm()
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = ExtTemplateForm(request.POST, request.FILES)
        form.instance.application = application
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))


class ExtTemplateEdit(TurboDieselUpdateView):
    template_name = 'administration/template.html'

    def get(self, request, application_alias, id):
        application = self.preget(request, application_alias)
        filter_instance = dbTemplates.Template.objects.filter(id=id, name__contains=application_alias)
        if len(filter_instance) > 0:
            form = ExtTemplateForm(instance=filter_instance[0])
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias, id):
        application = self.prepost(request, application_alias)
        filter_instance = dbTemplates.Template.objects.filter(id=id, name__contains=application_alias)
        if len(filter_instance) > 0:
            form = ExtTemplateForm(request.POST, request.FILES, instance=filter_instance[0])
            if request.POST.get('new'):
                form = ExtTemplateForm(request.POST, request.FILES)
                form.instance.application = application

            form.instance.creation_date = filter_instance[0].creation_date
            form.instance.last_changed = filter_instance[0].last_changed
            if form.is_valid():
                form.save()
                if request.POST.get('lazy'):
                    return HttpResponse('', status=204)
                else:
                    return HttpResponseRedirect('../..')
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, request=request, application=application))
            
