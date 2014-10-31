# coding=cp1251
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.contrib import messages


from turbodiesel.models import Page, ExtCode, get_application_instance
from turbodiesel.application import data

from django.conf import settings

def embeded_code1(request):
    from turbodiesel.models import get_model

    entity_model = get_model(request, 'bag', 'vintage')
    if len(request.POST):
        item = entity_model.objects.filter(id=request.POST.get('remove-item'))
        if len(item):
            item[0].delete()

    filter = "session__exact='%s' , order__status__exact=1" % request.session.session_key
    data_array = entity_model.objects.filter(**eval("dict(%s)" % filter))
    count = len(data_array)
    cost = 0
    for item in data_array:
        try:
            cost += int(item.article.price)
        except:
            pass
    return {'count': count, 'cost': cost, 'items': data_array}


def code_execute(request, page, application):
    page_embeded = {}
    error_list = []
    if page is not None:
        if page.code is not None:
            code = """
def embeded_code(request): 
    %s 
    """ % page.code.code.replace('\n', '\n    ')
            try:
                exec (code, globals())
                page_embeded = embeded_code1(request)
            except Exception, error:
                error_list.append(error)

    codes = ExtCode.objects.filter(site=application.site, is_global=True)
    app_embeded = {}

    for item in codes:
        code = """
def embeded_code(request): 
    %s 
        """ % item.code.replace('\n', '\n    ')
        try:
            exec (code, locals())
            app_embeded[item.name] = embeded_code1(request)
        except Exception, error:
            error_list.append(error)

    return page_embeded, app_embeded, error_list


def home(request, application_path):
    path_split = application_path.split('/')
    if len(path_split) == 0:
        return render_to_response('base_error.html', {'error_title': u'���� "%s" �� ��������' % application_path})
    if path_split[0] == '':
        return render_to_response('base_error.html', {'error_title': u'�� ������� ����������'})
    if path_split[0] == 'robots.txt':
        return data.robot(request)
    application = get_application_instance(path_split[0], request)
    if application.default:
        path_split.insert(0, '')
    if len(path_split) > 1:
        if path_split[1] == 'ajax':
            return data.ajax(request, path_split)
        # if path_split[1] == 'form':
        #     return data.form(request, path_split)
        page_lst = Page.objects.filter(site=application.site, alias=path_split[1])
        if len(page_lst) == 0:
            custom_template = request.GET.get('template')
            embeded = code_execute(request, None, application)
            if custom_template is None:
                return render_to_response('base_error.html', {
                    'error_title': u'��� ���������� "%s" �������� "%s" �� ����������' % (path_split[0], path_split[1])})
            else:
                return render_to_response('%s/%s.html' % (application.alias, custom_template),
                                          {'logotype': application.logotype, 'title': application.name,
                                           'page_embeded': embeded[0], 'app_embeded': embeded[1],
                                           'messages': messages.get_messages(request)})
    else:
        page_lst = Page.objects.filter(site=application.site, main=True)
        if len(page_lst) == 0:
            return render_to_response('base_error.html', {
                'error_title': u'��� ���������� "%s" �� ���������� ������� ��������' % path_split[0]})

    embeded = code_execute(request, page_lst[0], application)

    settings.SITE_ID = application.site_id


    return render_to_response(page_lst[0].template.name,
                              {'logotype': application.logotype, 'title': application.title, 'page': page_lst[0],
                               'page_embeded': embeded[0], 'app_embeded': embeded[1], 'error': embeded[2],
                               'messages': messages.get_messages(request)})


def main_url(request):
    _application = get_application_instance('norveg', request)
    _page_lst = Page.objects.filter(site=_application.site, main=True)
    if len(_page_lst) == 0:
        return render_to_response('base_error.html', {
            'error_title': u'��� ���������� "%s" �� ���������� ������� ��������' % _application.alias})

    embeded = code_execute(request, _page_lst[0], _application)

    settings.SITE_ID = _application.site_id


    return render_to_response(_page_lst[0].template.name,
                              {'logotype': _application.logotype, 'title': _application.title, 'page': _page_lst[0],
                               'page_embeded': embeded[0], 'app_embeded': embeded[1],
                               'messages': messages.get_messages(request)})