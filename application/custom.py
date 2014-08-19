# coding=cp1251
'''
deprecated
'''
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from metamodel.models import Application, Page
from django.contrib import messages
from application import data


def unitcard(request, application, custom_template):
    return render_to_response('%s/%s.html' % (application.alias, custom_template),
                              {'logotype': application.logotype, 'title': application.name})