"""
Django settings for express project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'x3k(&lowa@ty*)i1u!boear6k3%l-6dw*$wm=^=xp)zvfvclf8'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'supra',
    'supra.auths.oauth',
    'usuario',
    'motorizado',
    'exp',
    'pedido',
    'easy_pdf',
    'reporte',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # Or path to database file if using sqlite3.
        'NAME': 'exp',
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': 'Exile*74522547',
        'HOST': '104.236.33.228',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}


ROOT_URLCONF = 'exp.urls'

WSGI_APPLICATION = 'exp.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # PROJECT_ROOT, 'static'
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.normpath(os.path.join(os.path.dirname(__file__), '../static/')),
)


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Express Del Norte',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    'MENU': (
        {'app': 'domicilios', 'label': 'Clientes',
            'icon': 'icon-user', 'models': ('cliente', 'empresa',)},
        {'app': 'domicilios', 'label': 'Empleados',
            'icon': 'icon-briefcase', 'models': ('empleado',)},
        {'app': 'domicilios', 'label': 'Motorizados', 'icon': 'icon-road',
            'models': ('motorizado', 'moto', 'soat', 'tecno',)},
        {'app': 'domicilios', 'label': 'Pedidos',
            'icon': 'icon-shopping-cart', 'models': ('pedido',)},
        {'app': 'domicilios', 'label': 'Items',
            'icon': 'icon-shopping-cart', 'models': ('items',)},
        {'app': 'domicilios', 'label': 'Tiempo',
            'icon': 'icon-shopping-cart', 'models': ('tiempo',)},
    ),

    # misc
    'LIST_PER_PAGE': 15
}

TEMPLATE_DIRS = (
    os.path.join('templates'),
)

LOGIN_URL = 'usuario:user-login'

LOGIN_REDIRECT_URL = 'usuario:index_general'

"""
try:
    from .local_settings import *
except ImportError:
    pass

# Production database, smtp, roots etc..

try:
    from .production_settings import *
except ImportError:
    pass
"""
