# coding=cp1251
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DeleteView

from turbodiesel.administration import data
from turbodiesel.models import Application, get_application_instance, Page
import settings
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('editor', 'date_change', 'site')


class ApplicationEdit(TurboDieselUpdateView):
    template_name = 'administration/application_edit.html'
    caption = 'entity_type_system'
    action = 'application_action_edit'

    def get_context_data(self, **kwargs):
        application_alias = kwargs['application_alias']
        context = super(ApplicationEdit, self).get_context_data(**kwargs)
        request = kwargs['request']
        extension_list = settings.EXTENSIONS + data.get_custom_entity(application_alias, request)

        application = get_application_instance(application_alias, request)
        pages = Page.objects.filter(site=application.site)
        # data = []
        #        for field in pages:
        #            value = {}
        #            for meta in field._meta.fields:
        #                value[meta.name] = truncate(field.__dict__[str(meta.name if meta.attname is None else meta.attname)], meta.name)
        #            data.append(value)

        context['pages'] = pages
        context['extension'] = extension_list
        return context

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, request=request, application_alias=application_alias))

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ApplicationForm(instance=application)
        return self.render_to_response(self.get_context_data(form=form, request=request, application_alias=application_alias))


class ApplicationCreate(TurboDieselCreateView):
    template_name = 'administration/create.html'
    caption = 'entity_type_system'
    action = 'application_action_create'

    def post(self, request, **kwargs):
        self.prepost(request)
        form = ApplicationForm(request.POST, request.FILES)
        site = Site.objects.create(name=form.instance.title, domain=form.instance.alias)
        form.instance.site = site
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request))

    def get(self, request, **kwargs):
        self.preget(request)
        form = ApplicationForm()
        return self.render_to_response(self.get_context_data(form=form, request=request))


class ApplicationDelete(DeleteView):
    template_name = 'administration/application_confirm_delete.html'
    model = Application
    success_url = '/admin'

    def get_object(self):
        application = get_application_instance(self.args[0], self.request)
        return application

    def post(self, request, application_alias):
        application = self.get_object()
        site = application.site
        ret = super(ApplicationDelete, self).post(request, application_alias)
        Site.delete(site)
        return ret

    def get(self, request, application_alias):
        return self.render_to_response({'object': self.get_object()})

    # def dispatch(self, request, application_alias, **kwargs):
    #     application = get_application_instance(application_alias, request)
    #     super(ApplicationDelete, self).dispatch(request, application_alias, pk=application.pk)