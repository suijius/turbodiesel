# coding=cp1251
# Django settings for TurboDiesel project.


import os.path

# import djcelery

# djcelery.setup_loader()

ROOT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('SuijiuS', 'suijius@gmail.com'),
)


MANAGERS = ADMINS

PROFILE_LOG_BASE = os.curdir + "/log"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'shop',  # Or path to database file if using sqlite3.
        'USER': 'td',  # Not used with sqlite3.
        'PASSWORD': 'td',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
    },
    #    'history': {
    #        'ENGINE': 'django.db.backends.mysql',
    #        'NAME': 'td_history', # Or path to database file if using sqlite3.
    #        'USER': 'td', # Not used with sqlite3.
    #        'PASSWORD': 'td', # Not used with sqlite3.
    #        'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
    #        'PORT': '3306', # Set to empty string for default. Not used with sqlite3.
    #    },
    #    'delivery': {
    #        'ENGINE': 'django.db.backends.mysql',
    #        'NAME': 'delivery', # Or path to database file if using sqlite3.
    #        'USER': 'td', # Not used with sqlite3.
    #        'PASSWORD': 'td', # Not used with sqlite3.
    #        'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
    #        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    #    },
    'metadata': {
        'ENGINE': 'django.db.backends.mysql',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'information_schema',  # Or path to database file if using sqlite3.
        'USER': 'td',  # Not used with sqlite3.
        'PASSWORD': 'td',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
    },


}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MEDIA_ROOT = os.path.join(ROOT_PATH, 'media').replace('\\', '/') + '/'
MEDIA_URL = 'media/'

STATIC_ROOT = ''
STATIC_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = '9^jy@&f(#@yw#mj%_yzw$izbhkp%+m*te$o(!9qf5ji=@y#qlm'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'dbtemplates.loader.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'reversion.middleware.RevisionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',

    # required by django-admin-tools
    'django.core.context_processors.request',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.CookieStorage'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates/').replace('\\', '/'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'metamodel',
    'nature',
    # 'mptt',
    #    'djcelery',
    'dbtemplates',
    #    'djkombu',
    #'lettuce.django',
    #'reversion'
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

#LDAP_DOMAIN = ''
#LDAP_SERVER = 'ldaps://%s' % LDAP_DOMAIN

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

APPEND_SLASH = True

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#        'LOCATION': 'unique-snowflake'
#    }
#}

#CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
#BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
CELERY_RESULT_BACKEND = "amqp"
BROKER_HOST = "schepurnov"
BROKER_PORT = 5672
BROKER_USER = "turbodiesel"
BROKER_PASSWORD = "turbodiesel"
BROKER_VHOST = "schepurnov"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

FROM_MAIL = 'suijius@gmail.com'

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler'
#        },
#        'logfile': {
#            'level': 'DEBUG',
#            'class': 'logging.handlers.WatchedFileHandler',
#            'filename': '/usr/local/lib/TurboDiesel/media/turbodiesel/images/logfile.log',
#            'formatter': 'simple'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins', 'logfile'],
#            'level': 'DEBUG',
#            'propagate': True,
#            },
#        },
#    'formatters': {
#        'verbose': {
#            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#        },
#        'simple': {
#            'format': '%(asctime)s [%(levelname)s] [%(module)s]: %(message)s'
#        },
#        },
#    }


INTERNAL_IPS = ('127.0.0.1',)

AUTH_PROFILE_MODULE = "turbodiesel.UserProfile"

DBTEMPLATES_USE_CODEMIRROR = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

EXTENSIONS = [
    {'Name': u'Изображения', 'Image': 'turbodiesel/images/admin/image.png', 'TableName': 'ext_image', 'ClassName': 'ExtImage', 'Type': 1},
    {'Name': u'Кодовые вставки', 'Image': 'turbodiesel/images/admin/code.png', 'TableName': 'ext_code', 'ClassName': 'ExtCode', 'Type': 1},
    {'Name': u'Фильтры', 'Image': 'turbodiesel/images/admin/filter.png', 'TableName': 'ext_filter', 'ClassName': 'ExtFilter', 'Type': 1},
    {'Name': u'Шаблоны', 'Image': 'turbodiesel/images/admin/template.png', 'TableName': 'ext_template', 'ClassName': 'dbTemplates', 'Type': 1},
    {'Name': u'Пользователи', 'Image': 'turbodiesel/images/admin/user.png', 'TableName': 'ext_user', 'ClassName': 'User', 'Type': 1},
    {'Name': u'Рабочие потоки', 'Image': 'turbodiesel/images/admin/workflow.png', 'TableName': 'ext_workflow', 'ClassName': 'ExtWorkflow', 'Type': 1},
    {'Name': u'Статусы', 'Image': 'turbodiesel/images/admin/workflow.png', 'TableName': 'ext_status', 'ClassName': 'ExtStatus', 'Type': 1},
    {'Name': u'Переходы', 'Image': 'turbodiesel/images/admin/workflow.png', 'TableName': 'ext_edge', 'ClassName': 'ExtEdge', 'Type': 1},
]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'django.suijius@gmail.com'
EMAIL_HOST_PASSWORD = 'irdecntyu'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = 'django.suijius@gmail.com'
SEND_BROKEN_LINK_EMAILS = False

SESSION_SAVE_EVERY_REQUEST = True


