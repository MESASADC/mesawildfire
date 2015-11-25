#
# http://palewi.re/posts/2009/09/01/django-recipe-remove-newlines-text-block/
#
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
import settings
import re
import os
import logging

register = template.Library()


@register.filter
@stringfilter
def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))


@register.filter
@stringfilter
def reduce_spaces(text):
    """
    Removes extraneous spaces from a block of text.
    """
    return mark_safe(re.sub('\s+', ' ', text))


@register.simple_tag
def version_string():
    return afis_js_hash()

@register.simple_tag
def afis_js_hash():
    s = str(hash(open(os.path.join(settings.STATIC_ROOT, 'js', 'afis.js')).read()))
    logging.debug('afis.js hash = %s' % s)
    return s
