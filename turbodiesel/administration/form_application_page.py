# coding=cp1251

import json

from django.forms import ModelForm
from dbtemplates import models as db_templates
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect, HttpResponse

from turbodiesel.administration import data

from turbodiesel.models import Page
import settings
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView


class ApplicationPageForm(ModelForm):
    class Meta:
        model = Page
        exclude = ('editor', 'date_change', 'application', 'parent', 'site')


class ApplicationPageCreate(TurboDieselCreateView):
    template_name = 'administration/application_page_edit.html'
    caption = 'entity_type_system'
    action = 'application_page_action_create'

    def get_context_data(self, **kwargs):
        context = super(ApplicationPageCreate, self).get_context_data(**kwargs)
        form = context['form']
        for field_name in form.fields:
            if type(form[field_name].field.widget) == Textarea and field_name != 'keywords' and field_name != 'description':
                form[field_name].field.widget.attrs.__setitem__('class', "textarea span")

        return context

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = ApplicationPageForm(request.POST, request.FILES)
        form.instance.site = application.site
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../edit')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request))

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        templates = db_templates.Template.objects.filter(sites=application.site)
        form = ApplicationPageForm()
        form.fields['template'].queryset = templates

        return self.render_to_response(self.get_context_data(form=form, request=request, application=application))


class ApplicationPageEdit(TurboDieselUpdateView):
    template_name = 'administration/application_page_edit.html'
    caption = 'entity_type_system'
    action = 'application_page_action_edit'

    def get_context_data(self, **kwargs):
        context = super(ApplicationPageEdit, self).get_context_data(**kwargs)
        request = kwargs['request']
        extension_list = settings.EXTENSIONS + data.get_custom_entity(kwargs['application_alias'], request)
        context['pages'] = kwargs.get('pages', [])
        context['extension'] = json.dumps(extension_list)
        context['pages'] = kwargs.get('pages', [])
        context['page'] = kwargs.get('page', [])
        form = context['form']
        for field_name in form.fields:
            if type(form[field_name].field.widget) == Textarea and field_name != 'keywords' and field_name != 'description':
                form[field_name].field.widget.attrs.__setitem__('class', "textarea span")
        return context

    def post(self, request, application_alias, page_alias):
        application = self.prepost(request, application_alias)
        page_instance = Page.objects.filter(alias=page_alias, site=application.site)
        if len(page_instance) > 0:
            # templates = db_templates.Template.objects.filter(sites=application.site)
            # pages = Page.objects.filter(application=page_instance[0].application)
            change_template = False
            change_code = False
            if request.POST.get('template') != '' and request.POST.get('template') is not None and page_instance[0].template_id == int(request.POST['template']):
                change_template = True
            if request.POST.get('code') != '' and request.POST.get('code') is not None and page_instance[0].code_id == int(request.POST['code']):
                change_code = True
            for item in request.POST:
                while request.POST[item].__contains__('&lt') or request.POST[item].__contains__('&gt') or request.POST[item].__contains__('&amp'):
                    request.POST[item] = request.POST[item].replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&nbsp;', ' ')
            form = ApplicationPageForm(request.POST, request.FILES, instance=page_instance[0])
            if request.POST.get('new'):
                form = ApplicationPageForm(request.POST, request.FILES)
                form.instance.site = application.site
            if form.is_valid():
                form.save()
                if change_template and page_instance[0].template is not None:
                    template = page_instance[0].template
                    template.content = request.POST['template-content'].strip()
                    template.save()
                if change_code and page_instance[0].code is not None:
                    code = page_instance[0].code
                    code.code = request.POST['code-content'].strip()
                    code.save()

                if request.POST.get('lazy'):
                    return HttpResponse('', status=204)
                else:
                    return HttpResponseRedirect('../../../edit')
            else:
                return self.render_to_response(self.get_context_data(form=form, request=request, application_alias=application_alias))
        else:
            return HttpResponse('', status=500)

    def get(self, request, application_alias, page_alias):
        application = self.preget(request, application_alias)
        page_instance = Page.objects.filter(alias=page_alias, site=application.site)
        if len(page_instance) > 0:
            templates = db_templates.Template.objects.filter(sites=application.site)
            form = ApplicationPageForm(instance=page_instance[0])
            form.fields['template'].queryset = templates
            return self.render_to_response(
                self.get_context_data(form=form, request=request, page=page_instance[0], application=application, application_alias=application_alias))
        else:
            return HttpResponse('', status=404)
