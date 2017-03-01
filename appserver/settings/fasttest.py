# -*- coding: utf-8 -*-
'''
Fast Test settings

- Used to run tests fast on the continuous integration server and locally
'''

from .test import * # noqa

DATABASES['default'] = {
    'ENGINE' : 'django.db.backends.sqlite3',
    'NAME': 'testdb'
}
