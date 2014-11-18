# coding=utf-8
import uuid
import base64

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from turbodiesel.tests.base import BaseTestCase


class SimpleTest(BaseTestCase):
    guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    guid.replace('=', '')

    def test_01_create_app(self):
        """
        Создание приложения без имени
        """
        self.login()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/create/', {
            'name': '',
            'title': self.guid,
            'alias': self.guid,
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_02_create_app(self):
        """
        Создание приложения без заголовка
        """
        self.login()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/create/', {
            'name': self.guid,
            'title': '',
            'alias': self.guid,
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_03_create_app(self):
        """
        Создание приложения без псевдонима
        """
        self.login()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/create/', {
            'name': self.guid,
            'title': self.guid,
            'alias': '',
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_04_create_app(self):
        """
        Создание приложения без логотипа
        """
        self.login()
        response = self.client.post('/admin/application/create/', {
            'name': self.guid,
            'title': self.guid,
            'alias': self.guid,
            'logotype': None,
        })
        self.assertEqual(response.status_code, 200)

    def test_05_create_app(self):
        """
        Корректное создание приложения
        """
        self.login()
        self.create_app()

    def test_06_create_app(self):
        """
        Открытие формы для создания приложения
        """
        self.login()
        response = self.client.get('/admin/application/create/')
        self.assertEqual(response.status_code, 200)

    def test_07_open_app(self):
        """
        Открытие созданного приложения
        """
        self.login()
        self.create_app()
        response = self.client.get('/admin/application/'+self.guid+'/edit/')
        self.assertEqual(response.status_code, 200)

    def test_08_edit_app(self):
        """
        Изменение приложения без имени
        """
        self.login()
        self.create_app()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/'+self.guid+'/edit/', {
            'name': '',
            'title': self.guid,
            'alias': self.guid,
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_09_edit_app(self):
        """
        Изменение приложения без заголовка
        """
        self.login()
        self.create_app()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/'+self.guid+'/edit/', {
            'name': self.guid,
            'title': '',
            'alias': self.guid,
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_10_edit_app(self):
        """
        Изменение приложения без псевдонима
        """
        self.login()
        self.create_app()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/'+self.guid+'/edit/', {
            'name': self.guid,
            'title': self.guid,
            'alias': '',
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_11_edit_app(self):
        """
        Изменение приложения без логотипа
        """
        self.login()
        self.create_app()
        response = self.client.post('/admin/application/'+self.guid+'/edit/', {
            'name': self.guid,
            'title': self.guid,
            'alias': self.guid,
            'logotype': None,
        })
        self.assertEqual(response.status_code, 200)

    def test_12_edit_app(self):
        """
        Изменение приложения с существующим псевдонимом
        """
        self.login()
        self.create_app()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/'+self.guid+'/edit/', {
            'name': self.guid,
            'title': self.guid,
            'alias': self.guid,
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 200)

    def test_13_edit_app(self):
        """
        Изменение приложения без ошибок
        """
        self.login()
        self.create_app()
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/'+self.guid+'/edit/', {
            'name': self.guid,
            'title': self.guid,
            'alias': self.guid + '_1',
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 302)

    def test_14_delete_get_app(self):
        """
        Удаление приложения
        """
        self.login()
        self.create_app()
        response = self.client.get('/admin/application/'+self.guid+'/delete/')
        self.assertEqual(response.status_code, 200)

    def test_15_delete_post_app(self):
        """
        Удаление приложения
        """
        self.login()
        self.create_app()
        response = self.client.post('/admin/application/'+self.guid+'/delete/')
        self.assertEqual(response.status_code, 302)
