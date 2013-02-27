from django.conf.urls.defaults import patterns, url

from goorchids.site import views
from gobotany.taxa import views as taxa_views

urlpatterns = patterns(
    '',

    # Home page
    url(r'^$', views.home_view, name='site-home'),
    url('^family/(?P<family_slug>[a-z]+)/$',
        taxa_views.family_view, name='site-family'),
    url('^genus/(?P<genus_slug>[a-z]+)/$',
        taxa_views.genus_view, name='site-genus'),
    url('^species/(?P<genus_slug>[a-z]+)/(?P<epithet>[-a-z]+)/$',
        taxa_views.species_view, name='site-species'),
    )
