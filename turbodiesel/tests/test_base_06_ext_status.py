# coding=utf-8
from turbodiesel.models import Application, Entity, ExtStatus, ExtWorkflow

from turbodiesel.tests.base import BaseTestCase
from django.conf import settings
import uuid
import base64


class ApplicationExtStatusTest(BaseTestCase):
    application = None

    def setUp(self):
        self.login()
        settings.SITE_ID = 1
        self.guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        self.guid.replace('=', '')
        self.create_app()
        self.application = Application.objects.get(alias=self.guid)
        settings.SITE_ID = self.application.site_id
        super(ApplicationExtStatusTest, self).setUp()

    def test_01_get_create_status(self):
        """
        Открытие формы для создания статуса
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extstatus/' + str(wf.id) + '/create/')
        self.assertEqual(response.status_code, 200)

    def test_02_post_create_status(self):
        """
        Cоздание статуса без ошибок
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/' + str(wf.id) + '/create/', {
            'name': 'statusname'
        })
        self.assertEqual(response.status_code, 302)

    def test_03_post_create_status(self):
        """
        Cоздание статуса без имени
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/' + str(wf.id) + '/create/', {
        })
        self.assertEqual(response.status_code, 500)

    def test_04_post_create_status(self):
        """
        Cоздание статуса с несуществующим workflow
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/0/create/', {
            'name': 'statusname'
        })
        self.assertEqual(response.status_code, 500)

    def test_05_get_edit_status(self):
        """
        Открытие формы для редактирования статуса
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extstatus/' + str(st.id) + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_06_post_edit_status(self):
        """
        Редактирование статуса без ошибок
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/' + str(st.id) + '/edit/', {
            'name': 'statusname'
        })
        self.assertEqual(response.status_code, 302)

    def test_07_post_edit_status(self):
        """
        Редактирование имени статуса
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/' + str(st.id) + '/edit/', {
            'name': 'statusname1'
        })
        self.assertEqual(response.status_code, 302)

    def test_08_post_edit_status(self):
        """
        Редактирование статуса с неправильным workflow
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/0/edit/', {
            'name': 'statusname'
        })
        self.assertEqual(response.status_code, 500)

    def test_09_get_edit_status(self):
        """
        Открытие формы для редактирования статуса с несуществующим статусом
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extstatus/0/edit/')
        self.assertEqual(response.status_code, 500)

    def test_10_get_create_status(self):
        """
        Открытие формы для создания статуса с несуществующим workflow
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        response = self.client.get('/admin/application/' + self.guid + '/extension/extstatus/0/create/')
        self.assertEqual(response.status_code, 200)

    def test_11_post_edit_status(self):
        """
        Редактирование статуса без ошибок с созданием нового статуса
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/' + str(st.id) + '/edit/', {
            'name': 'statusname',
            'new': 'new'
        })
        self.assertEqual(response.status_code, 302)

    def test_12_post_edit_status(self):
        """
        Редактирование статуса без ошибок без закрытия окна
        """
        wf = ExtWorkflow.objects.create(name='workflow', site=self.application.site)
        st = ExtStatus.objects.create(name='status', workflow=wf)
        response = self.client.post('/admin/application/' + self.guid + '/extension/extstatus/' + str(st.id) + '/edit/', {
            'name': 'statusname',
            'lazy': 'lazy'
        })
        self.assertEqual(response.status_code, 204)
