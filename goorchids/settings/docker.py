from goorchids.settings.settings import *

if 'test' not in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'gobotany',
            'HOST': 'postgres',
            'PORT': 5432,
            'USER': 'postgres',
            'PASSWORD': 'secret',
        }
    }
    HAYSTACK_CONNECTIONS['default']['URL'] = 'http://solr:8983/solr/gobotany_solr_core'
    HAYSTACK_CONNECTIONS['default']['ADMIN_URL'] = 'http://solr:8983/solr/#/~cores'

ALLOWED_HOSTS = ["*"]
