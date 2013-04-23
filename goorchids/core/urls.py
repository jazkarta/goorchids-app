from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.defaults import include, patterns, url
from . import views


handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('goorchids.site.urls')),
    url(r'^edit/', include('goorchids.editor.urls')),
    url(r'^loaddata/', views.loaddata,
        name='goorchids-loaddata'),
    url(r'^dumpdata/', views.dumpdata,
        name='goorchids-dumpdata'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('gobotany.api.urls')),
    url(r'^edit/', include('gobotany.editor.urls')),
    url(r'^plantoftheday/', include('gobotany.plantoftheday.urls')),
    url(r'^accounts/', include('registration.auth_urls')),
    url(r'^', include('gobotany.search.urls')),
    url(r'^', include('gobotany.site.urls')),
    url(r'^', include('gobotany.taxa.urls')),
    url(r'^', include('gobotany.simplekey.urls')),)


# Serve uploaded media files as static files in development
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
            }),
       )
# For now, always have staticfiles turned on, even in production.

class FakeSettings():
    DEBUG = True

def fix_staticfiles():
    import django.contrib.staticfiles.views
    import django.conf.urls.static

    django.conf.urls.static.settings = FakeSettings()
    django.contrib.staticfiles.views.settings = FakeSettings()

fix_staticfiles()
urlpatterns += staticfiles_urlpatterns()
