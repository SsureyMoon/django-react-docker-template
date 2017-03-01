# -*- coding: utf-8 -*-
"""
Staging Server settings

- Run in None-Debug mode
- Use console backend for emails
- No Django Debug Toolbar
- Add django-extensions as app
- Set Remote DB REDIS Server Info.
"""
from .common import *  # noqa

from celery.schedules import crontab
from importlib.machinery import SourceFileLoader

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY')

SETTING_TYPE = 'Staging'

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': env('PSQL_DB_NAME'),
        'USER': env('PSQL_DB_USER'),
        'PASSWORD': env('PSQL_DB_PASSWD'),
        'HOST': env('PSQL_HOST'),
        'PORT': env('PSQL_PORT'),
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# STATIC_ROOT = str(SRC_DIR('static'))
# Your local stuff: Below this line define 3rd party library settings
# this username and password are for test only

DEFAULT_FILE_STORAGE = 'core.storages.MediaRootS3BotoStorage' #'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'core.storages.StaticRootS3BotoStorage'

AWS_STORAGE_BUCKET_NAME = 'capricorn-staging'

AWS_REGION = 'ap-northeast-2' # Seoul
# AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3-{}.amazonaws.com'.format(AWS_REGION)
AWS_SECRET_BUCKET = 'capricorn-credentials-staging'

AWS_SECRET_BUCKET_REGION = 'ap-northeast-2' # Seoul
AWS_SECRET_BUCKET_QUERYSTRING_AUTH = True
AWS_SECRET_BUCKET_S3_HOST = 's3.{}.amazonaws.com'.format(AWS_SECRET_BUCKET_REGION)
os.environ['S3_USE_SIGV4'] = 'True'

SQS_AWS_REGION = 'ap-northeast-2' # Seoul
SQS_NAME = env('SQS_NAME')

AWS_DEFAULT_ACL = 'private'
AWS_QUERYSTRING_AUTH = True
MEDIA_URL = 'https://%s.s3.amazonaws.com/assets/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s.s3.amazonaws.com/assets/static/' % AWS_STORAGE_BUCKET_NAME

del STATIC_ROOT
del STATICFILES_DIRS
# STATIC_ROOT = str(SRC_DIR('static'))
STATICFILES_DIRS = (str(STATIC_DIR('dist')),)
del STATICFILES_FINDERS

# We use AWS role allocated to each instance. so following properties are not necessary:
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR.path('app_debug.log')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        },
        'celery_file': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR.path('celery.log')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['require_debug_false'],
            'filename': str(LOG_DIR.path('app_error.log')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'app': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'capricorn': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'releases.tasks': {
            'handlers': ['celery_file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

ALLOWED_HOSTS = ['capricorn-staging.ap-northeast-2.elasticbeanstalk.com', 'localhost']
