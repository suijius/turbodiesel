# coding=cp1251
"""
������ ������
"""

import datetime

import django
from django.apps import AppConfig
from django.core.urlresolvers import clear_url_caches
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models.loading import cache
from django.db.models.signals import post_save, post_delete, pre_save
from django.db import models
from django.db.models.base import Model
from django.db import connections
from django.db.models.base import ModelBase
from django.db import transaction
from django.utils.importlib import import_module
from dbtemplates import models as db_templates
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

# try:
#     reversion.register(dbTemplates.Template)
# except:
#     pass

'''
��������������� ������ ��� ������ � MySql
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
        verbose_name = u'information schema mysql - �������'
        verbose_name_plural = u'information schema mysql - �������'


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
        verbose_name = u'information schema mysql - �������'
        verbose_name_plural = u'information schema mysql - �������'


class Attack(models.Model):
    u"""
    �������� ������ ��� ������� ������� ������
    """
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    ip = models.CharField(max_length=255, verbose_name=u'ip')
    url = models.CharField(max_length=1000, verbose_name=u'url')
    date_attack = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'attack'
        verbose_name = u'�����'
        verbose_name_plural = u'�����'


'''
������ ��������� ���������

'''


class Version(models.Model):
    u"""
    ������������ ����
    """
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    number = models.CharField(max_length=10, verbose_name=u'�����')
    svn_revision = models.CharField(max_length=10, verbose_name=u'������� � ���������')
    description = models.TextField(verbose_name=u'��������', blank=True)
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'version'
        verbose_name = u'������'
        verbose_name_plural = u'������'

    def __unicode__(self):
        return self.number


class Language(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    lang = models.CharField(max_length=10, verbose_name=u'���������')
    name = models.TextField(max_length=200, verbose_name=u'����')

    class Meta:
        db_table = u'language'
        verbose_name = u'����'
        verbose_name_plural = u'�����'

    def __unicode__(self):
        return self.name


class Localization(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    lang = models.ForeignKey(Language, db_column='lang', verbose_name=u'����')
    key = models.TextField(max_length=200, verbose_name=u'����')
    string = models.TextField(max_length=200, verbose_name=u'�������')

    class Meta:
        db_table = u'localization'
        verbose_name = u'�����������'
        verbose_name_plural = u'�����������'

    def __unicode__(self):
        return "%s/%s/%s" % (self.lang.lang, self.key, self.string)


class Application(models.Model):
    """
    ����������
    """
    # application_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'���')
    title = models.CharField(max_length=255, verbose_name=u'���������')
    alias = models.CharField(max_length=255, verbose_name=u'��������� (eng)', unique=True)
    logotype = models.ImageField(upload_to='turbodiesel/images/admin', verbose_name=u'�������', db_column='image')
    default = models.BooleanField(verbose_name=u'�� ���������')
    site = models.OneToOneField(Site, primary_key=True)

    class Meta:
        db_table = u'application'
        verbose_name = u'����������'
        verbose_name_plural = u'����������'

    def __unicode__(self):
        return self.name


# class Rule(models.Model):
#     """
#     ����
#     """
#     rule_id = models.AutoField(primary_key=True, verbose_name=u'ID')
#     name = models.CharField(max_length=255, verbose_name=u'���')
#     parent = models.ForeignKey('Rule', db_column='parent', null=True, blank=True)
#     application = models.ForeignKey(Application, db_column='application')
#
#     class Meta:
#         db_table = u'rule'
#         verbose_name = u'����'
#         verbose_name_plural = u'����'
#
#     def __unicode__(self):
#         return self.name


# class Operation(models.Model):
#     """
#     ��������
#     """
#     operation_id = models.AutoField(primary_key=True, verbose_name=u'ID')
#     name = models.CharField(max_length=255, verbose_name=u'���')
#     description = models.TextField(verbose_name=u'��������')
#
#     class Meta:
#         db_table = u'operation'
#         verbose_name = u'��������'
#         verbose_name_plural = u'��������'
#
#     def __unicode__(self):
#         return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    telephone = models.TextField(verbose_name=u'�������', blank=True)
    sites = models.ManyToManyField(Site)
    # application = models.ManyToManyField(Application, verbose_name=u'����������')#, through='ApplicationUser')

    class Meta:
        db_table = u'auth_user_profile'
        verbose_name = u'������� ������������'
        verbose_name_plural = u'������� �������������'


# class ApplicationUser(models.Model):
#     application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
#     user_profile = models.ForeignKey(UserProfile, db_column='user_profile_id', verbose_name=u'������������')
#
#     class Meta:
#         db_table = u'application_user'


class ExtCode(models.Model):
    id = models.AutoField(db_column='code_id', primary_key=True, verbose_name=u'ID')
    # application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
    name = models.CharField(max_length=255, verbose_name=u'���', unique=True)
    code = models.TextField(verbose_name=u'��� ����������')
    is_global = models.BooleanField(verbose_name=u'���������� ���', default=False)
    site = models.ForeignKey(Site)

    class Meta:
        db_table = u'ext_code'
        verbose_name = u'������� �������'
        verbose_name_plural = u'������� �������'

    def __unicode__(self):
        return self.name


class Page(models.Model):
    page_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'������� ������������')
    title = models.CharField(max_length=255, verbose_name=u'��������� ��������')
    alias = models.CharField(max_length=255, verbose_name=u'��� � �������� ������')
    # application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
    template = models.ForeignKey(db_templates.Template, db_column='template_id', verbose_name=u'������')
    code = models.ForeignKey(ExtCode, db_column='code_id', verbose_name=u'������� �������', null=True, blank=True)
    main = models.BooleanField(default=False, verbose_name=u'������� �������� ����������')
    description = models.TextField(verbose_name=u'����-��������', null=True, blank=True)
    keywords = models.TextField(verbose_name=u'����-�������� �����', null=True, blank=True)
    content = models.TextField(verbose_name=u'�������� �������', null=True, blank=True)
    site = models.ForeignKey(Site)

    class Meta:
        db_table = u'page'
        verbose_name = u'��������'
        verbose_name_plural = u'��������'

    def __unicode__(self):
        return self.name


class Entity(models.Model):
    """
    ��������
    """
    entity_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'���', unique=True)
    alias = models.CharField(max_length=255, verbose_name=u'��������� (eng)', unique=True)
    description = models.TextField(verbose_name=u'��������', blank=True)
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(verbose_name=u'���� ���������', null=True, blank=True)
    image = models.ImageField(upload_to='turbodiesel/images/admin')
    # application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
    service = models.BooleanField(verbose_name=u'��������� ��������')
    site = models.ForeignKey(Site)

    class Meta:
        db_table = u'entity'
        verbose_name = u'��������'
        verbose_name_plural = u'��������'

    def __unicode__(self):
        return self.name


# class Access(models.Model):
#     """
#     �������
#     """
#     access_id = models.AutoField(primary_key=True, verbose_name=u'ID')
#     operation_id = models.ForeignKey(Operation, verbose_name=u'��������')
#     entity_id = models.ForeignKey(Entity, verbose_name=u'��������')
#     rule_id = models.ForeignKey(Rule, verbose_name=u'����')
#     object_id = models.IntegerField(verbose_name=u'������')
#
#     class Meta:
#         db_table = u'access'
#         verbose_name = u'������'
#         verbose_name_plural = u'�������'
#
#     def __unicode__(self):
#         return self.name


# class PropertyTypeUI(models.Model):
#     """
#     ���� ���������� ����������
#     """
#     property_type_ui_id = models.AutoField(primary_key=True, verbose_name=u'ID')
#     name = models.CharField(max_length=50, verbose_name=u'���')
#     editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
#     date_change = models.DateTimeField(null=True, blank=True)
#
#     class Meta:
#         db_table = u'property_type_ui'
#         verbose_name = u'��� ��������� ����������'
#         verbose_name_plural = u'���� ���������� ����������'
#
#     def __unicode__(self):
#         return self.name


class PropertyType(models.Model):
    """
    ���� ����������
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
        ('WORKFLOW', 'WORKFLOW'),
    )
    property_type_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=50, verbose_name=u'���')
    dbtype = models.CharField(choices=TYPE, max_length=50, verbose_name=u'��� � ���� ������')
    description = models.TextField(blank=True, verbose_name=u'��������')
    # type_ui = models.ForeignKey(PropertyTypeUI, verbose_name=u'��� ����������������� ����������')
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'property_type'
        verbose_name = u'��� ���������'
        verbose_name_plural = u'���� ����������'

    def __unicode__(self):
        return self.name


class Property(models.Model):
    """
    ���������
    """
    REF = (
        ('ONE2ONE', 'ONE2ONE'),
        ('ONE2MANY', 'ONE2MANY'),
    )

    property_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    label = models.CharField(max_length=100, verbose_name=u'������������ ���')
    name = models.CharField(max_length=100, verbose_name=u'������������� ����')
    description = models.TextField(verbose_name=u'��������', blank=True)
    property_type = models.ForeignKey(PropertyType, verbose_name=u'��� ������')
    link_entity = models.ForeignKey(Entity, verbose_name=u'������ �� ��������', blank=True, null=True,
                                    related_name='link_entity')
    # reference = models.CharField(choices=REF, max_length=50, verbose_name=u'��� �����', blank=True, null=True)
    editor = models.ForeignKey(User, db_column='editor', null=True, blank=True)
    date_change = models.DateTimeField(null=True, blank=True)
    parent_entity = models.ForeignKey(Entity, verbose_name=u'������������ ��������', related_name='parent_entity')
    visible = models.BooleanField(verbose_name=u'���������� � ��������', default=True)
    caption = models.BooleanField(verbose_name=u'���������� � ����������', default=True)

    class Meta:
        db_table = u'property'
        verbose_name = u'��������'
        verbose_name_plural = u'���������'

    def __unicode__(self):
        return self.label


'''
������ ���������� ���������������� ����������
'''


class ExtImage(models.Model):
    id = models.AutoField(db_column='image_id', primary_key=True, verbose_name=u'ID')
    # application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
    name = models.CharField(max_length=255, verbose_name=u'���', unique=True)
    alias = models.CharField(max_length=255, verbose_name=u'��������� (eng)', unique=True)
    image = models.ImageField(upload_to='turbodiesel/images/application', verbose_name=u'�����������')
    site = models.ForeignKey(Site)

    class Meta:
        db_table = u'ext_image'
        verbose_name = u'��������'
        verbose_name_plural = u'��������'

    def __unicode__(self):
        return self.name


class ExtFilter(models.Model):
    id = models.AutoField(db_column='filter_id', primary_key=True, verbose_name=u'ID')
    # application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
    name = models.CharField(max_length=255, verbose_name=u'���', unique=True)
    alias = models.CharField(max_length=255, verbose_name=u'���������', unique=True, db_column='alias')
    entity = models.ForeignKey(Entity, verbose_name=u'��������', blank=False, null=False, related_name='entity')
    expression = models.TextField(verbose_name=u'������', blank=True, null=True)
    extra = models.TextField(verbose_name=u'���������� � �������', blank=True, null=True)
    groupby = models.TextField(verbose_name=u'�����������', blank=True, null=True)
    site = models.ForeignKey(Site)

    class Meta:
        db_table = u'ext_filter'
        verbose_name = u'������'
        verbose_name_plural = u'�������'

    def __unicode__(self):
        return self.name


class FilterOnPage(models.Model):
    filter_on_page_id = models.AutoField(primary_key=True, verbose_name=u'ID')
    page = models.ForeignKey(Page, db_column='page_id', verbose_name=u'�������� ����������', blank=False, null=False,
                             related_name='page')
    filter = models.ForeignKey(ExtFilter, db_column='filter_id', verbose_name=u'������', blank=False, null=False,
                               related_name='filter')

    class Meta:
        db_table = u'filter_on_page'
        verbose_name = u'������ �� ��������'
        verbose_name_plural = u'������� �� ��������'

    def __unicode__(self):
        return '%s - %s' % (self.page.name, self.filter.name)


class ExtWorkflow(models.Model):
    id = models.AutoField(db_column='workflow_id', primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'���')
    description = models.CharField(max_length=1000, verbose_name=u'��������')
    # application = models.ForeignKey(Application, db_column='application_id', verbose_name=u'����������')
    site = models.ForeignKey(Site)

    class Meta:
        db_table = u'ext_workflow'
        verbose_name = u'������� �������'
        verbose_name_plural = u'������� ��������'


class ExtStatus(models.Model):
    id = models.AutoField(db_column='status_id', primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'���')
    workflow = models.ForeignKey(ExtWorkflow, db_column='workflow_id', verbose_name=u'������� �������', blank=False,
                                 null=False, related_name='workflow')

    class Meta:
        db_table = u'ext_status'
        verbose_name = u'���������'
        verbose_name_plural = u'���������'


class ExtEdge(models.Model):
    id = models.AutoField(db_column='edge_id', primary_key=True, verbose_name=u'ID')
    name = models.CharField(max_length=255, verbose_name=u'���')
    previous = models.ManyToManyField(ExtStatus, verbose_name=u'���������� ������')  # , through='PreviousStatus')
    action = models.ManyToManyField(ExtCode, verbose_name=u'����������� ��������')  # , through='EdgeCode')
    target = models.ForeignKey(ExtStatus, db_column='target_id', verbose_name=u'��������� ������', blank=False,
                               null=False, related_name='target')

    class Meta:
        db_table = u'ext_edge'
        verbose_name = u'�������'
        verbose_name_plural = u'��������'


class PreviousStatus(models.Model):
    edge = models.ForeignKey(ExtEdge, db_column='edge_id', verbose_name=u'�������')
    status = models.ForeignKey(ExtStatus, db_column='status_id', verbose_name=u'��������')

    class Meta:
        db_table = u'previous_status'


class EdgeCode(models.Model):
    edge = models.ForeignKey(ExtEdge, db_column='edge_id', verbose_name=u'�������')
    code = models.ForeignKey(ExtCode, db_column='code_id', verbose_name=u'����')

    class Meta:
        db_table = u'edge_code'


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1
    fk_name = 'parent_entity'


# class PageInline(admin.TabularInline):
#     model = Page
#     extra = 1


# class ImageInline(admin.TabularInline):
#     model = ExtImage
#     extra = 1


def create_model(entity, inline):
    if entity.alias != "":
        properties = {'id': models.AutoField(primary_key=True, verbose_name='id', db_column='id')}
        for prop in Property.objects.filter(parent_entity=entity):
            property_type = PropertyType.objects.get(property=prop)
            if property_type.dbtype == 'DATE':
                properties[prop.name] = models.DateField(db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif property_type.dbtype == 'DATETIME':
                properties[prop.name] = models.DateTimeField(db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif property_type.dbtype == 'INTEGER':
                properties[prop.name] = models.IntegerField(db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif property_type.dbtype == 'DOUBLE':
                properties[prop.name] = models.FloatField(db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif property_type.dbtype == 'BOOLEAN':
                properties[prop.name] = models.BooleanField(db_column=prop.name, verbose_name=prop.label, default=True)
            elif property_type.dbtype == 'TEXT':
                properties[prop.name] = models.TextField(db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif property_type.dbtype == 'STRING':
                properties[prop.name] = models.CharField(max_length=1000, db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif property_type.dbtype == 'IMAGE':
                properties[prop.name] = models.ImageField(upload_to='turbodiesel/images/entity/' + entity.alias, db_column=prop.name, verbose_name=prop.label, blank=True, null=True)
            elif prop.property_type.dbtype == 'ENTITY':
                if not globals().__contains__('nature_' + prop.link_entity.alias):
                    foreign_entity = Entity.objects.filter(alias=prop.link_entity.alias)
                    if len(foreign_entity) > 0:
                        create_model(foreign_entity[0], inline)
                properties[prop.name] = models.ForeignKey(globals()['nature_' + prop.link_entity.alias],
                                                          db_column=prop.name, verbose_name=prop.label,
                                                          blank=True, null=True,
                                                          related_name='%s_%s' % (entity.alias, prop.name))
            elif prop.property_type.dbtype == 'EXTUSER':
                properties[prop.name] = models.ForeignKey(User, db_column=prop.name,
                                                          verbose_name=prop.label,
                                                          related_name='%s_%s' % (entity.alias, prop.name))

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
                            title += u" %s," % (self.__getattribute__(field.name))
                        except:
                            title += u"%s=''," % field.name
                    else:
                        title += u" %s," % (self.__getattribute__(field.name))
            return title[0:-1]

        properties['__unicode__'] = __unicode__
        if globals().get('nature_' + entity.alias, None) is None:
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
        type(globals()[l]) == django.db.models.base.ModelBase)
        and (issubclass(globals()[l], Model))
        and globals()[l] not in [django.contrib.auth.models.User, django.db.models.base.Model, django.contrib.auth.models.Group]]

    '''
    � �������������� ��������
    '''
    # collection = [globals()[l] for l in globals().keys() if (
    # type(globals()[l]) == django.db.models.base.ModelBase or type(globals()[l]) == mptt.models.MPTTModelBase)
    # and (issubclass(globals()[l], Model) or issubclass(globals()[l], MPTTModel))
    # and globals()[l] not in [django.contrib.auth.models.User, django.db.models.base.Model, django.contrib.auth.models.Group, mptt.models.MPTTModel]]

    site = admin.site

    for cl in collection:
        properties = [property.__dict__['name'] for property in cl.__dict__['_meta'].__dict__['local_fields']]
        list_display = properties[:]
        list_display.append(list_display[0])
        list_display.remove(list_display[0])

        # properties.append(properties[0])
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

        if cladmin.__name__ in 'EntityAdmin':
            cladmin.inlines = (PropertyInline, )
        # if cladmin.__name__ in 'ApplicationAdmin':
        #     cladmin.inlines = (PageInline, ImageInline)

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
        # try:
        #     reversion.register(cl)
        # except:
        #     pass
        pre_save.connect(pre_save_model, sender=cl)

        post_save.connect(post_save_model, sender=cl)
        post_delete.connect(post_delete_model, sender=cl)

        clear_url_caches()
        reload(import_module(settings.ROOT_URLCONF))


def clear_cache(app, model):
    cached_models = cache.app_models.get(app)
    # if cached_models.has_key(model.lower()):
    #     del cached_models[model.lower()]

    if model.lower() in cached_models:
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
               """ % kwargs['instance'].alias
                cursor.execute(sql)
        if kwargs['instance']._meta.object_name == 'Property':
            if kwargs['instance'].property_type.dbtype == 'ENTITY' or kwargs['instance'].property_type.dbtype == 'EXTUSER':
                if kwargs['instance'].property_type.dbtype == 'EXTUSER':
                    option = {'table': kwargs['instance'].parent_entity.alias, 'column': kwargs['instance'].name, 'foreign': 'auth_user', 'nature': ''}
                else:
                    option = {'table': kwargs['instance'].parent_entity.alias, 'column': kwargs['instance'].name, 'foreign': kwargs['instance'].link_entity.alias, 'nature': 'nature_'}
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
            except:
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
        except:
            pass
        clear_cache('nature', kwargs['instance'].alias)
    elif kwargs['instance']._meta.object_name == 'Property':
        clear_cache('nature', kwargs['instance'].parent_entity.alias)
    collect_entity()


_application_map = {}
_entity_map = {}


def get_application_instance(application_alias, request):
    """
    ��������� ���������� ����������
    :param application_alias: ��������� ����������
    :param request: HTTP ������
    :return: ��������� ����������
    """
    if application_alias is None:
        raise Exception(u'������������ �������� ��� ������ ����������, �� ������ ������ �������')

    # ������� �������� ��������� ���������� �� ����
    application = _application_map.get(application_alias, None)
    if application is not None:
        return application

    # ������� �������� ��������� ���������� �� ����������
    application_type = ContentType.objects.get(app_label="metamodel", model="application")
    if request.META.get('PATH_INFO') != '/':
        try:
            application = application_type.get_object_for_this_type(alias=application_alias)
            _application_map[application_alias] = application
            return application
        except ObjectDoesNotExist:
            ip = request.META.get('HTTP_X_REAL_IP')
            if ip is not None:
                Attack.objects.create(ip=ip, url=request.META.get('PATH_INFO'), date_attack=datetime.datetime.now())
                transaction.commit()

    # ������� �������� ���������� �� ���������
    try:
        application = application_type.get_object_for_this_type(default=True)
        _application_map[application.alias] = application
        return application
    except ObjectDoesNotExist:
        raise Exception(u'���������� �� ��������� �� ����������')

    # if request.META.get('PATH_INFO') != '/':
    #     instance_list = Application.objects.filter(alias=application_alias)
    #     if len(instance_list):
    #         _application_map[application_alias] = instance_list[0]
    #         return instance_list[0], False
    #     else:
    #         Attack.objects.create(ip=request.META.get('HTTP_X_REAL_IP'), url=request.META.get('PATH_INFO'), date_attack=datetime.datetime.now())
    #         transaction.commit()

    # instance_list = Application.objects.filter(default=True)
    # if len(instance_list):
    #     _application_map[application_alias] = instance_list[0]
    #     return instance_list[0], True
    # else:
    #     raise Exception(u'���������� "%s" �� ����������' % application_alias)


def get_entity_instance(request, entity_alias=None, application_alias=None):
    if entity_alias is None and application_alias is None:
        raise Exception(u'������������ �������� ��� ������ ����������, �� ������ ������ �������')

    # ��������� ���������� ������ ��������
    application = get_application_instance(application_alias, request)
    instance_list = Entity.objects.filter(alias=entity_alias, site=application.site)
    if len(instance_list):
        entity = instance_list[0]
        return entity
    else:
        raise Exception(u'�������� "%s" �� ����������' % entity_alias)


def get_model(request, entity_alias, application_alias):
    # ��������� ������ ���������� ��������
    try:
        entity_type = ContentType.objects.get(app_label="metamodel", model=entity_alias)
        return entity_type.model_class()
    except ObjectDoesNotExist:
        pass

    # ��������� ������ ���������� ��������
    try:
        entity_type = ContentType.objects.get(app_label="dbtemplates", model=entity_alias)
        return entity_type.model_class()
    except ObjectDoesNotExist:
        pass

    try:
        entity_type = ContentType.objects.get(app_label="nature", model=entity_alias)
        return entity_type.model_class()
    except ObjectDoesNotExist:
        pass


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


def __unicode__(self):
    return '%s %s' % (self.last_name, self.first_name)


User.__unicode__ = __unicode__


class MetamodelAppConfig(AppConfig):
    name = 'metamodel'

    def ready(self):
        collect_entity()
        pass
