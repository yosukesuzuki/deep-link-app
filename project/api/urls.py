# -*- coding: utf-8 -*-
# api.urls

from kay.routing import (
    ViewGroup, Rule
)

view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='api.views.index'),
    )
]
