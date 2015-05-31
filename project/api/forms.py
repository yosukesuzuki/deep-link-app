# -*- coding: utf-8 -*-

from kay.utils.forms.modelform import ModelForm

from core.models import APIKey


class APIKeyForm(ModelForm):
    class Meta:
        model = APIKey
        exclude = ('user_created')
