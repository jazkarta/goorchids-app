from django.urls import path, re_path
from haystack.forms import HighlightedSearchForm
from goorchids.site import views
from django.contrib.flatpages import views as flatpages_views


urlpatterns = [
    # Home page
    path('', views.home_view, name='site-home'),
    path('location-suggestions/', views.location_suggestions_view,
        name='site-location-suggestions'),
    path('key-by-location/', views.redirect_to_simple_key_by_location),
    path('plant-name-suggestions/', views.plant_name_suggestions_view,
        name='plant-name-suggestions'),
    path('search-suggestions/', views.search_suggestions_view,
        name='site-search-suggestions'),

    # Search results
    path('search/',
        views.GoOrchidsSearchView(
            template='search.html',
            form_class=HighlightedSearchForm,
        ),
        name='search',
    ),
    re_path(r'family/(?P<family_slug>[a-z]+)/',
        views.family_view, name='site-family'),
    re_path(r'genus/(?P<genus_slug>[a-z]+)/',
        views.genus_view, name='site-genus'),
    re_path(r'species/(?P<genus_slug>[a-z]+)/(?P<epithet>[-a-z]+)/',
        views.species_view, name='site-species'),
    re_path(r'api/maps/(?P<genus>[^/-]+)-(?P<epithet>[^/]+)-na-state-distribution-map(\.svg|/)',
        views.north_american_distribution_map,
        name='na-state-distribution-map'),
    path('about/', flatpages_views.flatpage, {'url': '/about/'}, name='site-about'),
    path('privacy/', flatpages_views.flatpage, {'url': '/privacy/'}, name='site-privacy'),
    path('terms-of-use/', flatpages_views.flatpage, {'url': '/terms-of-use/'}, name='site-terms-of-use'),
]
