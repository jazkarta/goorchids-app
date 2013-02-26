from django.template import RequestContext
from django.shortcuts import render_to_response
from gobotany.core.models import HomePageImage


# Home page

def home_view(request):
    """View for the home page of the Go Orchids site."""

    home_page_images = HomePageImage.objects.all()

    return render_to_response('home.html', {
        'home_page_images': home_page_images,
        }, context_instance=RequestContext(request))
