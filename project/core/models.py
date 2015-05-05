# -*- coding: utf-8 -*-
# core.models

from google.appengine.ext import db
from kay.auth.models import GoogleUser


class Article(db.Model):
    title = db.StringProperty()
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.title


class ShortURLUser(GoogleUser):
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)


class ShortURL(db.Model):
    long_url = db.StringProperty(verbose_name='long URL', required=True)
    fallback_url = db.StringProperty(verbose_name='Fallback URL')
    iphone_url = db.StringProperty(verbose_name='iPhone URL')
    ipad_url = db.StringProperty(verbose_name='iPad URL')
    android_url = db.StringProperty(verbose_name='Android URL')
    wp_url = db.StringProperty(verbose_name='WindowsPhone URL')
    firefox_url = db.StringProperty(verbose_name='FireFox URL')
    user_created = db.StringProperty(verbose_name='Key of ShortURLUser')
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)


class ShortURLRule(db.Model):
    long_url = db.StringProperty(verbose_name='long URL', required=True)
    fallback_url = db.StringProperty(verbose_name='Fallback URL')
    iphone_url = db.StringProperty(verbose_name='iPhone URL')
    ipad_url = db.StringProperty(verbose_name='iPad URL')
    android_url = db.StringProperty(verbose_name='Android URL')
    wp_url = db.StringProperty(verbose_name='WindowsPhone URL')
    firefox_url = db.StringProperty(verbose_name='FireFox URL')
    user_created = db.StringProperty(verbose_name='Key of ShortURLUser')
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
