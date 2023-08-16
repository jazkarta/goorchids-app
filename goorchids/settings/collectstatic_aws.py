from .settings import *

#Let django-storages update staticfiles to S3 when running collectstatic
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_LOCATION = 'static'
