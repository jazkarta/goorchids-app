from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cv/all-edits', views.list_edits, name='goorchids-list-edits'),
    url(r'^cv/edited-taxa', views.list_edited_taxa,
        name='goorchids-edited-taxa'),
]
