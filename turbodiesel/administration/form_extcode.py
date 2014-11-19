# coding=cp1251

from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse

from turbodiesel.models import ExtCode
from turbodiesel.administration.metamodel_view import TurboDieselUpdateView, TurboDieselCreateView


class ExtCodeForm(ModelForm):
    class Meta:
        model = ExtCode
        exclude = ('application', 'date_change', 'site')


class ExtCodeCreate(TurboDieselCreateView):
    template_name = 'administration/code.html'

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = ExtCodeForm()
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = ExtCodeForm(request.POST, request.FILES)
        form.instance.site = application.site
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))


class ExtCodeEdit(TurboDieselUpdateView):
    template_name = 'administration/code.html'

    def get(self, request, application_alias, code_id):
        try:
            application = self.preget(request, application_alias)
            code_instance = ExtCode.objects.filter(id=code_id, site=application.site)
            form = None
            if len(code_instance) > 0:
                form = ExtCodeForm(instance=code_instance[0])
            return self.render_to_response(
                context=self.get_context_data(form=form, request=request, application=application))
        except:
            return HttpResponse('', status=404)

    def post(self, request, application_alias, code_id):
        application = self.prepost(request, application_alias)
        try:
            code_instance = ExtCode.objects.filter(id=code_id, site=application.site)
            if len(code_instance) > 0:
                form = ExtCodeForm(request.POST, request.FILES, instance=code_instance[0])
                if request.POST.get('new'):
                    form = ExtCodeForm(request.POST, request.FILES)
                    form.instance.site = application.site
                if form.is_valid():
                    form.save()
                    if request.POST.get('lazy'):
                        return HttpResponse('', status=204)
                    else:
                        return HttpResponseRedirect('../..')
                else:
                    return self.render_to_response(self.get_context_data(form=form, request=request, application=application))
            else:
                return HttpResponse('', status=404)
        except:
            return HttpResponse('', status=404)
