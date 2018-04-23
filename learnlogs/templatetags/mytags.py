from django import template
from learnlogs.models import Topic
from learnlogs.i18n.module import Module
from django.conf import settings
from django.utils import translation

tranc = Module()
register = template.Library()


@register.simple_tag()
def get_right_nav(owner_name):
    return Topic.objects.filter(owner=owner_name).order_by('-date_add')


@register.simple_tag()
def trans(text, session):
    default = translation.get_language()
    if default in settings.LANGUAGE_LIST.keys():
        luagange = session.get('language', default)
    else:
        luagange = session.get('language', 'en-us')

    if luagange == 'en-us':
        return text
    return tranc.trans(text=text, luagange=luagange)
    # return session


@register.simple_tag()
def get_language_list():
    language_list = settings.LANGUAGE_LIST
    return language_list
