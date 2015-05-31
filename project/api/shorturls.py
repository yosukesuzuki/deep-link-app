# -*- coding: utf-8 -*-

from core.models import ShortURL, ShortURLCreateLog


class URLShorten(object):
    PAR_PAGE = 50

    def __init__(self, method, user_created, values, path=None):
        """
        :param str method: REST Method
        :param core.models.ShortURLUser user: model of login user
        :param values:
        :param str path:
        """
        self.method = method
        self.user_created = user_created
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
                'firefox_url': entity.firefox_url, 'path': entity.key().name()}

    def get(self):
        query_results = ShortURL.all().filter(u'user_created =', self.user_created).order('-created_at').fetch(
            self.PAR_PAGE)
        short_urls = [self.model_to_dict(result) for result in query_results]
        self.result = {'short_urls': short_urls, 'status': 'success'}
        self.code = 200
        return

    def post(self):
        long_url = self.values['long_url']
        short_url = ShortURL(long_url=long_url, user_created=self.user_created)
        self.result = short_url.check_exist_or_create()
        self.code = self.result['code']
        return

    def put(self):
        if self.path is None:
            return
        entity = ShortURL.get_by_key_name(self.path)
        if entity is None:
            self.result = {'message': 'not found', 'status': 'error'}
            self.code = 404
            return
        if entity.user_created != self.user_created:
            self.result = {'message': 'bad request', 'status': 'error'}
            self.code = 400
            return
        for property in ['fallback_url', 'iphone_url', 'ipad_url', 'android_url', 'wp_url', 'firefox_url']:
            if property in self.values:
                setattr(entity, property, self.values[property])
        if 'custom_name' in self.values and self.values['custom_name'] != '':
            custom_name_result = entity.set_custom_name(self.values['custom_name'])
            if custom_name_result['code'] != 201:
                self.result = custom_name_result
                self.code = custom_name_result['code']
                return
            custom_name_entity = ShortURL.get_by_key_name(custom_name_result['path'])
            short_url = self.model_to_dict(custom_name_entity)
            short_url['status'] = 'success'
            self.result = short_url
            self.code = 201
            return
        entity.put()
        short_url = self.model_to_dict(entity)
        short_url['status'] = 'success'
        self.result = short_url
        self.code = 200
        return

    def delete(self):
        entity = ShortURL.get_by_key_name(self.path)
        if entity is None:
            self.result = {'message': 'not found', 'status': 'error'}
            self.code = 404
            return
        entity.delete()
        log_entity_key_name = entity.get_log_entity_key_name()
        short_url_create_log = ShortURLCreateLog.get_by_key_name(log_entity_key_name)
        short_urls = short_url_create_log.short_urls
        short_urls.remove(self.path)
        short_url_create_log.short_urls = short_urls
        short_url_create_log.put()
        self.result = {'message': 'no content', 'status': 'success'}
        self.code = 204
        return

    def do(self):
        if self.method == 'GET':
            self.get()
        elif self.method == 'POST':
            self.post()
        elif self.method == 'PUT' or self.method == 'PATCH':
            self.put()
        elif self.method == 'DELETE':
            self.delete()
