"""
Django settings for donation_tracker project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load project-specific variables from the root .env file
load_dotenv(dotenv_path=BASE_DIR / '.env', verbose=True)

# Store the secret key in the environment for security
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mathfilters',
    'project.apps.tracker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.common.context.environment',
                'project.apps.tracker.context.statistics',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.donation_tracker'

LOGIN_REDIRECT_URL = '/'
LOGGED_IN_HOME = '/'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Read the database configuration from the environment, with defaults
DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.environ.get('DB_DBNAME', 'donation_tracker'),
#        'USER': os.environ.get('DB_USERNAME', 'donation_tracker_webserver'),
#        'PASSWORD': os.environ['DB_PASSWORD'],
#        'HOST': os.environ.get('DB_HOSTNAME', 'localhost'),
#        'PORT': os.environ.get('DB_PORT', '5432'),
#    }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Globalization (i18n/l10n)
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# In general, accept ISO and UK date/time formats for my own sanity

DATE_FORMAT = 'j F Y' # 1 April 2021
# Accept 2021-04-01, 01/04/2021, 01/04/21
DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']

DATETIME_FORMAT = 'f A, j F Y' # 1:30 PM, 4 March 2021
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%d/%m/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M',
    '%d/%m/%y %H:%M:%S',
    '%d/%m/%y %H:%M',
]

FIRST_DAY_OF_WEEK = 1

MONTH_DAY_FORMAT = 'j F' # 1 January

SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'f A, d/m/Y'

TIME_FORMAT = 'f A'
TIME_INPUT_FORMATS = [
    '%H:%M:%S',
    '%H:%M',
]

TIME_ZONE = 'UTC'

# No i18n or l10n provided yet. TODO, I guess?

USE_I18N = False
USE_L10N = False

USE_TZ = False

YEAR_MONTH_FORMAT = 'F Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
