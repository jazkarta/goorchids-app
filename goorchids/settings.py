from gobotany.settings import *
import os

SITE_ID = 1

STATE_NAMES = {
    # US
    'ak': u'Alaska',
    'al': u'Alabama',
    'ar': u'Arkansas',
    'az': u'Arizona',
    'ca': u'California',
    'co': u'Colorado',
    'ct': u'Connecticut',
    'dc': u'District of Columbia',
    'de': u'Delaware',
    'fl': u'Florida',
    'ga': u'Georgia',
    'hi': u'Hawaii',
    'ia': u'Iowa',
    'id': u'Idaho',
    'il': u'Illinois',
    'in': u'Indiana',
    'ks': u'Kansas',
    'ky': u'Kentucky',
    'la': u'Louisiana',
    'ma': u'Massachusetts',
    'md': u'Maryland',
    'me': u'Maine',
    'mi': u'Michigan',
    'mn': u'Minnesota',
    'mo': u'Missouri',
    'ms': u'Mississippi',
    'mt': u'Montana',
    'nc': u'North Carolina',
    'nd': u'North Dakota',
    'ne': u'Nebraska',
    'nh': u'New Hampshire',
    'nj': u'New Jersey',
    'nm': u'New Mexico',
    'nv': u'Nevada',
    'ny': u'New York',
    'oh': u'Ohio',
    'ok': u'Oklahoma',
    'or': u'Oregon',
    'pa': u'Pennsylvania',
    'ri': u'Rhode Island',
    'sc': u'South Carolina',
    'sd': u'South Dakota',
    'tn': u'Tennessee',
    'tx': u'Texas',
    'ut': u'Utah',
    'va': u'Virginia',
    'vt': u'Vermont',
    'wa': u'Washington',
    'wi': u'Wisconsin',
    'wv': u'West Virginia',
    'wy': u'Wyoming',

    # Canada
    'ab': u'Alberta',
    'bc': u'British Columbia',
    'mb': u'Manitoba',
    'nb': u'New Brunswick',
    'nl': u'Newfoundland and Labrador',
    'nt': u'Northwest Territories',
    'ns': u'Nova Scotia',
    'nu': u'Nunavut',
    'on': u'Ontario',
    'pe': u'Prince Edward Island',
    'qc': u'Quebec',
    'sk': u'Saskatchewan',
    'yt': u'Yukon'
}

ALLOWED_HOSTS = [
    'goorchids.northamericanorchidcenter.org',
    'goorchids-staging.herokuapp.com',
    'goorchids-dev.herokuapp.com',
    'goorchids.herokuapp.com',
]

ROOT_URLCONF = 'goorchids.core.urls'
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), 'core', 'static'),
    os.path.join(os.path.dirname(__file__), '..', 'external', 'gobotany-app', 'gobotany', 'static'),
]
# Fix S3 staticfiles configuration
if DEFAULT_FILE_STORAGE == 'storages.backends.s3boto.S3BotoStorage':
    # Let django-storages update staticfiles to S3 when running collectstatic
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# INSTALLED_APPS.remove('gobotany.plantshare')
# INSTALLED_APPS.remove('facebook_connect')
# INSTALLED_APPS.remove('captcha')

INSTALLED_APPS = [
    'goorchids.site',
    'goorchids.editor',
    'goorchids.core',
    'django.contrib.flatpages',
] + INSTALLED_APPS

MIDDLEWARE = MIDDLEWARE + (
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',)

LOGIN_URL = '/accounts/login'

TEMPLATES[0]['OPTIONS']['loaders'] = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'goorchids.core.app_template_loader.Loader',
]
TEMPLATES[0]['APP_DIRS'] = False

if os.environ.get('FORCE_SSL', 'false').lower() != 'true':
    try:
        MIDDLEWARE = list(MIDDLEWARE)
        MIDDLEWARE.remove('sslify.middleware.SSLifyMiddleware')
        MIDDLEWARE = tuple(MIDDLEWARE)
        SESSION_COOKIE_SECURE = False
        CSRF_COOKIE_SECURE = False
    except ValueError:
        pass
    # AWS_S3_SECURE_URLS = False

ADMINS = (
    ('Go Orchids Dev', 'chiruzzi.marco@gmail.com'),
)
