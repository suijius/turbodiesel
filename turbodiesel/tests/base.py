# -*- coding: utf-8 -*-
import uuid
import base64
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase, TestCase, Client
from selenium.webdriver.firefox.webdriver import WebDriver


class LiveServerBaseTestCase(LiveServerTestCase):
    # fixtures = ['user-data.json']
    guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    guid.replace('=', '')

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(LiveServerBaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LiveServerBaseTestCase, cls).tearDownClass()

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def login(self):
        if self.is_element_present(By.ID, "id_username"):
            self.driver.find_element_by_id("id_username").clear()
            self.driver.find_element_by_id("id_username").send_keys("root")
            self.driver.find_element_by_id("id_password").clear()
            self.driver.find_element_by_id("id_password").send_keys("irdecntyu")
            self.driver.find_element_by_css_selector("input.btn.btn-large").click()

    def create_app(self):
        """
        Cоздания приложения
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/")
        self.login()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, u"Создание приложения"))
        driver.find_element_by_link_text(u"Создание приложения").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(self.guid)
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(self.guid)
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys(self.guid)
        driver.find_element_by_id("id_logotype").send_keys("C:\\Users\\Public\\Pictures\\Sample Pictures\\Chrysanthemum.jpg")
        driver.find_element_by_id("submit").click()
        self.assertTrue(self.is_element_present(By.LINK_TEXT, u"Создание приложения"))

    def open_app(self):
        """
        Открытие созданного приложения
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='content']/div[3]/div/div/div[2]"))

    def delete_app(self):
        """
        Удаление приложения
        """
        self.open_app()
        driver = self.driver
        driver.get(self.base_url + "/admin/")
        self.login()
        driver.find_element_by_css_selector("img[alt='" + self.guid + "']").click()
        driver.find_element_by_link_text(u"Удалить").click()
        driver.find_element_by_css_selector("input.btn.btn-large").click()
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.assertFalse(self.is_element_present(By.CSS_SELECTOR, "img[alt='" + self.guid + "']"))


class BaseTestCase(TestCase):
    guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    guid.replace('=', '')
    # fixtures = ['user-data.json']
    client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    @classmethod
    def setUpClass(cls):
        user_list = User.objects.filter(username='root')
        if user_list.count() == 0:
            cls.user = User.objects.create_superuser(username='root', email='jacob@mail.ru', password='irdecntyu')
        super(TestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls).tearDownClass()

    def setUp(self):
        super(TestCase, self).setUp()

    def login(self):
        response = self.client.login(username='root', password='irdecntyu')
        self.assertEqual(response, True)

    def create_app(self):
        """
        Корректное создания приложения
        """
        fp = open('C:/Users/Public/Pictures/Sample Pictures/Chrysanthemum.jpg', 'rb')
        response = self.client.post('/admin/application/create/', {
            'name': self.guid,
            'title': self.guid,
            'alias': self.guid,
            'logotype': fp,
        })
        fp.close()
        self.assertEqual(response.status_code, 302)

