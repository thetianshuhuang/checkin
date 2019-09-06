"""
Django settings
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

# -- Config Imports -----------------------------------------------------------

import os
import sys
import json


# -- Path Setup ---------------------------------------------------------------

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# -- Security -----------------------------------------------------------------

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# The secret key is stored in ``key.json`` and should be generated with
# ``python manage.py makekey``.
with open(os.path.join(BASE_DIR, "key.json")) as file:
    keys = json.load(file)
    SECRET_KEY = keys["key"]

# Running in apache
if 'django.core.wsgi' in sys.modules:
    DEBUG = False
    DEV_MODE = False
    MIN = True
    HTML_MINIFY = True

# Running with ``runserver``
else:
    DEBUG = True
    DEV_MODE = True
    MIN = False
    HTML_MINIFY = True

# Allowed hosts (must add server IP to list)
ALLOWED_HOSTS = [
    # Localhost and localhost accessories
    'localhost',
    '127.0.0.1',
]


# -- Applications -------------------------------------------------------------

INSTALLED_APPS = [
    # API app
    'api.apps.ApiConfig',
    # Main app
    'main.apps.MainConfig',
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# -- Middleware ---------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# HTML Minifier
#
# Serve all HTML files with newlines and indentation stripped to reduce
# filesize
if HTML_MINIFY:
    MIDDLEWARE += [
        'htmlmin.middleware.HtmlMinifyMiddleware',
        'htmlmin.middleware.MarkRequestMiddleware',
    ]


# -- Login Exempt URLs --------------------------------------------------------

# Root URL config file (do not change this)
ROOT_URLCONF = 'checkin.urls'


# -- Templates ----------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates/")],
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


# -- WSGI definition (for Apache) ---------------------------------------------

# WSGI_APPLICATION = ''


# -- Databases ----------------------------------------------------------------

# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
#
# Different database settings are used for Windows and Linux. Windows uses
# Windows Active Directory authentication, while Linux requires a local SQL
# server login. Both use the ODBC Driver 13 for SQL server and PyODBC.
#
# Database modes switch automatically using os.name.

DATABASES = {
    # Default: server settings
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# -- Password validation ------------------------------------------------------

# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.NumericPasswordValidator'),
    },
]

# -- Internationalization -----------------------------------------------------
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# -- Static files -------------------------------------------------------------

# (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
