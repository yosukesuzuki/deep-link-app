# -*- coding: utf-8 -*-

from kay.ext.testutils.gae_test_base import GAETestBase

from core.models import ShortURL, ShortURLID, ShortURLUser


class PutShortURLTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_put_url(self):
        user = ShortURLUser(key_name="hoge")
        user.put()
        short_url = ShortURL(long_url="http://kay-template.appspot.com/", user_created=str(user.key()))
        log_entity_key_name = "hoge"
        log_entity_key_name += "e6988488afff91c2059ecda505f205d2c7ac701f5f8016e68b037c641523f7816169e0"
        log_entity_key_name += "dec370742f70ad49d3b520e7bc687da204c2bc3ef58184793f01fdfb28"
        self.assertEquals(log_entity_key_name, short_url.get_log_entity_key_name())
        code = short_url.check_exist_or_create()
        self.assertEquals(code, "1")


class ShortURLIDTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_code(self):
        short_url_id = ShortURLID(long_url="http://kay-template.appspot.com/")
        self.assertEquals(short_url_id.code(), None)
        short_url_id.put()
        self.assertEquals(short_url_id.code(), "1")
