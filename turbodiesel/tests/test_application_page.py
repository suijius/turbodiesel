# -*- coding: utf-8 -*-
import uuid
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ApplicationPageTests(LiveServerTestCase):
    # fixtures = ['user-data.json']
    guid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    guid.replace('=', '')

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ApplicationPageTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ApplicationPageTests, cls).tearDownClass()

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

    def test_01_open_app(self):
        """
        Тестирование создания и открытия приложения
        """
        self.create_app()
        self.open_app()
        driver = self.driver
        driver.get(self.base_url + "/admin/")
        self.login()

    def test_02_create_page_01(self):
        """
        Тестирование вывода ошибки при незаполнении обязательного поля
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        driver.find_element_by_css_selector("div.grid.span8 > div.grid-title > a.pull-right.btn").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("title")
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys("short-name")
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_css_selector("a.chzn-single.chzn-single-with-drop > div > b").click()
        driver.find_element_by_id("id_description").click()
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("meta data")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("meta key")
        driver.find_element_by_id("submit").click()
        self.assertTrue(self.is_element_present(By.XPATH, "//form[@id='page']/div[1]/div[2]"))  # Наличие ошибки об обязательном заполненном поле

    def test_02_create_page_02(self):
        """
        Тестирование вывода ошибки при незаполнении обязательного поля
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        driver.find_element_by_css_selector("div.grid.span8 > div.grid-title > a.pull-right.btn").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("01-short-name")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys("short-name")
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_css_selector("a.chzn-single.chzn-single-with-drop > div > b").click()
        driver.find_element_by_id("id_description").click()
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("meta data")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("meta key")
        driver.find_element_by_id("submit").click()
        self.assertTrue(self.is_element_present(By.XPATH, "//form[@id='page']/div[2]/div[2]"))  # Наличие ошибки об обязательном заполненном поле

    def test_02_create_page_03(self):
        """
        Тестирование вывода ошибки при незаполнении обязательного поля
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        driver.find_element_by_css_selector("div.grid.span8 > div.grid-title > a.pull-right.btn").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("01-short-name")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("title")
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_css_selector("a.chzn-single.chzn-single-with-drop > div > b").click()
        driver.find_element_by_id("id_description").click()
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("meta data")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("meta key")
        driver.find_element_by_id("submit").click()
        self.assertTrue(self.is_element_present(By.XPATH, "//form[@id='page']/div[3]/div[2]"))  # Наличие ошибки об обязательном заполненном поле

    def test_02_create_page_04(self):
        """
        Тестирование вывода ошибки при незаполнении обязательного поля
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        driver.find_element_by_css_selector("div.grid.span8 > div.grid-title > a.pull-right.btn").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("01-short-name")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("title")
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys("short-name")
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_css_selector("a.chzn-single.chzn-single-with-drop > div > b").click()
        driver.find_element_by_id("id_description").click()
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("meta data")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("meta key")
        driver.find_element_by_id("submit").click()
        self.assertTrue(self.is_element_present(By.XPATH, "//form[@id='page']/div[4]/div[2]"))  # Наличие ошибки об обязательном заполненном поле

    def test_02_create_page_05(self):
        """
        Тестирование вывода ошибки при незаполнении обязательного поля при не найденном шаблоне страницы
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        driver.find_element_by_css_selector("div.grid.span8 > div.grid-title > a.pull-right.btn").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("01-short-name")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("title")
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys("short-name")
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_css_selector("div#id_template_chzn > div.chzn-drop > div.chzn-search > input").send_keys("base.html")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("meta data")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("meta key")
        driver.find_element_by_id("submit").click()
        self.assertFalse(self.is_element_present(By.XPATH, "//form[@id='page']/div[4]/div[2]"))  # Наличие ошибки об обязательном заполненном поле при не найденном шаблоне

    def test_02_create_page_06(self):
        """
        Тестирование вывода ошибки при незаполнении обязательного поля при не найденном шаблоне страницы
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/application/" + self.guid + "/edit/")
        self.login()
        driver.find_element_by_css_selector("div.grid.span8 > div.grid-title > a.pull-right.btn").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("01-short-name")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("title")
        driver.find_element_by_id("id_alias").clear()
        driver.find_element_by_id("id_alias").send_keys("short-name")
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_css_selector("div#id_template_chzn > div.chzn-drop > div.chzn-search > input").send_keys("base")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("meta data")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("meta key")
        driver.find_element_by_id("submit").click()
        self.assertFalse(self.is_element_present(By.XPATH, "//form[@id='page']/div[4]/div[2]"))  # Наличие ошибки об обязательном заполненном поле при не найденном шаблоне



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