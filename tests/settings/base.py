from stock.settings import *


def exclude(sequence, to_exclude):
    return filter(lambda item: item not in to_exclude, sequence)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

MEDIA_ROOT = join(DEV_TMP_DIR, 'test_media')

INSTALLED_APPS = exclude(INSTALLED_APPS, ['south', 'haystack'])
