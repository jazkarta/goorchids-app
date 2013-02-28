from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from gobotany.core.models import HomePageImage
import json


# Home page

def home_view(request):
    """View for the home page of the Go Orchids site."""

    home_page_images = HomePageImage.objects.all()

    return render_to_response('home.html', {
        'home_page_images': home_page_images,
        }, context_instance=RequestContext(request))


def location_suggestions_view(request):
    """Return some suggestions for location input."""
    query = request.GET.get('q', '').lower()

    suggestions = []
    for state in sorted(settings.STATE_NAMES.values()):
        if state.lower().startswith(query):
            suggestions.append(state)

    return HttpResponse(json.dumps(suggestions),
                        mimetype='application/json; charset=utf-8')


def redirect_to_simple_key_by_location(request):
    """Redirect to the simple key with a particular location selected."""
    location = request.GET.get('state_distribution', '')
    return redirect('/simple/monocots/orchid-monocots#state_distribution=%s' % location)
