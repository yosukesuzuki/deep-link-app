# -*- coding: utf-8 -*-
"""
api.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""
import re
from werkzeug.exceptions import BadRequest
from kay.utils import render_json_response
from core.models import validate_api_key, APIKey
from api.shorturls import URLShorten

URLSHORTEN_PATTERN = re.compile("[0-9a-zA-Z]+")

from functools import update_wrapper


def api_auth(func):
    def inner(request, *args, **kwargs):
        if request.user.is_anonymous():
            try:
                api_key = request.args['key']
            except BadRequest:
                return render_json_response({'message': 'bad request', 'status': 'error'}, status=400)
            if validate_api_key(api_key) is False:
                return render_json_response({'message': 'invalid key', 'status': 'error'}, status=403)
        return func(request, *args, **kwargs)

    update_wrapper(inner, func)
    return inner


@api_auth
def shorturl(request, path=None):
    if path is not None and URLSHORTEN_PATTERN.search(path) is False:
        return render_json_response({'message': 'bad request', 'status': 'error'}, status=400)
    user_created = str(request.user.key())
    if request.user.is_anonymous():
        api_key_entity = validate_api_key(request.args['key'])
        user_created = api_key_entity.user_created
    shorturls = URLShorten(method=request.method, user_created=user_created, values=request.values, path=path)
    shorturls.do()
    return render_json_response(shorturls.result, status=shorturls.code)


@api_auth
def apikey(request):
    query_results = APIKey.all().filter(u'user_created =', str(request.user.key())).order('-created_at').fetch(20)
    api_keys = [result.key().name() for result in query_results]
    return render_json_response({'api_keys': api_keys, 'status': 'success'}, status=200)
