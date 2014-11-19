# coding=utf-8
from turbodiesel.models import Application, Page, ExtCode

from turbodiesel.tests.base import BaseTestCase
from dbtemplates import models as db_templates
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

    def test_01_get_create_page(self):
        """
        Открытие формы для создания страницы
        """
        response = self.client.get('/admin/application/' + self.guid + '/page/create/')
        self.assertEqual(response.status_code, 200)

    def test_02_post_create_page(self):
        """
        Создание страницы без шаблона
        """
        response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
            'name': u'Краткое наименование',
            'title': u'Заголовок страницы',
            'alias': 'alias',
            'main': False,
            'description': u'Мета-описание',
            'keywords': u'Мета-ключевые слова',
            'content': u'Основной контент'
        })
        self.assertEqual(response.status_code, 200)

    def test_03_post_create_page(self):
        """
        Создание страницы без ошибок
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'name': u'Краткое наименование',
                'title': u'Заголовок страницы',
                'alias': 'alias',
                'template': dbt[0].id,
                'main': False,
                'description': u'Мета-описание',
                'keywords': u'Мета-ключевые слова',
                'content': u'Основной контент'
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_04_post_create_page(self):
        """
        Создание страницы без имени
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'title': u'Заголовок страницы',
                'alias': 'alias',
                'template': dbt[0].id,
                'main': False,
                'description': u'Мета-описание',
                'keywords': u'Мета-ключевые слова',
                'content': u'Основной контент'
            })
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_05_post_create_page(self):
        """
        Создание страницы без заголовка
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'name': u'Краткое наименование',
                'alias': 'alias',
                'template': dbt[0].id,
                'main': False,
                'description': u'Мета-описание',
                'keywords': u'Мета-ключевые слова',
                'content': u'Основной контент'
            })
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_06_post_create_page(self):
        """
        Создание страницы без псевдонима
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'name': u'Краткое наименование',
                'title': u'Заголовок страницы',
                'template': dbt[0].id,
                'main': False,
                'description': u'Мета-описание',
                'keywords': u'Мета-ключевые слова',
                'content': u'Основной контент'
            })
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_07_post_create_page(self):
        """
        Создание страницы без описания
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'name': u'Краткое наименование',
                'title': u'Заголовок страницы',
                'alias': 'alias',
                'template': dbt[0].id,
                'main': False,
                'keywords': u'Мета-ключевые слова',
                'content': u'Основной контент'
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_08_post_create_page(self):
        """
        Создание страницы без ключевых слов
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'name': u'Краткое наименование',
                'title': u'Заголовок страницы',
                'alias': 'alias',
                'template': dbt[0].id,
                'main': False,
                'description': u'Мета-описание',
                'content': u'Основной контент'
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_09_post_create_page(self):
        """
        Создание страницы без контента
        """
        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
                'name': u'Краткое наименование',
                'title': u'Заголовок страницы',
                'alias': 'alias',
                'template': dbt[0].id,
                'main': False,
                'description': u'Мета-описание',
                'keywords': u'Мета-ключевые слова',
            })
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_10_get_edit_page(self):
        """
        Вызов формы для редактирования фейковой страницы
        """
        # dbt = db_templates.Template.objects.filter(sites=self.application.site)
        # if dbt.count():
        #     response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
        #         'name': u'Краткое наименование',
        #         'title': u'Заголовок страницы',
        #         'alias': 'alias',
        #         'template': dbt[0].id,
        #         'main': False,
        #         'description': u'Мета-описание',
        #         'keywords': u'Мета-ключевые слова',
        #         'content': u'Основной контент'
        #     })
        #     self.assertEqual(response.status_code, 302)
        # else:
        #     self.assertTrue(False, 'Не существует базового шаблона для приложения')

        self.test_03_post_create_page()

        page_list = Page.objects.filter(site=self.application.site)
        if page_list.count():
            response = self.client.get('/admin/application/' + self.guid + '/page/' + str(page_list[0].page_id) + '/edit/')
            self.assertEqual(response.status_code, 404)
        else:
            self.assertTrue(False, 'Не существует главной страницы приложения')

    def test_11_get_edit_page(self):
        """
        Вызов формы для редактирования реальной страницы
        """
        # dbt = db_templates.Template.objects.filter(sites=self.application.site)
        # if dbt.count():
        #     response = self.client.post('/admin/application/' + self.guid + '/page/create/', {
        #         'name': u'Краткое наименование',
        #         'title': u'Заголовок страницы',
        #         'alias': 'alias',
        #         'template': dbt[0].id,
        #         'main': False,
        #         'description': u'Мета-описание',
        #         'keywords': u'Мета-ключевые слова',
        #         'content': u'Основной контент'
        #     })
        #     self.assertEqual(response.status_code, 302)
        # else:
        #     self.assertTrue(False, 'Не существует базового шаблона для приложения')

        self.test_03_post_create_page()

        page_list = Page.objects.filter(site=self.application.site)
        if page_list.count():
            response = self.client.get('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/')
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(False, 'Не существует главной страницы приложения')

    def test_12_post_edit_page(self):
        """
        Редактирование страницы с совпадающим псевдонимом
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_13_post_edit_page(self):
        """
        Редактирование страницы с изменением псевдонима
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias1',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_14_post_edit_page(self):
        """
        Редактирование страницы без имени
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    # 'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 200)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_15_post_edit_page(self):
        """
        Редактирование страницы без заголовка
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    # 'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 200)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_16_post_edit_page(self):
        """
        Редактирование страницы без псевдонима
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    # 'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 200)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_17_post_edit_page(self):
        """
        Редактирование страницы без шаблона
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    # 'template': dbt[0].id,
                    # 'template-content': u"""
# <html>
# <head>
#     <title>Новый сайт</title>
# </head>
# <body>
# </body>
# </html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 200)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_18_post_edit_page(self):
        """
        Редактирование страницы без указания главной страницы
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    # 'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_19_post_edit_page(self):
        """
        Редактирование страницы без описания
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    # 'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_20_post_edit_page(self):
        """
        Редактирование страницы без ключевых слов
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    # 'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_21_post_edit_page(self):
        """
        Редактирование страницы без контента
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова'
                    # 'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_22_post_edit_page(self):
        """
        Редактирование страницы со спецсимволами
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Новый сайт&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;/body&gt;
&lt;/html&gt;""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова'
                    # 'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_23_post_edit_page(self):
        """
        Редактирование страницы с созданием копии
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Новый сайт&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;/body&gt;
&lt;/html&gt;""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент',
                    'new': 'new'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_24_post_edit_page(self):
        """
        Редактирование страницы с сохранением без закрытия
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Новый сайт&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;/body&gt;
&lt;/html&gt;""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент',
                    'lazy': 'lazy'
                })
                self.assertEqual(response.status_code, 204)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_25_post_edit_page(self):
        """
        Редактирование страницы со встраиваемым кодом
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        code = ExtCode.objects.create(site=self.application.site, name='code')
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'code': code.id,
                    'code-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })
                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_26_post_edit_page(self):
        """
        Редактирование страницы с изменением встраиваемого кода
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        code = ExtCode.objects.create(site=self.application.site, name='code')
        code1 = ExtCode.objects.create(site=self.application.site, name='code1')
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'code': code.id,
                    'code-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })

                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'code': code1.id,
                    'code-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })


                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')

    def test_27_post_edit_page(self):
        """
        Редактирование страницы с изменением встраиваемого кода
        """

        self.test_03_post_create_page()

        dbt = db_templates.Template.objects.filter(sites=self.application.site)
        code = ExtCode.objects.create(site=self.application.site, name='code')
        if dbt.count():
            page_list = Page.objects.filter(site=self.application.site)
            if page_list.count():
                self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'code': code.id,
                    'code-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': False,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })

                response = self.client.post('/admin/application/' + self.guid + '/page/' + page_list[0].alias + '/edit/', {
                    'name': u'Краткое наименование',
                    'title': u'Заголовок страницы',
                    'alias': 'alias',
                    'template': dbt[0].id,
                    'template-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'code': code.id,
                    'code-content': u"""
<html>
<head>
    <title>Новый сайт</title>
</head>
<body>
</body>
</html>""",
                    'main': True,
                    'description': u'Мета-описание',
                    'keywords': u'Мета-ключевые слова',
                    'content': u'Основной контент'
                })


                self.assertEqual(response.status_code, 302)
                # Page.objects.filter(site=self.application.site)
            else:
                self.assertTrue(False, 'Не существует главной страницы приложения')
        else:
            self.assertTrue(False, 'Не существует базового шаблона для приложения')
