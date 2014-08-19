# coding=cp1251

from metamodel.models import Application, UserProfile
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
import data
import settings
import json
from django.contrib.auth.models import User
from metamodel_view import TurboDieselUpdateView, TurboDieselCreateView
from django.http import HttpResponseRedirect, HttpResponse


class ExtUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'date_change')


class ExtUserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'password')


class ExtUserCreate(TurboDieselCreateView):
    template_name = 'administration/user.html'

    def get(self, request, application_alias):
        application = self.preget(request, application_alias)
        form = UserCreationForm()
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias):
        application = self.prepost(request, application_alias)
        form = UserCreationForm(request.POST, request.FILES)
        #        form.instance.application = application
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, request=request, application=application))


class ExtUserEdit(UpdateView):
    template_name = 'administration/user.html'

    def get(self, request, application_alias, user_id):
        application = self.preget(request, application_alias)
        #        user_instance = UserProfile.objects.filter(user_id = user_id, application = application)
        user_instance = User.objects.filter(id=user_id)
        if len(user_instance) > 0:
            form = ExtUserForm(instance=user_instance[0])
        return self.render_to_response(
            context=self.get_context_data(form=form, request=request, application=application))

    def post(self, request, application_alias, user_id):
        application = self.prepost(request, application_alias)
        user_instance = User.objects.filter(id=user_id)
        if len(user_instance) > 0:
            form = ExtUserForm(request.POST, request.FILES, instance=user_instance[0])
            #            form.instance.application = application
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('../..')
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, request=request, application=application))

