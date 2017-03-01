# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""
from .common import *  # noqa

import socket
from celery.schedules import crontab
from importlib.machinery import SourceFileLoader

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='nl31lg67==&snr#@f8)9de#=mgb2+005-1zi00f)g89&-6lw3)')

SETTING_TYPE = 'Local'
# Mail settings
# ------------------------------------------------------------------------------

# EMAIL_PORT = 1025
#
# EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': env('PSQL_DB_NAME', default='db'),
        'USER': env('PSQL_DB_USER', default='dbuser'),
        'PASSWORD': env('PSQL_DB_PASSWD', default='dbpassword1234'),
        'HOST': 'remotedb',
        'PORT': '5432',
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

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1]+"1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

GRAPH_MODELS = {
  'all_applications': False,
  'group_models': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y/%m/%d %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR.path('app_debug.log')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        },
        'celery_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR.path('celery.log')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        },
        'error_file': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR.path('app_error.log')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'capricorn': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['error_file'],
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

# WEBPACK, In favor for webpack dev server
# ------------------------------------------------------------------------------
# Webpack Local Stats file
STATS_FILE = ROOT_DIR('webpack-stats.json')
WDS_ON = True
# Webpack config
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'capricorn/static/dist/', # must end with slash
        'STATS_FILE': STATS_FILE,
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}
