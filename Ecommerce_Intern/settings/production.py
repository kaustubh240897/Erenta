"""
Django settings for Ecommerce_Intern project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'az07)e=s3ttmo+5l)!)1nw7!q=kd9sbah^&9qjj-(&y93q)167'



ALLOWED_HOSTS = ['*']

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'kaustubh.dwi@gmail.com' # sendgrid
# EMAIL_HOST_PASSWORD =  os.environ.get('EMAIL_HOST_PASSWORD', 'It12345cse')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'Erenta <kaustubh.dwi@gmail.com>'
# BASE_URL = 'https://rent-now.herokuapp.com'

# MANAGERS = (
#     ('kd12345', "kaustubh.dwi@gmail.com"),
# )
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Erenta <erentajapan@gmail.com>'
BASE_URL = 'https://rent-now.herokuapp.com'

MANAGERS = (
    ('Kaustubh Dwivedi', "erentajapan@gmail.com"),
)



ADMINS = MANAGERS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     # third party
    'storages',

    'multiselectfield',
    'products',
    'search',
    'tags',
    'carts',
    'orders',
    'accounts',
    'addresses',
    'otherdetails',
    'analytics',
    'category',
    'billing',
    'crispy_forms',
    'notification',
    
]

AUTH_USER_MODEL='accounts.User' #changes the built in user model to ours
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'

FORCE_SESSION_TO_ONE =  False
FORCE_INACTIVE_USER_ENDSESSION = False

STRIPE_SECRET_KEY = "sk_test_HOMstuXI7oONEi2EkZO0diAb0044RmXYPQ"
STRIPE_PUB_KEY = 'pk_test_01sCwPKCtrJau8EiJu30FEXE00xcNv24Mm'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGOUT_REDIRECT_URL ='/'
ROOT_URLCONF = 'Ecommerce_Intern.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Ecommerce_Intern.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_project"),
]
STATIC_ROOT=os.path.join(os.path.dirname(BASE_DIR), "static_files", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(os.path.dirname(BASE_DIR), "static_files", "media_root")

from Ecommerce_Intern.aws.conf import *

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True