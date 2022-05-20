from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from gobotany.core import botany
from gobotany.core.models import Family
from gobotany.core.models import Genus
from gobotany.core.models import GlossaryTerm
from gobotany.core.models import Synonym
from gobotany.core.models import CommonName
from gobotany.core.models import PartnerSpecies
from gobotany.core.models import Pile
from gobotany.core.models import PlantPreviewCharacter
from gobotany.core.partner import which_partner
from gobotany.plantoftheday.models import PlantOfTheDay
from gobotany.taxa.views import _images_with_copyright_holders
from gobotany.taxa.views import _format_character_value
from gobotany.taxa.views import _native_to_north_america_status
from gobotany.api.views import _distribution_map
from gobotany.search.views import GoBotanySearchView
from goorchids.core.models import GoOrchidTaxon
from goorchids.site.maps import NorthAmericanOrchidDistributionMap
from itertools import groupby
from operator import itemgetter
from datetime import date


def location_suggestions_view(request):
    """Return some suggestions for location input."""
    query = request.GET.get('q', '').lower()

    suggestions = []
    for state in sorted(settings.STATE_NAMES.values()):
        if state.lower().startswith(query):
            suggestions.append(state)

    return JsonResponse(suggestions, safe=False)


def redirect_to_simple_key_by_location(request):
    """Redirect to the simple key with a particular location selected."""
    location = request.GET.get('state_distribution', '')
    return redirect('/simple/monocots/orchid-monocots/#state_distribution=%s' %
                    (location[:1].upper() + location[1:]))


def _plant_name_suggestions(query, querytype='istartswith', site_search=False):
    """Find matching names from multiple tables."""
    assert querytype in ('istartswith', 'icontains')

    fieldmap = {
        GoOrchidTaxon: ('scientific_name',),
        Genus: ('name', 'common_name'),
        CommonName: ('common_name',),
        Synonym: ('scientific_name',),
    }
    if site_search:
        fieldmap[Family] = ('name', 'common_name')
        fieldmap[GlossaryTerm] = ('term',)

    suggestions = []
    for model, fields in fieldmap.items():
        for field in fields:
            include_field = field + '__' + querytype
            if querytype == 'istartswith':
                exclude_field = field
            else:
                exclude_field = field + '__istartswith'
            q = model.objects.filter(**{include_field: query})
            q = q.exclude(**{exclude_field: query})
            if model is GoOrchidTaxon:
                q = q.filter(ready_for_display=True)
            suggestions += list(q.values_list(field, flat=True))

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
    return JsonResponse(suggestions, safe=False)


def search_suggestions_view(request):
    """Return some suggestions for search input."""

    MAX_RESULTS = 10
    query = request.GET.get('q', '').lower()

    suggestions = []
    if query != '':
        # First look for suggestions that match at the start of the
        # query string.

        # This query is case-insensitive to return names as they appear
        # in the database regardless of the case of the query string.
        suggestions = _plant_name_suggestions(
            query, querytype='istartswith', site_search=True)

        # If fewer than the maximum number of suggestions were found,
        # try finding some additional ones that match anywhere in the
        # query string.
        if len(suggestions) < MAX_RESULTS:
            suggestions.extend(_plant_name_suggestions(
                query, querytype='icontains'))

    suggestions = suggestions[:MAX_RESULTS]
    return JsonResponse(suggestions, safe=False)


# Home page

def home_view(request):
    """View for the home page of the Go Botany site."""

    try:
        intro = FlatPage.objects.get(url='/home/').content
    except ObjectDoesNotExist:
        intro = None

    # Get or generate today's Plant of the Day, if appropriate.
    partner = which_partner(request)
    plant_of_the_day = PlantOfTheDay.get_by_date.for_day(
        date.today(), partner.short_name)
    plant_of_the_day_taxon = None
    if plant_of_the_day:
        # Get the Taxon record of the Plant of the Day.
        try:
            plant_of_the_day_taxon = GoOrchidTaxon.objects.get(
                scientific_name=plant_of_the_day.scientific_name)
        except ObjectDoesNotExist:
            pass

    plant_of_the_day_image = None
    species_images = []

    if hasattr(plant_of_the_day_taxon, 'taxon_ptr'):
        species_images = botany.species_images(
            plant_of_the_day_taxon.taxon_ptr,
            image_types='flowers,inflorescences')
    if len(species_images) == 0:
        species_images = botany.species_images(
            plant_of_the_day_taxon,
            image_types='flowers,inflorescences')

    if species_images:
        plant_of_the_day_image = species_images[0]

    return render(request, 'gobotany/home.html', {
        'intro': intro,
        'plant_of_the_day': plant_of_the_day_taxon,
        'plant_of_the_day_image': plant_of_the_day_image,
    })


# Family and Genus pages

def family_view(request, family_slug):

    family_name = family_slug.capitalize()
    family = get_object_or_404(Family, name=family_name)

    # If it is decided that common names will not be required, change the
    # default below to None so the template will omit the name if missing.
    DEFAULT_COMMON_NAME = 'common name here'
    common_name = family.common_name or DEFAULT_COMMON_NAME

    family_drawings = (family.images.filter(
                       image_type__name='example drawing'))
    if not family_drawings:
        # No example drawings for this family were specified.
        # Use 2 images from the family's species instead.
        species = family.taxa.all()
        family_drawings = []
        for s in species:
            species_images = botany.species_images(s, image_types='flowers,inflorescences')
            if len(species_images):
                family_drawings.append(species_images[0])
                if len(family_drawings) == 2:
                    break
    family_drawings = _images_with_copyright_holders(family_drawings)

    pile = family.taxa.all()[0].piles.all()[0]
    pilegroup = pile.pilegroup

    return render(request, 'gobotany/family.html', {
        'family': family,
        'common_name': common_name,
        'family_drawings': family_drawings,
        'pilegroup': pilegroup,
        'pile': pile,
        }, context_instance=RequestContext(request))


def genus_view(request, genus_slug):

    genus_name = genus_slug.capitalize()
    genus = get_object_or_404(Genus, name=genus_name)

    # If it is decided that common names will not be required, change the
    # default below to None so the template will omit the name if missing.
    DEFAULT_COMMON_NAME = 'common name here'
    common_name = genus.common_name or DEFAULT_COMMON_NAME

    genus_drawings = genus.images.filter(image_type__name='example drawing')
    if not genus_drawings:
        # No example drawings for this genus were specified.
        # Use 2 images from the genus's species instead.
        species = genus.taxa.all()
        genus_drawings = []
        for s in species:
            species_images = botany.species_images(s, image_types='flowers,inflorescences')
            if len(species_images):
                genus_drawings.append(species_images[0])
                if len(genus_drawings) == 2:
                    break
    genus_drawings = _images_with_copyright_holders(genus_drawings)

    pile = genus.taxa.all()[0].piles.all()[0]
    pilegroup = pile.pilegroup

    return render(request, 'gobotany/genus.html', {
        'genus': genus,
        'common_name': common_name,
        'genus_drawings': genus_drawings,
        'pilegroup': pilegroup,
        'pile': pile,
        }, context_instance=RequestContext(request))


# Species page


def _compare_character_values(a, b):
    choice_a = a.lower()
    choice_b = b.lower()

    # If both values are recognized as textual numbers
    # or months, compare them naturally.
    months = ['january', 'february', 'march', 'april', 'may',
        'june', 'july', 'august', 'september', 'october', 'november',
        'december']
    numbers = ['one', 'two', 'three', 'four', 'five', 'six',
        'seven', 'eight', 'nine']
    choice_a_1stword = choice_a.split(' ')[0]
    choice_b_1stword = choice_b.split(' ')[0]
    if choice_a_1stword in months and choice_b_1stword in months:
        return months.index(choice_a_1stword) - months.index(choice_b_1stword)
    if choice_a_1stword in numbers and choice_b_1stword in numbers:
        return numbers.index(choice_a_1stword) - numbers.index(choice_b_1stword)

    # If both are a number or begin with one, sort numerically.
    try:
        int_choice_a = int(choice_a)
        int_choice_b = int(choice_b)
    except:
        pass
    else:
        return int_choice_a - int_choice_b

    # Otherwise, sort alphabetically.

    # Exception: always make Doesn't Apply (NA) last.
    if choice_a == 'na':
        return 1
    if choice_b == 'na':
        return -1

    if choice_a < choice_b:
        return -1
    if choice_a > choice_b:
        return 1

    return 0  # default value (no sort)


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

    species_images = []
    if hasattr(taxon, 'taxon_ptr'):
        species_images = botany.species_images(taxon.taxon_ptr)
    if len(species_images) == 0:
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
                'values': sorted((_format_character_value(v) for v in seq2),
                                 cmp=_compare_character_values),
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

    return render(request, 'gobotany/species.html', {
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
        'ready_for_display': taxon.ready_for_display,
        'compact_multivalue_characters': COMPACT_MULTIVALUE_CHARACTERS,
        'brief_characteristics': preview_characters,
        'all_characteristics': all_characteristics,
        'epithet': epithet,
        'native_to_north_america': native_to_north_america
    }, context_instance=RequestContext(request))


def north_american_distribution_map(request, genus, epithet):
    distribution_map = NorthAmericanOrchidDistributionMap()
    return _distribution_map(request, distribution_map, genus, epithet)


class GoOrchidsSearchView(GoBotanySearchView):

    def get_results(self):
        res = []
        for r in super(GoOrchidsSearchView, self).get_results():
            if r._model is not GoOrchidTaxon:
                res.append(r)
            else:
                if r.object.ready_for_display:
                    res.append(r)
        return res
