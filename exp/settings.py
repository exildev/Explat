"""
Django settings for exp project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7jndr5evl9qq8hq*7$t0t4-qh5(1_y^(q!xxtaj55v@$!)+5nk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'supra',
    'usuario',
    'motorizado',
    'exp',
    'pedido',
    'braces',
    'easy_pdf',
    'reporte',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL=True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

ROOT_URLCONF = 'exp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'exp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # Or path to database file if using sqlite3.
        'NAME': 'express',
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': '85412369**$%%&*(/%$#qazxswEDC',
        'HOST': '127.0.0.1',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'PORT': '5432',  # Set to empty string for default.
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = (
    # PROJECT_ROOT, 'static'
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.normpath(os.path.join(os.path.dirname(__file__), '../static/')),
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

HOST_NODE = 'ec2-54-175-121-21.compute-1.amazonaws.com'

PORT_NODE = 4000
