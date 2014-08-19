# coding=cp1251

from metamodel.models import Application, ExtImage
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
import data
import settings
import json
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect, HttpResponse


class ExtImageForm(ModelForm):
    class Meta:
        model = ExtImage
        exclude = ('application', 'date_change')


class ExtImageCreate(TurboDieselCreateView):
    template_name = 'administration/create.html'

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ExtImageForm()
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        if len(request.FILES) > 0:
            request.FILES['image'].name = request.POST.get('alias') + '.' + request.FILES['image'].name.split('.')[-1]
        form = ExtImageForm(request.POST, request.FILES)
        form.instance.application = application
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))

