# coding=cp1251
"""
Модели данных
"""

import django
from django.contrib.sites.models import Site
from django.db.models.loading import cache
from django.utils.datastructures import SortedDict
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib import admin
from django.db import models
from django.db.models.base import Model
import datetime
from django.db import connections
from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import clear_url_caches
from mptt.models import MPTTModel, TreeForeignKey
from dbtemplates import models as dbTemplates
import mptt
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.db.models.base import ModelBase
# import reversion
from django.db import transaction

try:
    reversion.register(dbTemplates.Template)
except:
    pass

'''
Вспомогательные классы для работы с MySql
'''


class Table(models.Model):
    table_catalog = models.CharField(max_length=1536, db_column='TABLE_CATALOG')
    table_schema = models.CharField(max_length=192, db_column='TABLE_SCHEMA')
    table_name = models.CharField(max_length=192, db_column='TABLE_NAME')
    table_type = models.CharField(max_length=192, db_column='TABLE_TYPE')
    engine = models.CharField(max_length=192, db_column='ENGINE', blank=True)
    version = models.BigIntegerField(null=True, db_column='VERSION', blank=True)
    row_format = models.CharField(max_length=30, db_column='ROW_FORMAT', blank=True)
    table_rows = models.BigIntegerField(null=True, db_column='TABLE_ROWS', blank=True)
    avg_row_length = models.BigIntegerField(null=True, db_column='AVG_ROW_LENGTH', blank=True)
    data_length = models.BigIntegerField(null=True, db_column='DATA_LENGTH', blank=True)
    max_data_length = models.BigIntegerField(null=True, db_column='MAX_DATA_LENGTH', blank=True)
    index_length = models.BigIntegerField(null=True, db_column='INDEX_LENGTH', blank=True)
    data_free = models.BigIntegerField(null=True, db_column='DATA_FREE', blank=True)
    auto_increment = models.BigIntegerField(null=True, db_column='AUTO_INCREMENT', blank=True)
    create_time = models.DateTimeField(null=True, db_column='CREATE_TIME', blank=True)
    update_time = models.DateTimeField(null=True, db_column='UPDATE_TIME', blank=True)
    check_time = models.DateTimeField(null=True, db_column='CHECK_TIME', blank=True)
    table_collation = models.CharField(max_length=96, db_column='TABLE_COLLATION', blank=True)
    checksum = models.BigIntegerField(null=True, db_column='CHECKSUM', blank=True)
    create_options = models.CharField(max_length=765, db_column='CREATE_OPTIONS', blank=True)
    table_comment = models.CharField(max_length=6144, db_column='TABLE_COMMENT')

    class Meta:
        db_table = u'tables'
        verbose_name = u'information schema mysql - таблица'
        verbose_name_plural = u'information schema mysql - таблицы'


class Column(models.Model):
    table_catalog = models.CharField(max_length=1536, db_column='TABLE_CATALOG')
    table_schema = models.CharField(max_length=192, db_column='TABLE_SCHEMA')
    table_name = models.CharField(max_length=192, db_column='TABLE_NAME')
    column_name = models.CharField(max_length=192, db_column='COLUMN_NAME')
    ordinal_position = models.BigIntegerField(db_column='ORDINAL_POSITION')
    column_default = models.TextField(db_column='COLUMN_DEFAULT', blank=True)
    is_nullable = models.CharField(max_length=9, db_column='IS_NULLABLE')
    data_type = models.CharField(max_length=192, db_column='DATA_TYPE')
    character_maximum_length = models.BigIntegerField(null=True, db_column='CHARACTER_MAXIMUM_LENGTH', blank=True)
    character_octet_length = models.BigIntegerField(null=True, db_column='CHARACTER_OCTET_LENGTH', blank=True)
    numeric_precision = models.BigIntegerField(null=True, db_column='NUMERIC_PRECISION', blank=True)
    numeric_scale = models.BigIntegerField(null=True, db_column='NUMERIC_SCALE', blank=True)
    character_set_name = models.CharField(max_length=96, db_column='CHARACTER_SET_NAME', blank=True)
    collation_name = models.CharField(max_length=96, db_column='COLLATION_NAME', blank=True)
    column_type = models.TextField(db_column='COLUMN_TYPE')
    column_key = models.CharField(max_length=9, db_column='COLUMN_KEY')
    extra = models.CharField(max_length=81, db_column='EXTRA')
    privileges = models.CharField(max_length=240, db_column='PRIVILEGES')
    column_comment = models.CharField(max_length=3072, db_column='COLUMN_COMMENT')

    class Meta:
        db_table = u'columns'
        verbose_name = u'information schema mysql - колонка'
        verbose_name_plural = u'information schema mysql - колонки'


'''
Хранение данных для анализа попыток взлома
'''


class Attack(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    ip = models.CharField(max_length=255, verbose_name=u'ip')
    url = models.CharField(max_length=1000, verbose_name=u'url')
    date_attack = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'attack'
        verbose_name = u'Атака'
        verbose_name_plural = u'Атаки'


'''
Классы системных сущностей

'''


class Version(models.Model):
    """
    Версионность базы
    """
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    number = models.CharField(max_length=10, verbose_name=u'Номер')
    svn_revision = models.CharField(max_length=10, verbose_name=u'Ревизия в хранилище')
    description = models.TextField(verbose_name=u'Описание', blank=True)
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'version'
        verbose_name = u'версия'
        verbose_name_plural = u'Версии'

    def __unicode__(self):
        return self.number


class Language(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    lang = models.CharField(max_length=10, verbose_name=u'Псевдоним')
    name = models.TextField(max_length=200, verbose_name=u'Язык')

    class Meta:
        db_table = u'language'
        verbose_name = u'язык'
        verbose_name_plural = u'Языки'

    def __unicode__(self):
        return self.name


class Localization(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    lang = models.ForeignKey(Language, db_column='lang', verbose_name=u'Язык')
    key = models.TextField(max_length=200, verbose_name=u'Ключ')
    string = models.TextField(max_length=200, verbose_name=u'Перевод')

    class Meta:
        db_table = u'localization'
        verbose_name = u'локализация'
        verbose_name_plural = u'Локализации'

    def __unicode__(self):
        return "%s/%s/%s" % (self.lang.lang, self.key, self.string)


class Application(models.Model):
    """
    Приложения
    """
    application_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'Имя')
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    alias = models.CharField(max_length=255, verbose_name=u'Псевдоним (eng)', unique=True)
    logotype = models.ImageField(upload_to='turbodiesel/images/admin', verbose_name=u'Логотип', db_column='image')
    default = models.BooleanField(verbose_name=u'По умолчанию')

    class Meta:
        db_table = u'application'
        verbose_name = u'Приложение'
        verbose_name_plural = u'Приложения'

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    telephone = models.TextField(verbose_name=u'Телефон', blank=True)
    #    application = models.ManyToManyField(Application, verbose_name=u'Приложение')#, through='ApplicationUser')
    class Meta:
        db_table = u'auth_user_profile'
        verbose_name = u'профиль пользователя'
        verbose_name_plural = u'Профили пользователей'


class ApplicationUser(models.Model):
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')
    user_profile = models.ForeignKey(UserProfile, db_column='user_profile_id', verbose_name=u'Пользователь')

    class Meta:
        db_table = u'application_user'


class ExtCode(models.Model):
    code_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')
    name = models.CharField(max_length=255, verbose_name=u'Имя', unique=True)
    code = models.TextField(verbose_name=u'Код расширения')
    is_global = models.BooleanField(verbose_name=u'Глобальный код', default=False)

    class Meta:
        db_table = u'ext_code'
        verbose_name = u'Кодовая вставка'
        verbose_name_plural = u'Кодовые вставки'

    def __unicode__(self):
        return self.name


class Page(models.Model):
    page_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'Краткое наименование')
    title = models.CharField(max_length=255, verbose_name=u'Заголовок страницы')
    alias = models.CharField(max_length=255, verbose_name=u'Имя в адресной строке')
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')
    template = models.ForeignKey(dbTemplates.Template, db_column='template_id', verbose_name=u'Шаблон')
    code = models.ForeignKey(ExtCode, db_column='code_id', verbose_name=u'Кодовая вставка', null=True, blank=True)
    main = models.BooleanField(default=False, verbose_name=u'Главная страница приложения')
    description = models.TextField(verbose_name=u'Мета-описание', null=True, blank=True)
    keywords = models.TextField(verbose_name=u'Мета-ключевые слова', null=True, blank=True)
    content = models.TextField(verbose_name=u'Основной контент', null=True, blank=True)

    class Meta:
        db_table = u'page'
        verbose_name = u'Страница'
        verbose_name_plural = u'Страницы'

    def __unicode__(self):
        return self.name


class Entity(models.Model):
    """
    Сущности
    """
    entity_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'Имя', unique=True)
    alias = models.CharField(max_length=255, verbose_name=u'Псевдоним (eng)', unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True)
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(verbose_name=u'Дата изменения', null=True, blank=True)
    image = models.ImageField(upload_to='turbodiesel/images/admin')
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')
    service = models.BooleanField(verbose_name=u'Серсисная сущность')

    class Meta:
        db_table = u'entity'
        verbose_name = u'сущность'
        verbose_name_plural = u'Сущности'

    def __unicode__(self):
        return self.name


class PropertyTypeUI(models.Model):
    """
    Типы аттрибутов интерфейса
    """
    property_type_ui_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=50, verbose_name=u'Имя')
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'property_type_ui'
        verbose_name = u'тип аттрибута интерфейса'
        verbose_name_plural = u'Типы аттрибутов интерфейса'

    def __unicode__(self):
        return self.name


class PropertyType(models.Model):
    """
    Типы аттрибутов
    """
    TYPE = (
        ('DATE', 'DATE'),
        ('DATETIME', 'DATETIME'),
        ('INTEGER', 'INTEGER'),
        ('BOOLEAN', 'BOOLEAN'),
        ('DOUBLE', 'DOUBLE'),
        ('TEXT', 'TEXT'),
        ('STRING', 'STRING'),
        ('ENTITY', 'ENTITY'),
        ('IMAGE', 'IMAGE'),
        ('EXTUSER', 'EXTUSER'),
    )
    property_type_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=50, verbose_name=u'Имя')
    dbtype = models.CharField(choices=TYPE, max_length=50, verbose_name=u'Тип в базе данных')
    description = models.TextField(blank=True, verbose_name=u'Описание')
    #    type_ui = models.ForeignKey(PropertyTypeUI, verbose_name=u'Тип пользовательского интерфейса')
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'property_type'
        verbose_name = u'тип аттрибута'
        verbose_name_plural = u'Типы аттрибутов'

    def __unicode__(self):
        return self.name


class Property(models.Model):
    """
    Аттрибуты
    """
    REF = (
        ('ONE2ONE', 'ONE2ONE'),
        ('ONE2MANY', 'ONE2MANY'),
    )

    property_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    label = models.CharField(max_length=100, verbose_name=u'Отображаемое имя')
    name = models.CharField(max_length=100, verbose_name=u'Идентификатор поля')
    description = models.TextField(verbose_name=u'Описание', blank=True)
    property_type = models.ForeignKey(PropertyType, verbose_name=u'Тип данных')
    link_entity = models.ForeignKey(Entity, verbose_name=u'Ссылка на сущность', blank=True, null=True,
                                    related_name='link_entity')
    #    reference = models.CharField(choices=REF, max_length=50, verbose_name=u'Тип связи', blank=True, null=True)
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)
    parent_entity = models.ForeignKey(Entity, verbose_name=u'Родительская сущность', related_name='parent_entity')
    visible = models.BooleanField(verbose_name=u'Показывать в колонках', default=True)
    caption = models.BooleanField(verbose_name=u'Показывать в содержимом', default=True)

    class Meta:
        db_table = u'property'
        verbose_name = u'аттрибут'
        verbose_name_plural = u'Аттрибуты'

    def __unicode__(self):
        return self.label


'''
Классы расширения функциональности приложений
'''


class ExtImage(models.Model):
    image_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')
    name = models.CharField(max_length=255, verbose_name=u'Имя', unique=True)
    alias = models.CharField(max_length=255, verbose_name=u'Псевдоним (eng)', unique=True)
    image = models.ImageField(upload_to='turbodiesel/images/application', verbose_name=u'Изображение')

    class Meta:
        db_table = u'ext_image'
        verbose_name = u'Картинка'
        verbose_name_plural = u'Картинки'

    def __unicode__(self):
        return self.name


class ExtFilter(models.Model):
    filter_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')
    name = models.CharField(max_length=255, verbose_name=u'Имя', unique=True)
    alias = models.CharField(max_length=255, verbose_name=u'Псевдоним', unique=True, db_column='alias')
    entity = models.ForeignKey(Entity, verbose_name=u'Сущность', blank=False, null=False, related_name='entity')
    expression = models.TextField(verbose_name=u'Фильтр', blank=True, null=True)
    extra = models.TextField(verbose_name=u'Дополнение к фильтру', blank=True, null=True)
    groupby = models.TextField(verbose_name=u'Группировка', blank=True, null=True)

    class Meta:
        db_table = u'ext_filter'
        verbose_name = u'Фильтр'
        verbose_name_plural = u'Фильтры'

    def __unicode__(self):
        return self.name


class FilterOnPage(models.Model):
    filter_on_page_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    page = models.ForeignKey(Page, db_column='page_id', verbose_name=u'Страница приложения', blank=False, null=False,
                             related_name='page')
    filter = models.ForeignKey(ExtFilter, db_column='filter_id', verbose_name=u'Фильтр', blank=False, null=False,
                               related_name='filter')

    class Meta:
        db_table = u'filter_on_page'
        verbose_name = u'Фильтр на странице'
        verbose_name_plural = u'Фильтры на странице'

    def __unicode__(self):
        return '%s - %s' % (self.page.name, self.filter.name)


class ExtWorkflow(models.Model):
    workflow_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'Имя')
    description = models.CharField(max_length=1000, verbose_name=u'Описание')
    application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'Приложение')

    class Meta:
        db_table = u'ext_workflow'
        verbose_name = u'Рабочий процесс'
        verbose_name_plural = u'Рабочие процессы'


class ExtStatus(models.Model):
    status_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'Имя')
    workflow = models.ForeignKey(ExtWorkflow, db_column='workflow_id', verbose_name=u'Рабочий процесс', blank=False,
                                 null=False, related_name='workflow')

    class Meta:
        db_table = u'ext_status'
        verbose_name = u'Состояние'
        verbose_name_plural = u'Состояния'


class ExtEdge(models.Model):
    edge_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'Имя')
    previous = models.ManyToManyField(ExtStatus, verbose_name=u'Предыдущий статус')  #, through='PreviousStatus')
    action = models.ManyToManyField(ExtCode, verbose_name=u'Выполняемые действия')  #, through='EdgeCode')
    target = models.ForeignKey(ExtStatus, db_column='target_id', verbose_name=u'Следующий статус', blank=False,
                               null=False, related_name='target')

    class Meta:
        db_table = u'ext_edge'
        verbose_name = u'Переход'
        verbose_name_plural = u'Переходы'


class PreviousStatus(models.Model):
    edge = models.ForeignKey(ExtEdge, db_column='edge_id', verbose_name=u'Переход')
    status = models.ForeignKey(ExtStatus, db_column='status_id', verbose_name=u'Переходы')

    class Meta:
        db_table = u'previous_status'


class EdgeCode(models.Model):
    edge = models.ForeignKey(ExtEdge, db_column='edge_id', verbose_name=u'Переход')
    code = models.ForeignKey(ExtCode, db_column='code_id', verbose_name=u'Коды')

    class Meta:
        db_table = u'edge_code'


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1
    fk_name = 'parent_entity'


class PageInline(admin.TabularInline):
    model = Page
    extra = 1


class ImageInline(admin.TabularInline):
    model = ExtImage
    extra = 1


def create_model(entity, inline):
    if entity.alias != "":
        properties = {'id': models.AutoField(primary_key=True, verbose_name='id', db_column='id')}
        for property in Property.objects.filter(parent_entity=entity):
            property_type = PropertyType.objects.get(property=property)
            if property_type.dbtype == 'DATE':
                properties[property.name] = models.DateField(db_column=property.name, verbose_name=property.label,
                                                             blank=True, null=True)
            elif property_type.dbtype == 'DATETIME':
                properties[property.name] = models.DateTimeField(db_column=property.name, verbose_name=property.label,
                                                                 blank=True, null=True)
            elif property_type.dbtype == 'INTEGER':
                properties[property.name] = models.IntegerField(db_column=property.name, verbose_name=property.label,
                                                                blank=True, null=True)
            elif property_type.dbtype == 'DOUBLE':
                properties[property.name] = models.FloatField(db_column=property.name, verbose_name=property.label,
                                                              blank=True, null=True)
            elif property_type.dbtype == 'BOOLEAN':
                properties[property.name] = models.BooleanField(db_column=property.name, verbose_name=property.label,
                                                                default=True)
            elif property_type.dbtype == 'TEXT':
                properties[property.name] = models.TextField(db_column=property.name, verbose_name=property.label,
                                                             blank=True, null=True)
            elif property_type.dbtype == 'STRING':
                properties[property.name] = models.CharField(max_length=1000, db_column=property.name,
                                                             verbose_name=property.label, blank=True, null=True)
            elif property_type.dbtype == 'IMAGE':
                properties[property.name] = models.ImageField(upload_to='turbodiesel/images/entity/' + entity.alias,
                                                              db_column=property.name, verbose_name=property.label,
                                                              blank=True, null=True)
            elif property.property_type.dbtype == 'ENTITY':
                if not globals().__contains__('nature_' + property.link_entity.alias):
                    foreign_entity = Entity.objects.filter(alias=property.link_entity.alias)
                    if len(foreign_entity) > 0:
                        create_model(foreign_entity[0], inline)
                properties[property.name] = models.ForeignKey(globals()['nature_' + property.link_entity.alias],
                                                              db_column=property.name, verbose_name=property.label,
                                                              blank=True, null=True,
                                                              related_name='%s_%s' % (entity.alias, property.name))
            elif property.property_type.dbtype == 'EXTUSER':
                properties[property.name] = models.ForeignKey(User, db_column=property.name,
                                                              verbose_name=property.label,
                                                              related_name='%s_%s' % (entity.alias, property.name))

    properties['Meta'] = type('Meta', (),
                              {'db_table': 'nature_' + entity.alias, 'verbose_name_plural': entity.name.encode('utf8'),
                               'verbose_name': entity.name.lower().encode('utf8')})
    properties['__module__'] = 'nature.models'
    properties['entity'] = entity

    def __unicode__(self):
        title = u''
        fields = Property.objects.filter(parent_entity=entity)
        for field in fields:
            if field.caption:
                if field.link_entity:
                    try:
                        title = title + u" %s," % (self.__getattribute__(field.name))
                    except:
                        title = title + u"%s=''," % (field.name)
                else:
                    title = title + u" %s," % (self.__getattribute__(field.name))
        return title[0:-1]

    properties['__unicode__'] = __unicode__
    model = type(entity.alias.encode('cp1251'), (models.Model,), properties)
    globals()['nature_' + entity.alias] = model
    inline[globals()['nature_' + entity.alias]] = []

    return model


def collect_entity():
    """

    """
    inline = {}
    for entity in Entity.objects.all():
        create_model(entity, inline)

    collection = [globals()[l] for l in globals().keys() if (
        type(globals()[l]) == django.db.models.base.ModelBase or type(globals()[l]) == mptt.models.MPTTModelBase)
                  and (issubclass(globals()[l], Model) or issubclass(globals()[l], MPTTModel))
                  and globals()[l] not in [django.contrib.auth.models.User, django.db.models.base.Model,
                                           django.contrib.auth.models.Group, mptt.models.MPTTModel]]

    site = admin.site

    for cl in collection:
        properties = [property.__dict__['name'] for property in cl.__dict__['_meta'].__dict__['local_fields']]
        list_display = properties[:]
        list_display.append(list_display[0])
        list_display.remove(list_display[0])

        #properties.append(properties[0])
        properties.remove(properties[0])
        properties = properties + [property.__dict__['name'] for property in
                                   cl.__dict__['_meta'].__dict__['local_many_to_many']]

        st = cl._meta.object_name
        list_filter = []
        search_properties = []
        if st == 'Table' or st == 'Column' or st == 'SqliteMaster':
            continue

        #        cladmin = type(st + 'Admin', (admin.ModelAdmin,), dict(fields=properties, list_per_page=100, list_filter=list_filter, search_properties=search_properties))
        cladmin = type(st + 'Admin', (admin.ModelAdmin,),
                       dict(fields=properties, list_display=list_display, list_per_page=100, list_filter=list_filter,
                            search_properties=search_properties))

        if cladmin.__name__ in ('EntityAdmin'):
            cladmin.inlines = (PropertyInline, )
        if cladmin.__name__ in ('ApplicationAdmin'):
            cladmin.inlines = (PageInline, ImageInline)

        if inline.__contains__(cl):
            for entity in inline[cl]:
                entity_inline = type(str(entity.alias) + 'Inline', (admin.TabularInline,),
                                     dict(extra=1, model=globals()['nature_' + entity.alias]))
                cladmin.inlines = (entity_inline,)

        for reg_model in site._registry.keys():
            if cl._meta.db_table == reg_model._meta.db_table:
                del site._registry[reg_model]
        try:
            admin.site.unregister(cl)
        except:
            pass

        admin.site.register(cl, cladmin)
        try:
            reversion.register(cl)
        except:
            pass
        pre_save.connect(pre_save_model, sender=cl)

        post_save.connect(post_save_model, sender=cl)
        post_delete.connect(post_delete_model, sender=cl)

        clear_url_caches()
        reload(import_module(settings.ROOT_URLCONF))


def clear_cache(app, model):
    cached_models = cache.app_models.get(app)
    if cached_models.has_key(model.lower()):
        del cached_models[model.lower()]


def pre_save_model(sender, **kwargs):
    if kwargs['instance']._meta.object_name == 'ExtImage':
        kwargs['instance'].image.field.upload_to = 'turbodiesel/images/application/%s/' % kwargs[
            'instance'].application.alias


def post_save_model(sender, **kwargs):
    cursor = connections['default'].cursor()
    if kwargs['created']:
        if kwargs['instance']._meta.object_name == 'Entity':
            qset = Table.objects.using('metadata').values_list('table_name', 'table_schema').filter(
                table_name=kwargs['instance'].alias, table_schema='turbodiesel')
            if len(qset) == 0:
                sql = """
CREATE TABLE `nature_%s` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 PRIMARY KEY (`id`)
) AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
               """ % (kwargs['instance'].alias)
                cursor.execute(sql)
        if kwargs['instance']._meta.object_name == 'Property':
            if kwargs['instance'].property_type.dbtype == 'ENTITY' or kwargs[
                'instance'].property_type.dbtype == 'EXTUSER':
                if kwargs['instance'].property_type.dbtype == 'EXTUSER':
                    option = {'table': kwargs['instance'].parent_entity.alias, 'column': kwargs['instance'].name,
                              'foreign': 'auth_user', 'nature': ''}
                else:
                    option = {'table': kwargs['instance'].parent_entity.alias, 'column': kwargs['instance'].name,
                              'foreign': kwargs['instance'].link_entity.alias, 'nature': 'nature_'}
                sql = """
    ALTER TABLE `nature_%(table)s` ADD COLUMN `%(column)s` INT NULL,
    ADD CONSTRAINT `fk_nature_%(table)s_%(foreign)s_%(column)s`
    FOREIGN KEY (`%(column)s` )
    REFERENCES `%(nature)s%(foreign)s` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    , ADD INDEX `fk_nature_%(table)s_%(foreign)s_%(column)s` (`%(column)s` ASC) ;""" % option
            elif kwargs['instance'].property_type.dbtype == 'STRING':
                sql = """
ALTER TABLE `nature_%s` ADD COLUMN `%s` varchar(1000) NULL;
           """ % (kwargs['instance'].parent_entity.alias, kwargs['instance'].name)
            elif kwargs['instance'].property_type.dbtype == 'IMAGE':
                sql = """
ALTER TABLE `nature_%s` ADD COLUMN `%s` varchar(1000) NULL;
           """ % (kwargs['instance'].parent_entity.alias, kwargs['instance'].name)
            else:
                sql = """
ALTER TABLE `nature_%s` ADD COLUMN `%s` %s NULL;
           """ % (kwargs['instance'].parent_entity.alias, kwargs['instance'].name,
                  kwargs['instance'].property_type.dbtype)
            try:
                cursor.execute(sql)
                connections['default'].commit()
            except Exception, e:
                pass

    if kwargs['instance']._meta.object_name == 'Entity':
        clear_cache('nature', kwargs['instance'].alias)
    elif kwargs['instance']._meta.object_name == 'Property' and kwargs['created']:
        clear_cache('nature', kwargs['instance'].parent_entity.alias)

    collect_entity()


def post_delete_model(sender, **kwargs):
    if kwargs['instance']._meta.object_name == 'Entity':
        cursor = connections['default'].cursor()
        now = datetime.datetime.now()
        delete_date = now.strftime("%Y%m%d%H%M%S")
        sql = "ALTER TABLE `nature_%s` RENAME TO  `_delete_%s_nature_%s`;" % (
            kwargs['instance'].alias, delete_date, kwargs['instance'].alias)
        cursor.execute(sql)
        try:
            admin.site.unregister(globals()['nature_' + kwargs['instance'].alias])
            del globals()['nature_' + kwargs['instance'].alias]
        except Exception, e:
            pass
        clear_cache('nature', kwargs['instance'].alias)
    elif kwargs['instance']._meta.object_name == 'Property':
        clear_cache('nature', kwargs['instance'].parent_entity.alias)
    collect_entity()


_application_map = {}
_entity_map = {}


def get_application_instance(application_alias, request):
    if application_alias is None:
        raise Exception(u'Недопустимая операция при выборе приложения, не указан объект запроса')

    application = _application_map.get(application_alias, None)
    if application is not None:
        return (application, False)
    if request.META.get('PATH_INFO') != '/':
        instance_list = Application.objects.filter(alias=application_alias)
        if len(instance_list):
            _application_map[application_alias] = instance_list[0]
            return (instance_list[0], False)
        else:
            a = Attack.objects.create(ip=request.META.get('HTTP_X_REAL_IP'),
                                      url=request.META.get('PATH_INFO'), date_attack=datetime.datetime.now())
            transaction.commit()

    instance_list = Application.objects.filter(default=True)
    if len(instance_list):
        _application_map[application_alias] = instance_list[0]
        return (instance_list[0], True)
    else:
        raise Exception(u'Приложения "%s" не существует' % (application_alias))


def get_entity_instance(request, entity_alias=None, application_alias=None):
    if entity_alias is None and application_alias is None:
        raise Exception(u'Недопустимая операция при выборе приложения, не указан объект запроса')

    application, default = get_application_instance(application_alias, request)

    classname = ''
    classname_list = [ext['ClassName'] for ext in settings.EXTENSIONS if ext['TableName'] == entity_alias]
    if len(classname_list):
        classname = classname_list[0]
    if globals().__contains__(classname):
        model = globals()[classname]
        return model

    instance_list = Entity.objects.filter(alias=entity_alias, application=application)
    if len(instance_list):
        entity = instance_list[0]
        return entity
    else:
        raise Exception(u'Сущности "%s" не существует' % entity_alias)


def get_model(request, entity_alias, application_alias):
    model = None
    classname_list = [ext['ClassName'] for ext in settings.EXTENSIONS if ext['TableName'] == entity_alias]
    classname = entity_alias
    if len(classname_list):
        classname = classname_list[0]
    if globals().__contains__(classname):
        model = globals()[classname]
        if classname == 'dbTemplates':
            model = model.Template
    else:
        instance = get_entity_instance(request, entity_alias, application_alias)
        if type(instance) is not ModelBase:
            model = create_model(instance, {})
        else:
            model = instance
    return model


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


def __unicode__(self):
    return '%s %s' % (self.last_name, self.first_name)


User.__unicode__ = __unicode__

collect_entity()

