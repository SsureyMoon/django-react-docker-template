# -*- coding: utf-8 -*-
'''
Test settings

- Used to run tests fast on the continuous integration server and locally
'''

from .common import * # noqa

# Update installed app for jenkins runner
# INSTALLED_APPS += ('django_jenkins', )
# JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
#                  'django_jenkins.tasks.run_pep8',
#                  'django_jenkins.tasks.run_pyflakes',)

PROJECT_APPS = [appname for appname in LOCAL_APPS]

# DEBUG
# ------------------------------------------------------------------------------
# Turn debug off so tests run faster
DEBUG = False
CI_SERVER = env.bool('CI_SERVER', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = False

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='CHANGEME!!!')

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# In-memory email backend stores messages in django.core.mail.outbox
# for unit testing purposes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# CACHING
# ------------------------------------------------------------------------------
# Speed advantages of in-memory caching without having to run Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

DATABASES = {
        'default': {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            'NAME': 'testdb',
            'USER': 'devuser',
            'PASSWORD': 'devpassword',
            'HOST': 'dbserver',
            'PORT': '',
        }
    }

if CI_SERVER:
    DATABASES = {
        'default': {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            'NAME': 'testdb',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# PASSWORD HASHING
# ------------------------------------------------------------------------------
# Use fast password hasher so tests run faster
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

AWS_ACCESS_KEY_ID = 'aws-access-key-test'
AWS_SECRET_ACCESS_KEY = 'aws-secret-key-test'
AWS_STORAGE_BUCKET_NAME = 'appserver-test'

AWS_REGION = 'ap-northeast-1' # Tokyo
# AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3-{}.amazonaws.com'.format(AWS_REGION)
os.environ['S3_USE_SIGV4'] = 'True'

SQS_AWS_REGION = 'ap-northeast-2' # Seoul
SQS_NAME = 'sqs-test'

AWS_DEFAULT_ACL = 'private'
AWS_QUERYSTRING_AUTH = True
MEDIA_URL = 'https://%s.s3.amazonaws.com/assets/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s.s3.amazonaws.com/assets/static/' % AWS_STORAGE_BUCKET_NAME

# TEMPLATE LOADERS
# ------------------------------------------------------------------------------
# Keep templates in memory so tests run faster
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

