from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from gobotany.core.models import HomePageImage
from gobotany.core.models import Taxon
from gobotany.core.models import Genus
from gobotany.core.models import Synonym
from gobotany.core.models import CommonName
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


def _plant_name_suggestions(query, querytype='istartswith'):
    """Find matching names from multiple tables."""
    assert querytype in ('istartswith', 'icontains')

    fieldmap = {
        Taxon: ('scientific_name',),
        Genus: ('name', 'common_name'),
        CommonName: ('common_name',),
        Synonym: ('scientific_name',),
    }

    suggestions = []
    for model, fields in fieldmap.items():
        for field in fields:
            include_field = field + '__' + querytype
            if querytype == 'istartswith':
                exclude_field = field
            else:
                exclude_field = field + '__istartswith'
            suggestions += list(model.objects.filter(
                **{include_field: query}).
                exclude(**{exclude_field: query}).
                values_list(field, flat=True))

    suggestions.sort()
    return suggestions


def plant_name_suggestions_view(request):
    """Return some suggestions for genus/taxon name input."""

    MAX_RESULTS = 10
    query = request.GET.get('q', '').lower()

    suggestions = []
    if query != '':
        # First look for suggestions that match at the start of the
        # query string.

        # This query is case-insensitive to return names as they appear
        # in the database regardless of the case of the query string.
        suggestions = _plant_name_suggestions(query, querytype='istartswith')

        # If fewer than the maximum number of suggestions were found,
        # try finding some additional ones that match anywhere in the
        # query string.
        if len(suggestions) < MAX_RESULTS:
            suggestions.extend(_plant_name_suggestions(
                query, querytype='icontains'))

    suggestions = suggestions[:MAX_RESULTS]
    return HttpResponse(json.dumps(suggestions),
                        mimetype='application/json; charset=utf-8')
