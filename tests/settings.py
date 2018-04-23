# """
# Django settings for tests project.
# """
from oscar import get_core_apps, OSCAR_MAIN_TEMPLATE_DIR
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '+&l^d!%soa4gxsnx7_txbo0x3uv$@4i&n!r8yte72otwqo7vmh'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

OSCAR_DEFAULT_CURRENCY = 'zar'
OSCAR_REQUIRED_ADDRESS_FIELDS = []

MIDDLEWARE_CLASSES = (

    'django.contrib.sessions.middleware.SessionMiddleware',

)

INSTALLED_APPS = [
    'payfast',
    'django.contrib.contenttypes',
    'django.contrib.auth',
] + get_core_apps()
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.core.context_processors.metadata',
            ],
        }
    }
]


SITE_ID = 1
ROOT_URLCONF = 'tests.urls'

STATIC_URL = '/'
STATIC_ROOT = '/static/'

OSCAR_IMAGE_FOLDER = '/media/images'
OSCAR_PROMOTION_FOLDER = '/promotions/'
OSCAR_DELETE_IMAGE_FILES = True
OSCAR_SLUG_ALLOW_UNICODE = False
OSCAR_EAGER_ALERTS = True
PAYFAST_MERCHANT_ID = 10000100
PAYFAST_MERCHANT_KEY = '46f0cd694581a'
PAYFAST_PASSPHRASE = 'MYSECRETPASSPHRASE'
