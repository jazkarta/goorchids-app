from django.conf.urls.defaults import patterns, url

from goorchids.site import views
from gobotany.taxa import views as taxa_views

urlpatterns = patterns(
    '',

    # Home page
    url(r'^$', views.home_view, name='site-home'),
    url(r'^location-suggestions/', views.location_suggestions_view,
        name='site-location-suggestions'),
    url(r'^key-by-location/', views.redirect_to_simple_key_by_location),
    url(r'^plant-name-suggestions/', views.plant_name_suggestions_view,
        name='plant-name-suggestions'),

    url(r'^family/(?P<family_slug>[a-z]+)/$',
        taxa_views.family_view, name='site-family'),
    url(r'^genus/(?P<genus_slug>[a-z]+)/$',
        taxa_views.genus_view, name='site-genus'),
    url(r'^species/(?P<genus_slug>[a-z]+)/(?P<epithet>[-a-z]+)/$',
        views.species_view, name='site-species'),
    url(r'^api/maps/(?P<genus>[^/-]+)-(?P<epithet>[^/]+)-na-state-distribution-map(\.svg|/)',
        views.north_american_distribution_map,
        name='na-state-distribution-map'),
    ) + patterns(
    'django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='site-about'),
    )
