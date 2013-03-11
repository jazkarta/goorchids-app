from django.contrib import admin
admin.autodiscover()

from . import views
from django.conf.urls.defaults import include, patterns, url
# Just use the gobotany config directly for now
from gobotany.urls import urlpatterns, handler404, handler500

urlpatterns = patterns(
    '',
    url(r'^', include('goorchids.site.urls')),
    url(r'^edit/', include('goorchids.editor.urls')),
    url(r'^loaddata/', views.loaddata,
        name='goorchids-loaddata'),
    url(r'^dumpdata/', views.dumpdata,
        name='goorchids-dumpdata'),
    ) + urlpatterns
