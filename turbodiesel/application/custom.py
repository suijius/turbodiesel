# coding=cp1251
"""
deprecated
"""
from django.shortcuts import render_to_response


def unitcard(request, application, custom_template):
    return render_to_response('%s/%s.html' % (application.alias, custom_template),
                              {'logotype': application.logotype, 'title': application.name})