from gobotany.settings import *

ROOT_URLCONF = 'goorchids.core.urls'

INSTALLED_APPS.insert(0, 'goorchids.core')

if 'test' in sys.argv:
    pass
else:
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME',
                                             'goorchids')
INSTALLED_APPS.insert(0, 'goorchids.core')
