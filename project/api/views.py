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
from kay.auth.decorators import login_required
from kay.utils import render_json_response
from api.shorturls import URLShorten

URLSHORTEN_PATTERN = re.compile("[0-9a-zA-Z]+")


@login_required
def shorturl(request, path=None):
    if path is not None and URLSHORTEN_PATTERN.search(path) is False:
        return render_json_response({'message': 'bad request', 'status': 'error'}, status=400)
    shorturls = URLShorten(method=request.method, user=request.user, values=request.values, path=path)
    shorturls.do()
    return render_json_response(shorturls.result, status=shorturls.code)
