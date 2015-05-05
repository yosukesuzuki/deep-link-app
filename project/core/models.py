# -*- coding: utf-8 -*-
# core.models

from google.appengine.ext import db

# Create your models here.


class Article(db.Model):
    title = db.StringProperty()
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.title

class ShortURL(db.Model):
    long_url = db.StringProperty(verbose_name='long URL', required=True)
    fallback_url = db.StringProperty(verbose_name='Fallback URL')
    ipad_url = db.StringProperty(verbose_name='iPad URL')
    android_url = db.StringProperty(verbose_name='Android URL')
    wp_url = db.StringProperty(verbose_name='WindowsPhone URL')
    firefox_url = db.StringProperty(verbose_name='FireFox URL')
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)


