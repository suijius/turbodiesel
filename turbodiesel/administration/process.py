# coding=cp1251

# ToDo:создание процесса из файла *.bpmn
# ToDo:отображение процесса
# ToDo:пометка текущего состояния на схеме процесса
# ToDo:запуск процесса
# ToDo:создание скриптовых тасков
# ToDo:создание пользовательских тасков с заполнением форм
# ToDo:отображение списка запущенных процессов

from django.contrib.sites.models import Site

from lxml import html, etree
from turbodiesel.models import ExtBPMProcess, ExtBPMFlow, ExtBPMActivity
from turbodiesel.tests.base import BaseTestCase


class ApplicationPageTest(BaseTestCase):
    application = None

    def test_01_get_create_page(self):
        fp = open('c:\\Users\\schepurnov\\Downloads\\diagram (1).bpmn', 'rt')


        bpmn = etree.parse(fp)
        namespaces = {'p': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
        process_list = bpmn.xpath('//p:process', namespaces=namespaces)
        if len(process_list):
            process = process_list[0]
            exists_process_list = ExtBPMProcess.objects.filter(nature_key=process.attrib['id'])
            bpm_process = None
            if len(exists_process_list):
                bpm_process = exists_process_list[0]
                # ToDo:продумать реакцию на существующие не выполненные инстансы процессов
                # ToDo:версионность шаблонов процесса
            site = Site.objects.get(id=1)
            bpm_process = ExtBPMProcess.objects.create(nature_key=process.attrib['id'], name=process.attrib['name'], site=site)
            flows = process.xpath('*[@sourceRef]')
            expression = '*[@id = $name]'
            activities = {}
            for flow in flows:
                activities[flow.attrib['sourceRef']] = process.xpath(expression, namespaces=namespaces, name=flow.attrib['sourceRef'])[0]  # ToDo:доделать проверку на наличие
                activities[flow.attrib['targetRef']] = process.xpath(expression, namespaces=namespaces, name=flow.attrib['targetRef'])[0]  # ToDo:доделать проверку на наличие

            for key in activities.keys():
                activity = activities[key]
                activities[key] = ExtBPMActivity.objects.create(nature_key=activity.attrib['id'], name=activity.attrib.get('name', ''), process=bpm_process)

            for flow in flows:
                bpm_flow = ExtBPMFlow.objects.create(
                    nature_key=process.attrib['id'],
                    name=process.attrib.get('name', ''),
                    source=activities[flow.attrib['sourceRef']],
                    target=activities[flow.attrib['targetRef']]
                    )
        fp.close()
