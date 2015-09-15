from django.conf.urls import url
from haystack.forms import HighlightedSearchForm
from goorchids.site import views
from django.contrib.flatpages import views as flatpages_views

urlpatterns = [
    # Home page
    url(r'^$', views.home_view, name='site-home'),
    url(r'^location-suggestions/', views.location_suggestions_view,
        name='site-location-suggestions'),
    url(r'^key-by-location/', views.redirect_to_simple_key_by_location),
    url(r'^plant-name-suggestions/', views.plant_name_suggestions_view,
        name='plant-name-suggestions'),
    url(r'^search-suggestions/', views.search_suggestions_view,
        name='site-search-suggestions'),

    # Search results
    url(r'^search/$',
        views.GoOrchidsSearchView(
            template='search.html',
            form_class=HighlightedSearchForm,
        ),
        name='search',
    ),
    url(r'^family/(?P<family_slug>[a-z]+)/$',
        views.family_view, name='site-family'),
    url(r'^genus/(?P<genus_slug>[a-z]+)/$',
        views.genus_view, name='site-genus'),
    url(r'^species/(?P<genus_slug>[a-z]+)/(?P<epithet>[-a-z]+)/$',
        views.species_view, name='site-species'),
    url(r'^api/maps/(?P<genus>[^/-]+)-(?P<epithet>[^/]+)-na-state-distribution-map(\.svg|/)',
        views.north_american_distribution_map,
        name='na-state-distribution-map'),
    url(r'^about/$', flatpages_views.flatpage, {'url': '/about/'}, name='site-about'),
    url(r'^privacy/$', flatpages_views.flatpage, {'url': '/privacy/'}, name='site-privacy'),
    url(r'^terms-of-use/$', flatpages_views.flatpage, {'url': '/terms-of-use/'}, name='site-terms-of-use'),
]
