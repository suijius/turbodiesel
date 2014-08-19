#coding=cp1251

from metamodel.models import Application, ExtWorkflow
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
import data
import settings
import json
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect, HttpResponse

class ExtWorkflowForm(ModelForm):
    class Meta:
        model = ExtWorkflow
        exclude = ('application', 'date_change')
        
class ExtWorkflowCreate(TurboDieselCreateView):
    template_name = 'administration/create.html'
    
    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ExtWorkflowForm()
        return self.render_to_response(context = self.get_context_data(form = form, request = request, application = application))

    def post(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ExtWorkflowForm(request.POST, request.FILES)
        form.instance.application = application
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('..') 
        else:
            return self.render_to_response(self.get_context_data(form = form, request = request, application = application))

class ExtWorkflowEdit(TurboDieselUpdateView):
    template_name = 'administration/workflow.html'
   
    def get(self, request, application_alias, id):
        application = self.preget(request, application_alias)
        filter_instance = ExtWorkflow.objects.filter(workflow_id = id, application = application)
        if len(filter_instance) > 0:
            form = ExtWorkflowForm(instance = filter_instance[0])
        return self.render_to_response(context = self.get_context_data(form = form, request = request, application = application))

    def post(self, request, application_alias, id):
        application = self.prepost(request, application_alias)
        filter_instance = ExtWorkflow.objects.filter(workflow_id = id, application = application)
        if len(filter_instance) > 0:
            form = ExtWorkflowForm(request.POST, request.FILES, instance = filter_instance[0])
            if request.POST.get('new'):
                form = ExtWorkflowForm(request.POST, request.FILES)
                form.instance.application = application
            
            if form.is_valid(): 
                form.save()
                if request.POST.get('lazy'):
                    return HttpResponse('', status=204) 
                else:
                    return HttpResponseRedirect('../..') 
            else:
                return self.render_to_response(self.get_context_data(form = form, request = request, application = application))

