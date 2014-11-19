# -*- coding: utf-8 -*-
import uuid
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from turbodiesel.tests.base import LiveServerBaseTestCase


class ApplicationTests(LiveServerBaseTestCase):
    # fixtures = ['user-data.json']
    # guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    # guid.replace('=', '')
    #
    # @classmethod
    # def setUpClass(cls):
    #     cls.selenium = WebDriver()
    #     super(ApplicationTests, cls).setUpClass()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super(ApplicationTests, cls).tearDownClass()
    #
    # def setUp(self):
    #     self.driver = webdriver.Firefox()
    #     self.driver.implicitly_wait(30)
    #     self.base_url = "http://127.0.0.1:8000"
    #     self.verificationErrors = []
    #     self.accept_next_alert = True
    #
    # def login(self):
    #     if self.is_element_present(By.ID, "id_username"):
    #         self.driver.find_element_by_id("id_username").clear()
    #         self.driver.find_element_by_id("id_username").send_keys("root")
    #         self.driver.find_element_by_id("id_password").clear()
    #         self.driver.find_element_by_id("id_password").send_keys("irdecntyu")
    #         self.driver.find_element_by_css_selector("input.btn.btn-large").click()

    def test_01_create_app(self):
        """
        Тестирование создания приложения
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

    def test_02_recreate_app(self):
        """
        Тестирование создания приложения с существующим псевдонимом
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
        self.assertTrue(self.is_element_present(By.XPATH, "//form[@id='page']/div[3]/div[2]/span"))

    def test_03_open_app(self):
        """
        Тестирование открытия созданного приложения
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='content']/div[3]/div/div/div[2]"))

    def test_04_edit_app(self):
        """
        Тестирование редактирования атрибутов приложения
        """
        self.test_03_open_app()
        driver = self.driver
        # Переименовываем атрибуты
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(self.guid + "1")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(self.guid + "2")
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys(self.guid + "3")
        driver.find_element_by_id("id_logotype").send_keys("C:\\Users\\Public\\Pictures\\Sample Pictures\\Jellyfish.jpg")
        driver.find_element_by_id("submit").click()
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='content']/div[3]/div/div/div[2]"))
        # Возвращаем в исходное состояние
        driver.get(self.base_url + "/admin/application/" + self.guid + "3/edit/")
        self.assertTrue(self.is_element_present(By.ID, "id_name"))
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(self.guid)
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(self.guid)
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys(self.guid)
        driver.find_element_by_id("id_logotype").send_keys("C:\\Users\\Public\\Pictures\\Sample Pictures\\Jellyfish.jpg")
        driver.find_element_by_id("submit").click()

    def test_05_delete_app(self):
        """
        Тестирование удаления приложения
        """
        self.test_03_open_app()
        driver = self.driver
        driver.get(self.base_url + "/admin/")
        self.login()
        driver.find_element_by_css_selector("img[alt='" + self.guid + "']").click()
        driver.find_element_by_link_text(u"Удалить").click()
        driver.find_element_by_css_selector("input.btn.btn-large").click()
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.assertFalse(self.is_element_present(By.CSS_SELECTOR, "img[alt='" + self.guid + "']"))




    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True
    
    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException, e:
            return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)