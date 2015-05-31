# -*- coding: utf-8 -*-
# shorten.urls

from kay.routing import (
    ViewGroup, Rule
)

view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='shorten.views.index'),
    )
]
