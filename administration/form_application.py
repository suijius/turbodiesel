#coding=cp1251

from metamodel.models import Application
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
import data
import settings
import json
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect, HttpResponse


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('editor', 'date_change')
        
class ApplicationEdit(TurboDieselUpdateView):
    template_name = 'administration/application_edit.html'
    caption = 'entity_type_system'
    action = 'application_action_edit'


    def get_context_data(self, **kwargs):
        context = super(ApplicationEdit, self).get_context_data(**kwargs)
        request = kwargs['request']
        extensionList = settings.EXTENSIONS + data.get_custom_entity(kwargs['application_alias'], request)
        context['pages'] = kwargs.get('pages', [])
        context['extension'] = json.dumps(extensionList)
        return context
        
    def post(self, request, application_alias): 
        application = self.prepost(request, application_alias)
        form = ApplicationForm(request.POST, request.FILES, instance = application) 
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('.') 
        else:
            return self.render_to_response(self.get_context_data(form = form, request = request, application_alias = application_alias))
        
    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ApplicationForm(instance = application)
        return self.render_to_response(self.get_context_data(form = form, request = request, application_alias = application_alias))
        
class ApplicationCreate(TurboDieselCreateView):
    template_name = 'administration/create.html'
    caption = 'entity_type_system'
    action = 'application_action_create'

    
    def post(self, request): 
        self.prepost(request)

        form = ApplicationForm(request.POST, request.FILES) 
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('..') 
        else:
            return self.render_to_response(self.get_context_data(form = form, request = request))
        
    def get(self, request):
        self.preget(request)
        form = ApplicationForm()
        return self.render_to_response(self.get_context_data(form = form, request = request))        
