# -*- coding: utf-8 -*-
# api.urls
import uuid

from kay.generics import crud
from kay.generics import login_required
from kay.routing import (
    ViewGroup, Rule
)

from core.models import APIKey
from api.forms import APIKeyForm


class APIKeyCRUDViewGroup(crud.CRUDViewGroup):
    model = APIKey
    form = APIKeyForm
    templates = {
        'list': 'api/general_list.html',
        'update': '_internal/general_update.html',
        'show': '_internal/general_show.html',
    }

    def get_query(self, request):
        return self.model.all().filter(u'user_created =', str(request.user.key())).order('-created_at')

    def get_additional_context_on_create(self, request, form):
        key_name = uuid.uuid4().hex
        user_created = str(request.user.key())
        return {'key_name': key_name, 'user_created': user_created}

    authorize = login_required


view_groups = [
    APIKeyCRUDViewGroup(),
    ViewGroup(
        Rule('/v1/apikeys', endpoint='apikeys', view='api.views.apikey'),
        Rule('/v1/shorturls', endpoint='shorturls', view='api.views.shorturl'),
        Rule('/v1/shorturls/<string:path>', endpoint='shorturls_with_path', view='api.views.shorturl'),
    )
]
