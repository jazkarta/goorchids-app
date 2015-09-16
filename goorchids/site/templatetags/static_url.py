import re
from django.template import base as template
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()
STATIC_RE = re.compile(r'(\{\{\s*STATIC_URL\s*\}\})|(/static/)')


@register.filter
@stringfilter
def static_url(value):
    """Searches for {{ STATIC_URL }} or /static/ and replaces it with the
       STATIC_URL from settings.py"""
    value = STATIC_RE.sub(settings.STATIC_URL, value)
    return value
static_url.is_safe = True
