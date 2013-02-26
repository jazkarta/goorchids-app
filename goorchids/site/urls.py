from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

from goorchids.site import views

urlpatterns = patterns(
    '',

    # Home page
    url(r'^$', views.home_view, name='site-home'),
    )
