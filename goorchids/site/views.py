from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from gobotany.core import botany
from gobotany.core.models import HomePageImage
from gobotany.core.models import Taxon
from gobotany.core.models import Genus
from gobotany.core.models import Synonym
from gobotany.core.models import CommonName
from gobotany.core.models import PartnerSpecies
from gobotany.core.models import Pile
from gobotany.core.models import PlantPreviewCharacter
from gobotany.core.partner import which_partner
from gobotany.taxa.views import _images_with_copyright_holders
from gobotany.taxa.views import _format_character_value
from gobotany.taxa.views import _native_to_north_america_status
from gobotany.api.views import _distribution_map
from goorchids.core.models import GoOrchidTaxon
from maps import NorthAmericanOrchidDistributionMap
from itertools import groupby
from operator import itemgetter
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


# Species page

def species_view(request, genus_slug, epithet):

    COMPACT_MULTIVALUE_CHARACTERS = ['Habitat', 'New England state',
                                     'Specific Habitat']

    genus_name = genus_slug.capitalize()
    scientific_name = '%s %s' % (genus_name, epithet)
    taxon = get_object_or_404(GoOrchidTaxon, scientific_name=scientific_name)

    scientific_name_short = '%s. %s' % (scientific_name[0], epithet)

    pile_slug = request.GET.get('pile')
    if pile_slug:
        pile = get_object_or_404(Pile, slug=pile_slug)
    else:
        # Randomly grab the first pile from the species
        pile = taxon.piles.order_by('id')[0]
    pilegroup = pile.pilegroup

    partner = which_partner(request)
    partner_species = None
    if partner:
        rows = PartnerSpecies.objects.filter(
            species=taxon, partner=partner).all()
        if rows:
            partner_species = rows[0]

    species_in_simple_key = (partner_species and partner_species.simple_key)
    key = request.GET.get('key')
    if not key:
        if species_in_simple_key:
            key = 'simple'
        else:
            key = 'full'
    
    ready_for_display = taxon.ready_for_display

    species_images = botany.species_images(taxon)
    images = _images_with_copyright_holders(species_images)

    # Get the set of preview characteristics.

    plant_preview_characters = {
        ppc.character_id: ppc.order for ppc in
        PlantPreviewCharacter.objects.filter(pile=pile, partner_site=partner)
    }

    # Select ALL character values for this taxon.

    character_values = list(taxon.character_values.select_related(
        'character', 'character__character_group'))

    # Throw away values for characters that are not part of this pile.

    pile_ids = (None, pile.id)  # characters like 'habitat' have pile_id None
    character_values = [v for v in character_values
                        if v.character.pile_id in pile_ids]

    # Create a tree of character groups, characters, and values.

    get_group_name = lambda v: v.character.character_group.name
    get_character_name = lambda v: v.character.friendly_name

    character_values.sort(key=get_character_name)
    character_values.sort(key=get_group_name)

    all_characteristics = []
    for group_name, seq1 in groupby(character_values, get_group_name):
        characters = []

        for character_name, seq2 in groupby(seq1, get_character_name):
            seq2 = list(seq2)
            character = seq2[0].character  # arbitrary; all look the same
            characters.append({
                'group': character.character_group.name,
                'name': character.friendly_name,
                'values': sorted(_format_character_value(v) for v in seq2),
                'in_preview': character.id in plant_preview_characters,
                'preview_order': plant_preview_characters.get(character.id, -1),
            })

        all_characteristics.append({
            'name': group_name,
            'characters': characters
        })

    # Pick out the few preview characters for separate display.

    preview_characters = sorted((
        character
        for group in all_characteristics
        for character in group['characters']
        if character['in_preview']
    ), key=itemgetter('preview_order'))

    native_to_north_america = _native_to_north_america_status(taxon)

    return render_to_response('gobotany/species.html', {
        'pilegroup': pilegroup,
        'pile': pile,
        'scientific_name': scientific_name,
        'scientific_name_short': scientific_name_short,
        'taxon': taxon,
        'key': key,
        'species_in_simple_key': species_in_simple_key,
        'common_names': taxon.common_names.all(),  # view uses this 3 times
        'images': images,
        'partner_heading': partner_species.species_page_heading
            if partner_species else None,
        'partner_blurb': partner_species.species_page_blurb
            if partner_species else None,
        'compact_multivalue_characters': COMPACT_MULTIVALUE_CHARACTERS,
        'brief_characteristics': preview_characters,
        'all_characteristics': all_characteristics,
        'epithet': epithet,
        'native_to_north_america': native_to_north_america
    }, context_instance=RequestContext(request))


def north_american_distribution_map(request, genus, epithet):
    distribution_map = NorthAmericanOrchidDistributionMap()
    return _distribution_map(request, distribution_map, genus, epithet)
