from django.urls import path, re_path

from . import views

urlpatterns = [
    path('cv/all-edits', views.list_edits, name='goorchids-list-edits'),
    path('cv/edited-taxa', views.list_edited_taxa,
        name='goorchids-edited-taxa'),
    re_path(r'^cv/([^/]+)-characters/([^/]+)/$', views.edit_pile_character),
    re_path(r'^cv/([^/]+)-taxa/([^/]+)/$', views.edit_pile_taxon),
    re_path(r'^cv/lit-sources/([.0-9]+)/$', views.edit_lit_sources),
]
