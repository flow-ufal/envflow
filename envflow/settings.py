"""
Django settings for envflow project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url

from . import settings_odm2admin

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

EXPORTDB = False

APP_NAME = 'odm2admin'
VERBOSE_NAME = 'ODM2 Admin'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#70mome-%fdh2f*1kxud(8b$4zkyoplzzh!9)59szfc+!a4xwm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

BASE_URL = ''
CUSTOM_TEMPLATE_PATH = '/{}{}/'.format(BASE_URL, APP_NAME)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    #myapps
    'iha',
    'core',
    'user',

    #app install
    'widget_tweaks',
    'leaflet',

    #ODM2Admin
    'odm2admin',
    'ajax_select',
    'jquery',
    'djangocms_admin_style',
    'import_export',
    'social_django',
    'admin_shortcuts',
    'daterange_filter',
    'captcha',
    'fixture_magic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'envflow.urls'

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

WSGI_APPLICATION = 'envflow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'odm2',
        'USER': 'clebsonpy',
        'PASSWORD': '89635241',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=admin,odm2,odm2extra'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LEAFLET_CONFIG = {
    #'SPATIAL_EXTENT': (-30, -7, -39, -9),
    'DEFAULT_CENTER': (-9.664004, -35.739083),
    'DEFAULT_ZOOM': 8,
    'MIN_ZOOM': 2,
    'MAX_ZOOM': 18,
    }

#auth
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'core:index'
LOGOUT_URL = 'logout'
AUTH_USER_MODEL = 'user.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'user.backends.ModelBackend',
)
ACCOUNT_SIGNUP_FORM_CLASS = 'user.forms.UserMultiForm'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
