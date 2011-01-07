import os
import sys

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)

sys.path.insert(0, rel('..','lib'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1')

ADMINS = (
            ('admin', 'admin@some.mail'),
         )
MANAGERS = ADMINS

DEFAULT_CHARSET = 'UTF-8'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('database.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Kiev'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/')

MEDIA_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'secret_key'

AUTHENTICATION_BACKENDS = (
    'app.account.backends.CustomUserModelBackend',
)

CUSTOM_USER_MODEL = 'account.User'

LOGIN_URL = '/login/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    #"django.core.context_processors.debug",
    "django.core.context_processors.media"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'app.main.middleware.CurrentTestMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "app.main.context_processors.current_test",                               
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'app.main',
    'app.account',
    'registration',
	'django_extensions',
    'pagination'
)

LOGIN_REDIRECT_URL='/'

#Custom settings
ACCOUNT_ACTIVATION_DAYS = 3

try:
    from settings_local import *
except ImportError:
    pass