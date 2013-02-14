from django.contrib import admin
admin.autodiscover()

# Just use the gobotany config directly for now
from gobotany.urls import urlpatterns, handler404, handler500
