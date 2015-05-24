# -*- coding: utf-8 -*-
from kay.ext.testutils.gae_test_base import GAETestBase

from api.shorturls import URLShorten
from core.models import ShortURL, ShortURLUser


class URLShortenTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_get(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = ShortURL(long_url='http://appu.pw/', user_created=str(user.key()))
        short_url.check_exist_or_create()
        short_url2 = ShortURL(long_url='https://console-dot-appupw.appspot.com/', user_created=str(user.key()))
        short_url2.check_exist_or_create()
        shorturls = URLShorten(method='GET', user_created=str(user.key()), values={})
        shorturls.do()
        result = shorturls.result
        self.assertEquals(result['short_urls'][0]['long_url'], 'https://console-dot-appupw.appspot.com/')

    def test_post(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = URLShorten(method='POST', user_created=str(user.key()),
                               values={'long_url': 'https://console-dot-appupw.appspot.com/'})
        short_url.do()
        self.assertEquals(short_url.result['path'], '1')
        short_url2 = URLShorten(method='POST', user_created=str(user.key()),
                                values={'long_url': 'https://console-dot-appupw.appspot.com/'})
        short_url2.do()
        self.assertEquals(short_url2.result['code'], 409)

    def test_put(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = URLShorten(method='POST', user_created=str(user.key()),
                               values={'long_url': 'https://console-dot-appupw.appspot.com/'})
        short_url.do()
        short_url2 = URLShorten(method='PATCH', user_created=str(user.key()),
                                values={'iphone_url': 'iphoneschema://foobar'},
                                path=short_url.result['path'])
        short_url2.do()
        self.assertEquals(short_url2.result['iphone_url'], 'iphoneschema://foobar')
        short_url3 = ShortURL.get_by_key_name(short_url.result['path'])
        self.assertEquals(short_url3.iphone_url, 'iphoneschema://foobar')

    def test_delete(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = URLShorten(method='POST', user_created=str(user.key()),
                               values={'long_url': 'https://console-dot-appupw.appspot.com/'})
        short_url.do()
        short_url2 = URLShorten(method='DELETE', user_created=str(user.key()), values={}, path=short_url.result['path'])
        short_url2.do()
        self.assertEquals(short_url2.code, 204)
        check_entity = ShortURL.get_by_key_name(short_url.result['path'])
        self.assertEquals(check_entity, None)
