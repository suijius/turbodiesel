# coding=utf-8
from turbodiesel.models import Application, Entity, ExtImage

from turbodiesel.tests.base import BaseTestCase
from django.conf import settings
import uuid
import base64


class ApplicationExtImageTest(BaseTestCase):
    application = None

    def setUp(self):
        self.login()
        settings.SITE_ID = 1
        self.guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        self.guid.replace('=', '')
        self.create_app()
        self.application = Application.objects.get(alias=self.guid)
        settings.SITE_ID = self.application.site_id
        super(ApplicationExtImageTest, self).setUp()

    def test_01_get_create_image(self):
        """
        Открытие формы для создания фильтра
        """
        Entity.objects.create(name='entity1', alias='alias', site=self.application.site)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extimage/create/')
        self.assertEqual(response.status_code, 200)

    def test_02_post_create_image(self):
        """
        Cоздание фильтра без ошибок
        """
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extimage/create/', {
            'name': 'filtername',
            'alias': 'alias',
            'image': fp
        })
        self.assertEqual(response.status_code, 302)

    def test_03_post_create_image(self):
        """
        Cоздание фильтра без имени
        """
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extimage/create/', {
            # 'name': 'filtername',
            'alias': 'alias',
            'image': fp
        })
        self.assertEqual(response.status_code, 200)

    def test_04_post_create_image(self):
        """
        Cоздание фильтра без псевдоними
        """
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extimage/create/', {
            'name': 'filtername',
            # 'alias': 'alias',
            'image': fp
        })
        self.assertEqual(response.status_code, 200)

    def test_05_post_create_image(self):
        """
        Cоздание фильтра без файла
        """
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/' + self.guid + '/extension/extimage/create/', {
            'name': 'filtername',
            'alias': 'alias',
            # 'image': fp
        })
        self.assertEqual(response.status_code, 200)
