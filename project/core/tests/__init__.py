# -*- coding: utf-8 -*-

from google.appengine.api import memcache
from kay.ext.testutils.gae_test_base import GAETestBase

from core.models import ShortURL, ShortURLID, ShortURLUser, create_api_key, validate_api_key, abort_api_key


class PutShortURLTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_logging(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = ShortURL(long_url='http://kay-template.appspot.com/', user_created=str(user.key()))
        log_entity_key_name = 'foobar'
        log_entity_key_name += 'e6988488afff91c2059ecda505f205d2c7ac701f5f8016e68b037c641523f7816169e0'
        log_entity_key_name += 'dec370742f70ad49d3b520e7bc687da204c2bc3ef58184793f01fdfb28'
        self.assertEquals(log_entity_key_name, short_url.get_log_entity_key_name())

    def test_put(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = ShortURL(long_url='http://kay-template.appspot.com/', user_created=str(user.key()))
        result = short_url.check_exist_or_create()
        self.assertEquals(result['code'], 201)
        self.assertEquals(result['path'], '1')

    def test_custom_name(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        short_url = ShortURL(long_url='http://kay-template.appspot.com/', user_created=str(user.key()))
        result = short_url.check_exist_or_create()
        custom_name_entity = ShortURL.get_by_key_name(result['path'])
        custom_result = custom_name_entity.set_custom_name('foobar')
        self.assertEquals(custom_result['code'], 201)
        test_entity = ShortURL.get_by_key_name('foobar')
        self.assertEquals(test_entity.long_url, 'http://kay-template.appspot.com/')
        another_short_url = ShortURL(long_url='http://kay-template.appspot.com/foobar', user_created=str(user.key()))
        another_result = another_short_url.check_exist_or_create()
        another_custom_name_entity = ShortURL.get_by_key_name(another_result['path'])
        another_custom_result = another_custom_name_entity.set_custom_name('foobar')
        self.assertEquals(another_custom_result['code'], 409)
        self.assertEquals(another_custom_result['url'], 'http://kay-template.appspot.com/')


class ShortURLIDTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_code(self):
        short_url_id = ShortURLID(long_url='http://kay-template.appspot.com/')
        self.assertEquals(short_url_id.path, None)
        short_url_id.put()
        self.assertEquals(short_url_id.path, '1')


class APIKeyTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_create(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        api_key = create_api_key(user)
        memcache_key = 'api-key-%s' % api_key
        memcached_data = memcache.get(memcache_key)
        self.assertEquals(api_key, memcached_data)

    def test_validate(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        api_key = create_api_key(user)
        self.assertEquals(validate_api_key(api_key), True)
        memcache.delete('api-key-%s' % api_key)
        self.assertEquals(validate_api_key(api_key), True)
        memcache_result = memcache.get('api-key-%s' % api_key)
        self.assertEquals(memcache_result, api_key)

    def test_abort(self):
        user = ShortURLUser(key_name='foobar')
        user.put()
        api_key = create_api_key(user)
        self.assertEquals(validate_api_key(api_key), True)
        abort_api_key(api_key)
        self.assertEquals(validate_api_key(api_key), False)
