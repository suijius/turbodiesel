#coding=cp1251
from metamodel.models import Localization, Language, Entity, Property
from django.contrib import messages

def get_string(request, language, key):
    lang_list = Language.objects.filter(lang = 'ru')
    if len(lang_list) == 0:
        messages.error(request, u"����� %s �� ����������. ���������� ��� �������� � ������� Language" % language)
        return key
    elif len(lang_list) > 1:
        messages.error(request, u"���������� ��������� ������� ��� ����� %s. ���������� �������� � ������� ������� Language" % language)
        return key
    string_list = Localization.objects.filter(lang = lang_list[0], key = key)
    if len(string_list) == 0:
        messages.error(request, u"������ ��� ����� %s �� ����������. ���������� � �������� � ������� Localization" % key)
        return key
    elif len(string_list) > 1:
        messages.error(request, u"���������� ��������� ������� ��� ����� %s. ���������� �������� � ������� ������� Localization" % key)
        return key
    return string_list[0]
