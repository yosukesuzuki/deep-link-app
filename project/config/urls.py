# -*- coding: utf-8 -*-
# config.urls

from kay.routing import (
    ViewGroup, Rule
)

view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='config.views.index'),
    )
]
