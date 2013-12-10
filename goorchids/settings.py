from gobotany.settings import *
import os

if 'MEMCACHIER_SERVERS' in os.environ:
    os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

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
    'goorchids.herokuapp.com',
]

ROOT_URLCONF = 'goorchids.core.urls'
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), 'core', 'static'),
    os.path.join(os.path.dirname(__file__), '..', 'external', 'gobotany-app', 'gobotany', 'static'),
]
SOUTH_TESTS_MIGRATE = False

HAYSTACK_INCLUDE_SPELLING = True

if 'test' in sys.argv:
    pass
else:
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME',
                                             'goorchids')

#INSTALLED_APPS.remove('gobotany.plantshare')
INSTALLED_APPS.remove('piston')
INSTALLED_APPS.remove('facebook_connect')
INSTALLED_APPS.remove('captcha')

INSTALLED_APPS = [
    'goorchids.core',
    'goorchids.site',
    'goorchids.editor',
    'django.contrib.sites',
    'django.contrib.flatpages',
] + INSTALLED_APPS

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',)

LOGIN_URL = '/accounts/login'
