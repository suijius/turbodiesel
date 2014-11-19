# coding=utf-8
from turbodiesel.models import Application, Page, ExtCode

from turbodiesel.tests.base import BaseTestCase
from django.conf import settings
import uuid
import base64


class ApplicationPageTest(BaseTestCase):
    application = None

    def setUp(self):
        self.login()
        settings.SITE_ID = 1
        self.guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        self.guid.replace('=', '')
        self.create_app()
        self.application = Application.objects.get(alias=self.guid)
        settings.SITE_ID = self.application.site_id
        super(ApplicationPageTest, self).setUp()

    def test_01_get_create_code(self):
        """
        Открытие формы для создания кодовой вставки
        """
        response = self.client.get('/admin/application/' + self.guid + '/extension/extcode/create/')
        self.assertEqual(response.status_code, 200)

    def test_02_post_create_code(self):
        """
        Создание кодовой вставки без ошибок
        """
        response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/create/', {
            'name': 'codename',
            'code': '# coding=utf-8',
            'is_global': True
        })
        self.assertEqual(response.status_code, 302)

    def test_03_post_create_code(self):
        """
        Создание кодовой вставки без имени
        """
        response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/create/', {
            # 'name': 'codename',
            'code': '# coding=utf-8',
            'is_global': True
        })
        self.assertEqual(response.status_code, 200)

    def test_04_post_create_code(self):
        """
        Создание кодовой вставки без кода
        """
        response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/create/', {
            'name': 'codename',
            # 'code': '',
            'is_global': True
        })
        self.assertEqual(response.status_code, 200)

    def test_05_post_create_code(self):
        """
        Создание кодовой вставки без указания зоны видимости
        """
        response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/create/', {
            'name': 'codename',
            'code': '# coding=utf-8'
            # 'is_global': True
        })
        self.assertEqual(response.status_code, 302)

    def test_06_get_edit_code(self):
        """
        Открытие формы для редактирования кодовой вставки
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.get('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/')
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_07_post_edit_code(self):
        """
        Редактирование кодовой вставки без ошибок
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                'name': 'codename',
                'code': '# coding=utf-8',
                'is_global': True
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_08_post_edit_code(self):
        """
        Редактирование кодовой вставки без имени
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                # 'name': 'codename',
                'code': '# coding=utf-8',
                'is_global': True
            })
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_09_post_edit_code(self):
        """
        Редактирование кодовой вставки без кода
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                'name': 'codename',
                # 'code': '# coding=utf-8',
                'is_global': True
            })
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_10_post_edit_code(self):
        """
        Редактирование кодовой вставки без указателя видимости
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                'name': 'codename',
                'code': '# coding=utf-8'
                # 'is_global': True
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_11_post_edit_code(self):
        """
        Редактирование кодовой вставки как копии c таким же именем
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                'name': 'codename',
                'code': '# coding=utf-8',
                'is_global': True,
                'new': 'new'
            })
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_12_post_edit_code(self):
        """
        Редактирование кодовой вставки как копии c другим именем
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                'name': 'codename1',
                'code': '# coding=utf-8',
                'is_global': True,
                'new': 'new'
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_13_post_edit_code(self):
        """
        Редактирование кодовой вставки без закрытия окна
        """
        self.test_02_post_create_code()

        code_list = ExtCode.objects.filter(site=self.application.site)
        if code_list.count():
            response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/' + str(code_list[0].id) + '/edit/', {
                'name': 'codename',
                'code': '# coding=utf-8',
                'is_global': True,
                'lazy': 'lazy'
            })
            self.assertEqual(response.status_code, 204)
        else:
            self.assertTrue(False, 'Не создана кодовая вставка')

    def test_14_post_edit_code(self):
        """
        Редактирование кодовой вставки с некорректным ID
        """

        response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/0/edit/', {
            'name': 'codename',
            'code': '# coding=utf-8',
            'is_global': True
        })
        self.assertEqual(response.status_code, 404)

    def test_15_post_edit_code(self):
        """
        Редактирование кодовой вставки с буквенным ID
        """

        response = self.client.post('/admin/application/' + self.guid + '/extension/extcode/I0D/edit/', {
            'name': 'codename',
            'code': '# coding=utf-8',
            'is_global': True
        })
        self.assertEqual(response.status_code, 404)

    def test_16_get_edit_code(self):
        """
        Открытие формы для редактирования кодовой вставки c буквенным ID
        """
        response = self.client.get('/admin/application/' + self.guid + '/extension/extcode/I0D/edit/')
        self.assertEqual(response.status_code, 404)
