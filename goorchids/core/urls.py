from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from django.urls import include, path

from gobotany.taxa import views as taxa_views
from . import views


handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

admin.autodiscover()

urlpatterns = [
    path('', include('goorchids.site.urls')),
    path('edit/', include('goorchids.editor.urls')),
    path('loaddata/', views.loaddata, name='goorchids-loaddata'),
    path('dumpdata/', views.dumpdata, name='goorchids-dumpdata'),
    path('admin/', admin.site.urls),
    path('api/', include('gobotany.api.urls')),
    path('edit/', include('gobotany.editor.urls')),
    path('plantoftheday/', include('gobotany.plantoftheday.urls')),
    # path('accounts/', include('registration.auth_urls')),
    path('', include('gobotany.search.urls')),
    path('', include('gobotany.site.urls')),
    path('species/(?P<genus_slug>[a-z]+)/(?P<epithet>[-a-z\.\s\(\)]+)/',
        taxa_views.species_view, name='taxa-species'),
    path('', include('gobotany.taxa.urls')),
    path('', include('gobotany.simplekey.urls')),
    path('plantshare/', include('gobotany.plantshare.urls')),
]


# Serve uploaded media files as static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# For now, always have staticfiles turned on, even in production.

class FakeSettings():
    DEBUG = True

def fix_staticfiles():
    import django.contrib.staticfiles.views
    import django.conf.urls.static

    django.conf.urls.static.settings = FakeSettings()
    django.contrib.staticfiles.views.settings = FakeSettings()

# fix_staticfiles()
# urlpatterns += staticfiles_urlpatterns()
