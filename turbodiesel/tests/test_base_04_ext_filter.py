# coding=utf-8
from turbodiesel.models import Application, Entity, ExtFilter

from turbodiesel.tests.base import BaseTestCase
from django.conf import settings
import uuid
import base64


class ApplicationExtFilterTest(BaseTestCase):
    application = None

    def setUp(self):
        self.login()
        settings.SITE_ID = 1
        self.guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        self.guid.replace('=', '')
        self.create_app()
        self.application = Application.objects.get(alias=self.guid)
        settings.SITE_ID = self.application.site_id
        super(ApplicationExtFilterTest, self).setUp()

    def test_01_get_create_filter(self):
        """
        Открытие формы для создания фильтра
        """
        Entity.objects.create(name='entity1', alias='alias', site=self.application.site)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extfilter/create/')
        self.assertEqual(response.status_code, 200)

    def test_02_post_create_filter(self):
        """
        Cоздание фильтра без ошибок
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_03_post_create_filter(self):
        """
        Cоздание фильтра без имени
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            # 'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 200)

    def test_04_post_create_filter(self):
        """
        Cоздание фильтра без псевдонима
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            'name': 'filtername',
            # 'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 200)

    def test_05_post_create_filter(self):
        """
        Cоздание фильтра без сущности
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            'name': 'filtername',
            'alias': 'alias',
            # 'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 200)

    def test_06_post_create_filter(self):
        """
        Cоздание фильтра без выражения
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            # 'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_07_post_create_filter(self):
        """
        Cоздание фильтра без дополнительных условий
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            # 'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_08_post_create_filter(self):
        """
        Cоздание фильтра без группировки
        """
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/create/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_09_get_edit_filter(self):
        """
        Открытие формы для редактирования фильтра
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_10_post_edit_filter(self):
        """
        Редактирование фильтра без ошибок
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_11_post_edit_filter(self):
        """
        Редактирование фильтра без имени
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            # 'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 200)

    def test_12_post_edit_filter(self):
        """
        Редактирование фильтра без псевдонима
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            'name': 'filtername',
            # 'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 200)

    def test_13_post_edit_filter(self):
        """
        Редактирование фильтра без сущности
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            'name': 'filtername',
            'alias': 'alias',
            # 'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 200)

    def test_14_post_edit_filter(self):
        """
        Редактирование фильтра без выражения
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            # 'expression': 'expression',
            'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_15_post_edit_filter(self):
        """
        Редактирование фильтра без дополнительных условий
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            # 'extra': 'extra',
            'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)

    def test_16_post_edit_filter(self):
        """
        Редактирование фильтра без группировки
        """
        self.test_02_post_create_filter()

        filter = ExtFilter.objects.get(site=self.application.site)
        entity = Entity.objects.get(name='entity1')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extfilter/' + str(filter.id) + '/edit/', {
            'name': 'filtername',
            'alias': 'alias',
            'entity': entity.entity_id,
            'expression': 'expression',
            'extra': 'extra',
            # 'groupby': 'groupby'
        })
        self.assertEqual(response.status_code, 302)
