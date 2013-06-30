from os.path import join, dirname, pardir, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), pardir))
DEV_TMP_DIR = join(PROJECT_ROOT, pardir, '.devtmp')

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STYLES = True
DEBUG_SCRIPTS = True
DEBUG_TOOLBAR = False
DEBUG_THUMBNAIL = True

ADMINS = ()
MANAGERS = ADMINS

# new Django security settings
ALLOWED_HOSTS = []

# NOTE: development settings, overwrite it in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DEV_TMP_DIR, 'devel.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# NOTE: development settings, overwrite it in production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Prague'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'cs'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Media and static settings, development
MEDIA_ROOT = join(DEV_TMP_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = join(DEV_TMP_DIR, 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'project_static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# NOTE: development settings, use real secret key in your production
if DEBUG:
    SECRET_KEY = '0123456789' * 5

# NOTE: this is development, define cached loaders in production settings
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'stock.urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

# TODO: what we really need?
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',  # fashionpolice tags
    # 'django.core.context_processors.debug',

    # static/media url, debug variables etc.
    'stock.context_processors.settings_variables',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'grappelli',  # before admin
    'django.contrib.admin',

    'south',
    'raven.contrib.django',
    #'taggit',

    'stock',


    'sorl.thumbnail',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_COOKIE_DOMAIN = ''

# search haystack / ES configuration
# haystack search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'sm_search_common.backend.elasticsearch.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'stock',
    },
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15
HAYSTACK_ELASTICSEARCH_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "tokenizer": "lowercase",
                    "filter": ["asciifolding", "standard", "stop", "cz_stemmer"],
                    "char_filter": ["html_strip"],
                    "alias": ["snowball"]
                },
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["haystack_ngram"]
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["haystack_edgengram"]
                }
            },
            "tokenizer": {
                "haystack_ngram_tokenizer": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15
                },
                "haystack_edgengram_tokenizer": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15,
                    "side": "front"
                }
            },
            "filter": {
                "stop": {
                    "type": "stop",
                    "stopwords_path": "stopwords.txt"
                },
                "cz_stemmer": {
                    "type": "stemmer",
                    "name": "czech"
                },
                "haystack_ngram": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15
                },
                "haystack_edgengram": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15
                }
            }
        }
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'handlers': ['file', 'sentry'],
        'level': 'WARNING',
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(name)s\t%(lineno)s\t%(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/dev/null',
            'formatter': 'default',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
}
