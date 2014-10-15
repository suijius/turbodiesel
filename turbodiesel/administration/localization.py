# coding=cp1251
from django.contrib import messages

from turbodiesel.models import Localization, Language


def get_string(request, language, key):
    lang_list = Language.objects.filter(lang='ru')
    if len(lang_list) == 0:
        messages.error(request, u"Языка %s не существует. Необходимо его добавить в таблицу Language" % language)
        return key
    elif len(lang_list) > 1:
        messages.error(request,
                       u"Существует несколько записей для языка %s. Необходимо привести в порядок таблицу Language" % language)
        return key
    string_list = Localization.objects.filter(lang=lang_list[0], key=key)
    if len(string_list) == 0:
        messages.error(request,
                       u"Строки для ключа %s не существует. Необходимо её добавить в таблицу Localization" % key)
        return key
    elif len(string_list) > 1:
        messages.error(request,
                       u"Существует несколько записей для ключа %s. Необходимо привести в порядок таблицу Localization" % key)
        return key
    return string_list[0]
