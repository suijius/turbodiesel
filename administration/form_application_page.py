# coding=cp1251

from metamodel.models import Application, Page
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
import data
import settings
import json
from dbtemplates import models as dbTemplates
from django.forms.widgets import TextInput, Select, Textarea, DateTimeInput, CheckboxInput, DateInput
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect, HttpResponse


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
            if type(form[
                field_name].field.widget) == Textarea and field_name != 'keywords' and field_name != 'description':
                form[field_name].field.widget.attrs.__setitem__('class', "textarea span")

        return context

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = ApplicationPageForm(request.POST, request.FILES)
        form.instance.application = application
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../edit')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request))

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        templates = dbTemplates.Template.objects.filter(name__icontains=application_alias + '/')
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
        extensionList = settings.EXTENSIONS + data.get_custom_entity(kwargs['application_alias'], request)
        context['pages'] = kwargs.get('pages', [])
        context['extension'] = json.dumps(extensionList)
        context['pages'] = kwargs.get('pages', [])
        context['page'] = kwargs.get('page', [])
        form = context['form']
        for field_name in form.fields:
            if type(form[
                field_name].field.widget) == Textarea and field_name != 'keywords' and field_name != 'description':
                form[field_name].field.widget.attrs.__setitem__('class', "textarea span")
        return context

    def post(self, request, application_alias, page_alias):
        application = self.prepost(request, application_alias)
        page_instance = Page.objects.filter(alias=page_alias, site=application.site)
        if len(page_instance) > 0:
            templates = dbTemplates.Template.objects.filter(name__icontains=application_alias + '/')
            pages = Page.objects.filter(application=page_instance[0].application)
            change_template = False
            change_code = False
            if request.POST['template'] != '' and page_instance[0].template_id == int(request.POST['template']):
                change_template = True
            if request.POST['code'] != '' and page_instance[0].code_id == int(request.POST['code']):
                change_code = True
            for item in request.POST:
                while request.POST[item].__contains__('&lt') or request.POST[item].__contains__('&gt') or request.POST[
                    item].__contains__('&amp'):
                    request.POST[item] = request.POST[item].replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&nbsp;', ' ')
            form = ApplicationPageForm(request.POST, request.FILES, instance=page_instance[0])
            if request.POST.get('new'):
                form = ApplicationPageForm(request.POST, request.FILES)
                form.instance.application = application
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
                return self.render_to_response(
                    self.get_context_data(form=form, request=request, application_alias=application_alias))

    def get(self, request, application_alias, page_alias):
        application = self.preget(request, application_alias)
        page_instance = Page.objects.filter(alias=page_alias, site=application.site)
        if len(page_instance) > 0:
            templates = dbTemplates.Template.objects.filter(name__icontains=application_alias + '/')
            form = ApplicationPageForm(instance=page_instance[0])
            form.fields['template'].queryset = templates
            return self.render_to_response(
                self.get_context_data(form=form, request=request, page=page_instance[0], application=application,
                                      application_alias=application_alias))
