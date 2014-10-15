# coding=cp1251

from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse

from turbodiesel.administration.form_extworkflow import ExtWorkflowForm

from turbodiesel.models import ExtWorkflow, ExtStatus
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView


class ExtStatusForm(ModelForm):
    class Meta:
        model = ExtStatus
        exclude = ('application', 'date_change')


class ExtStatusCreate(TurboDieselCreateView):
    template_name = 'administration/create.html'

    def post(self, request, application_alias, workflow_id):
        application = self.preget(request, application_alias)
        workflow_instance = ExtWorkflow.objects.filter(workflow_id=workflow_id, site=application.site)
        if len(workflow_instance) > 0:
            get = dict(request.POST)
            get['name'] = get['name'][0]
            get['workflow'] = workflow_id
            form = ExtStatusForm(get)
            #            form.instance.workflow = workflow_instance[0]
            if form.is_valid():
                form.save()
                return HttpResponse('', status=200)
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, request=request, application=application))


class ExtStatusEdit(TurboDieselUpdateView):
    template_name = 'administration/workflow.html'

    def get(self, request, application_alias, id):
        application = self.preget(request, application_alias)
        filter_instance = ExtStatus.objects.filter(workflow_id=id, site=application.site)
        form = None
        if len(filter_instance) > 0:
            form = ExtWorkflowForm(instance=filter_instance[0])
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias, id):
        application = self.prepost(request, application_alias)
        filter_instance = ExtWorkflow.objects.filter(workflow_id=id, site=application.site)
        if len(filter_instance) > 0:
            form = ExtStatusForm(request.POST, request.FILES, instance=filter_instance[0])
            if request.POST.get('new'):
                form = ExtStatusForm(request.POST, request.FILES)
                form.instance.application = application

            if form.is_valid():
                form.save()
                if request.POST.get('lazy'):
                    return HttpResponse('', status=204)
                else:
                    return HttpResponseRedirect('../..')
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, request=request, application=application))

