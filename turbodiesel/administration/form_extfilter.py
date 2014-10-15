# coding=cp1251

from django.forms import ModelForm
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect

from turbodiesel.models import ExtFilter, Entity
from turbodiesel.administration.metamodel_view import TurboDieselUpdateView, TurboDieselCreateView


class ExtFilterForm(ModelForm):
    class Meta:
        model = ExtFilter
        exclude = ('application', 'date_change')


class ExtFilterCreate(TurboDieselCreateView):
    template_name = 'administration/filter.html'

    def get_context_data(self, **kwargs):
        context = super(ExtFilterCreate, self).get_context_data(**kwargs)
        form = context['form']
        for field_name in form.fields:
            if type(form[field_name].field.widget) == Textarea:
                form[field_name].field.widget.attrs.__setitem__('class', "span")
        return context

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ExtFilterForm()
        entities = Entity.objects.filter(site=application.site)
        form.fields['entity'].queryset = entities

        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = ExtFilterForm(request.POST, request.FILES)
        form.instance.application = application
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))


class ExtFilterEdit(TurboDieselUpdateView):
    template_name = 'administration/filter.html'

    def get_context_data(self, **kwargs):
        context = super(ExtFilterEdit, self).get_context_data(**kwargs)
        form = context['form']
        for field_name in form.fields:
            if type(form[field_name].field.widget) == Textarea:
                form[field_name].field.widget.attrs.__setitem__('class', "span")
        return context

    def get(self, request, application_alias, filter_id):
        application = self.preget(request, application_alias)
        filter_instance = ExtFilter.objects.filter(filter_id=filter_id, site=application.site)
        form = None
        if len(filter_instance) > 0:
            form = ExtFilterForm(instance=filter_instance[0])
            entities = Entity.objects.filter(site=application.site)
            form.fields['entity'].queryset = entities
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias, filter_id):
        application = self.prepost(request, application_alias)
        filter_instance = ExtFilter.objects.filter(filter_id=filter_id, site=application.site)
        if len(filter_instance) > 0:
            form = ExtFilterForm(request.POST, request.FILES, instance=filter_instance[0])
            form.instance.application = application
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('../..')
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, request=request, application=application))