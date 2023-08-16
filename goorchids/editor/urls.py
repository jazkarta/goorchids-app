from django.urls import path

from . import views

urlpatterns = [
    path('cv/all-edits', views.list_edits, name='goorchids-list-edits'),
    path('cv/edited-taxa', views.list_edited_taxa,
        name='goorchids-edited-taxa'),
]
