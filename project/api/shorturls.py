# -*- coding: utf-8 -*-

from core.models import ShortURL


class URLShorten(object):
    PAR_PAGE = 50

    def __init__(self, method, user, values, path=None):
        """
        :param str method: REST Method
        :param core.models.ShortURLUser user: model of login user
        :param values:
        :param str path:
        """
        self.method = method
        self.user = user
        self.values = values
        self.path = path
        self.result = {'message': 'bad request', 'status': 'error'}
        self.code = 400

    def model_to_dict(self, entity):
        """
        :param ShortURL entity: model of ShortURL
        """
        return {'long_url': entity.long_url, 'fallback_url': entity.fallback_url, 'iphone_url': entity.iphone_url,
                'ipad_url': entity.ipad_url, 'android_url': entity.android_url, 'wp_url': entity.wp_url,
                'firefox_url': entity.firefox_url}

    def do(self):
        if self.method == 'GET':
            query_results = ShortURL.all().filter(u'user_created', self.user.key()).order('-created_at').fetch(
                self.PAR_PAGE)
            short_urls = [self.model_to_dict(result) for result in query_results]
            self.result = {'shorturls': short_urls, 'status': 'success'}
            self.code = 200
            return
        if self.method == 'POST':
            long_url = self.values['url']
            short_url = ShortURL(long_url=long_url, user_created=str(self.user.key()))
            self.result = short_url.check_exist_or_create()
            self.code = self.result['code']
            return
        if self.method == 'PUT' or self.method == 'PATCH':
            if self.path is None:
                self.result = {'message': 'bad request', 'status': 'error'}
                self.code = 400
                return
            entity = ShortURL.get_by_key_name(self.path)
            for property in ['fallback_url', 'iphone_url', 'ipad_url', 'android_url', 'wp_url', 'firefox_url']:
                if property in self.values:
                    entity.fallback_url = self.values[property]
            short_url = self.model_to_dict(entity)
            short_url['status'] = 'success'
            self.result = short_url
            self.code = 200
            return
        if self.method == 'DELETE':
            return
