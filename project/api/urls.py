# -*- coding: utf-8 -*-
# api.urls

from kay.routing import (
    ViewGroup, Rule
)

view_groups = [
    ViewGroup(
        Rule('/v1/shorturls', endpoint='shorturls', view='api.views.shorturl'),
        Rule('/v1/shorturls/<string:path>', endpoint='shorturls_with_path', view='api.views.shorturl'),
    )
]
