from os.path import exists
from stock.settings.base import DEV_TMP_DIR, DATABASES, CACHES, INSTALLED_APPS, MIDDLEWARE_CLASSES, LOGGING

# check tmp directory exists or create
if not exists(DEV_TMP_DIR):
    from os import makedirs
    makedirs(DEV_TMP_DIR)

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STYLES = True
DEBUG_SCRIPTS = True
DEBUG_TOOLBAR = False

DISABLE_ABSOLUTE_URI_TAG = True  # if not set base page urls will use absolute urls
SESSION_COOKIE_DOMAIN = ''

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES.update({
    'pgsql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stock',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
    },
})

CACHES.update({
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
})

LOGGING['root']['handlers'] = ['console']
#LOGGING.setdefault('loggers', {})['django.db.backends'] = {'level': 'DEBUG', 'handers': ['console'], }

# For development without ElasticSearch, you can uncomment following lines to avoid some errors
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#    },
#}

if DEBUG_TOOLBAR:
    import cache_toolbar.panels.redis
    INSTALLED_APPS += (
        'debug_toolbar',
        'cache_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': False,
        'INTERCEPT_REDIRECTS': False,
    }

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
        'cache_toolbar.panels.BasePanel',
    )

    INTERNAL_IPS = ('127.0.0.1',)
