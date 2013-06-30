from django.utils.timezone import now
from django.conf import settings


VARIABLES = {
    'DEBUG': getattr(settings, 'DEBUG', False),
    'DEBUG_STYLES': getattr(settings, 'DEBUG_STYLES', False),
    'DEBUG_SCRIPTS': getattr(settings, 'DEBUG_SCRIPTS', False),
    'STATIC_URL': getattr(settings, 'STATIC_URL'),
    'MEDIA_URL': getattr(settings, 'MEDIA_URL'),
}


def settings_variables(request):
    return VARIABLES
