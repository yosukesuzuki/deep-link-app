# -*- coding: utf-8 -*-

"""
Kay test settings.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEBUG = False
ROOT_URL_MODULE = 'kay.tests.globalurls'

MIDDLEWARE_CLASSES = (
  'kay.sessions.middleware.SessionMiddleware',
)

COOKIE_AGE = 120 # 2 min
COOKIE_NAME = 'KAY_TEST_SESSION'
COOKIE_SECURE = True

INSTALLED_APPS = (
  'kay.tests',
)

APP_MOUNT_POINTS = {
  'kay.tests': '/',
}

